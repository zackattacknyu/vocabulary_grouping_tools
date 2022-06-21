#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File name: hanconv.py
import sys

def getlistfromfile(filename):
	if type(filename) is not unicode:filename = unicode(filename, defaultencoding)
	result = [[],[]]
	for line in unicode(file(filename).read(),'utf8').splitlines():
		if line.find(u'\t') == -1:continue
		if not -1 == line.find(u'#'):continue 
		if not -1 == line.find(u'?'):continue
		splited = line.rsplit(u'\t')
		if len(splited) in (0, 1):continue
		if len(splited[0]) == 0 or len(splited[1]) == 0:continue
		if len(splited[0]) != len(splited[1]):continue #Only for Hanja-Hangul Converting
		result[0].append(splited[0])
		result[1].append(splited[1])
	return result

def getlistfromfilenames(filenames):
	result = [[],[]]
	for filename in filenames:
		l = getlistfromfile(filename)
		for n in range(0, len(l[0])):
			result[0].append(l[0][n])
			result[1].append(l[1][n])
	return result

def getlistfrommode(mode):
	if type(mode) is not type(unicode()):mode = unicode(mode, defaultencoding)
	global getlistfrommodecache, getlistfrommodelastmode
	if getlistfrommodecacheenable == True:
		if getlistfrommodelastmode == mode:
			result = getlistfrommodecache
		else:
			getlistfrommodelastmode = mode
			result = getlistfromfilenames(modes[mode])
			getlistfrommodecache = result
	else:
		result = getlistfromfilenames(modes[mode])
	return result

def getlenoflistfrommode(mode):
	if type(mode) is not type(unicode()):mode = unicode(mode, defaultencoding)
	return len(getlistfrommode(mode)[0])

def printlistfrommode(mode):
	if type(mode) is not type(unicode()):mode = unicode(mode, defaultencoding)
	modelist = getlistfrommode(mode)
	errornum = 0
	for n in range(0, len(modelist[0])):
		try:
			print modelist[0][n]+u'\t'+modelist[1][n]
		except:
			errornum = errornum + 1
	print u"Total "+unicode(getlenoflistfrommode(mode))+u" of indexes"
	if errornum != 0:print unicode(errornum)+u' of indexes couldn\'t be printed because of ERROR' 
	

def convert(text = u'', mode = u'unionly', reverse=False):
	if type(mode) is not type(unicode()):mode = unicode(mode, defaultencoding)
	if type(text) is not type(unicode()):text = unicode(text, defaultencoding)
	convlist = getlistfrommode(mode)
	for n in range(0, len(convlist[0])):
		if reverse == True:
			text = text.replace(convlist[1][n], convlist[0][n])
		else:
			text = text.replace(convlist[0][n], convlist[1][n])
	return text

def initmodes():
	global modes
	#Set default modes
	modes[u'unionly'] = [u'dic0.txt', u'dic4.txt', u'dic5.txt', u'dic1.txt']
	modes[u'uniandcomp'] = [u'dic3.txt', u'dic2.txt']
	modes[u'withoutduuem'] = [u'dic0.txt', u'dic1.txt']
	modes[u'uninormal'] = [u'dic0.txt']
	modes[u'compboth'] = [u'dic4.txt', u'dic3.txt', u'dic2.txt']
	modes[u'hangul2hanja'] = [u'dic6.txt']

	#Alternative mode names
	modes[u'1'] = modes[u'unionly']
	modes[u'2'] = modes[u'uniandcomp']
	modes[u'3'] = modes[u'withoutduuem']
	modes[u'4'] = modes[u'uninormal']
	modes[u'5'] = modes[u'compboth']
	modes[u'6'] = modes[u'hangul2hanja']

getlistfrommodecacheenable = True
getlistfrommodecache = u''
getlistfrommodelastmode = u''
defaultencoding = sys.getfilesystemencoding()

modes = {}
initmodes()




