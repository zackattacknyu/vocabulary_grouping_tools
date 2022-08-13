import os
import sys
import json
import urllib.request
import urllib.parse

client_id = "WyPCRsYaxeKJ748sfFdV" # 개발자센터에서 발급받은 Client ID 값
client_secret = "EFpX_fxYpo" # 개발자센터에서 발급받은 Client Secret 값
#encText = urllib.parse.quote("반갑습니다")
#encText = urllib.parse.quote("피")
encText = urllib.parse.quote("저는 한국에 갔어")
data = "source=ko&target=en&text=" + encText
url = "https://openapi.naver.com/v1/papago/n2mt"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request, data=data.encode("utf-8"))
rescode = response.getcode()
if(rescode==200):
    response_body = response.read().decode('utf-8')
    response_json = json.loads(response_body)
    print(response_json['message']['result']['translatedText'])
else:
    print("Error Code:" + rescode)