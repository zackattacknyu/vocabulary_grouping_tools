import requests

from pprint import pprint

resp = requests.get('https://openapi.naver.com/v1/papago/n2mt',
                    params={'source': 'en',
                            'target': 'ko',
                            'text': 'Here I am'},
                    headers={'X-Naver-Client-Id': 'WyPCRsYaxeKJ748sfFdV',
                             'X-Naver-Client-Secret': 'EFpX_fxYpo'})

pprint(resp.json())
