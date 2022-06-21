#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File name: hanja.py
import sys
import hanconv
import os.path

#Definitions
def preface(): #Print Preface
	print u'Hanja Hangul Converter 0.0.6    by Sung-il KIM (masoris@gmail.com)'
	print u'Commands: exit(종료), mode(방식), reverse(역변환), list(목록)'
	print u'          convfile(파일변환) [filename]'
	print u'Type hanja to convert and press enter.'

def command(cmd): #Analyzing Command and Get Result
	global looping, reverse

	#Commands
	if cmd.lower() in (u'exit',u'종료'):
		looping = False
		return
	elif cmd.lower() in (u'list', u'목록'):
		hanconv.printlistfrommode(mode)
	elif cmd.lower() in (u'reverse', u'정변환', u'역변환'):
		if(reverse == True):
			reverse = False
			print u'Convert Hanja to Hangul'
			return
		elif(reverse == False):
			reverse = True
			print u'Convert Hangul to Hanja (Reverse)'
			return
	elif cmd.lower() in (u'mode', u'방식', u'모드'):
		setmode()
		print ''
		preface()
		return

	if cmd.lower()[0:5] == u'파일변환 ':
		cmd = u'convfile '+cmd[5:]
	if cmd.lower()[0:9] == u'convfile ':
		filename = cmd[9:].replace('\'','').replace('\"','')
		if not os.path.exists(filename):
			print 'ERROR: file \''+filename+'\' doesn\'t exists'
			return
		try:
			oritxt = unicode(file(filename).read(),'utf8')
			print u'Input :\n'+oritxt
			resulttxt = hanconv.convert(oritxt,mode,reverse)
			print u'Output :\n'+resulttxt
			file(filename,'w').write(resulttxt.encode('utf8'))
			print 'Successed Converting file\''+filename+'\'.'
		except:
			print 'ERROR: A error occur in converting file \''+filename+'\'.'	
		return

	#Convert
	print u'出'+unicode(times)+u'> '+convert(cmd)

def convert(txt): #Convert Hanja to Hangul
	return hanconv.convert(txt, mode, reverse)

def setmode(mod=u"-1"):
	global mode

	#Select Mode
	if(mod == u"-1"):
		print u'Choose mode to convert Hanja to Hangul'
		print u'1. Han unification only (Wikipedia, default)'
		print u'2. Han unification and CJK Compatibility Forms (MS Word)'
		print u'3. Without duuembeobchik (North Korean)'
		print u'4. Apply Unicode normalization algorithm'
		print u'5. (experiment) Compatible convert with both ways (1, 2)'
		print u'6. (experiment) Convert Hangul to Hanja'
		mod = unicode(raw_input(u'擇> '.encode(defaultencoding)),defaultencoding)
	
	mod = unicode(mod)
	if mod in hanconv.modes:
		mode = mod
	else:
		mode = u'1'

	if(message):
		print u'Mode '+mode+u' Selected'
		print u'Total '+unicode(hanconv.getlenoflistfrommode(mode))+' of indexes'


#Set Variations
looping = True
times = 0 #The number of looping times
reverse = False #Reverse Converting
message = False #Print Message
mode = '1' #Current Mode
arginput = ''
defaultencoding = sys.getfilesystemencoding()


	
#Start Programme
#Arguments Start
#Is argv1 is text to convert or a filename?
if(len(sys.argv)>=2):
	try:
		arginput = unicode(file(sys.argv[1]).read(),'utf8')		
	except:
		arginput = unicode(sys.argv[1],defaultencoding)

#Convert argv1 and print result
if(len(sys.argv)==2):
	print hanconv.convert(arginput)

#Convert argv1 by argv2 mode and print result
elif(len(sys.argv)==3):
	print hanconv.convert(arginput,sys.argv[2])

#Convert argv1 by argv2 mode and save result to argv3 file
elif(len(sys.argv)==4):
	file(sys.argv[3], 'w').write(hanconv.convert(arginput,sys.argv[2]).encode('utf8'))

#Start looping
else:
	message = True
	preface()
	print ''
	setmode()
	
	while(looping):
		times = times + 1
		command(unicode(raw_input(u'\n入'.encode(defaultencoding)+str(times)+'> '), defaultencoding))
#End Programme

