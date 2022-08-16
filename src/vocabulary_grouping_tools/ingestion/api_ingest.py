import urllib.request
import urllib.parse
import json

API_URL = 'https://openapi.naver.com/v1/papago/n2mt'
ENCODING_TYPE = 'utf-8'

# Ref: https://developers.naver.com/docs/papago/papago-nmt-api-reference.md
def get_english_translation(korean_text, client_id, client_secret,
                            source_language='ko', target_language='en'):
    enc_text = urllib.parse.quote(korean_text)
    data = f'source={source_language}&target={target_language}&text={enc_text}'
    request = urllib.request.Request(API_URL)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode(ENCODING_TYPE))
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read().decode(ENCODING_TYPE)
        response_json = json.loads(response_body)
        return response_json['message']['result']['translatedText']
    else:
        raise ValueError(f"Error Code:{rescode}")
