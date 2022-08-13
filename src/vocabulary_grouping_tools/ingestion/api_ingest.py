import urllib.request
import urllib.parse
import json

QUERY_PARAMS_START = 'source=ko&target=en&text='
API_URL = 'https://openapi.naver.com/v1/papago/n2mt'
ENCODING_TYPE = 'utf-8'


def get_english_translation(korean_text, client_id, client_secret):
    enc_text = urllib.parse.quote(korean_text)
    data = f'{QUERY_PARAMS_START}{enc_text}'
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
