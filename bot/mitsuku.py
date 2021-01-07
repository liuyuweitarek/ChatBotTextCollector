from google.cloud import translate 
import os,sys,re,random,requests,json
import urllib.parse
from termcolor import colored, cprint

class PandoraBot():
    def __init__(self, user_id='123456', dbs_path='./dbs', verbose=False):

        self.url = 'https://www.pandorabots.com/kuki/'
        self.header = {
                'User-Agent': ' '.join(('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2)',
                            'AppleWebKit/537.36 (KHTML, like Gecko)',
                            'Chrome/72.0.3626.119 Safari/537.36')),
                'Referer': self.url
                }
    def gen_rnd(self, seed=None, bites=8):
        random.seed(seed)
        hex_str = hex(random.randint(1+int((bites-1)*'ff', 16), int(bites*'ff', 16)))[2:]
        
        return hex_str

    def query(self, q):
        text = urllib.parse.quote(q)
        session = requests.Session()
        session.headers.update(self.header)
        main_page = session.get(self.url).text
        botkey = re.search(r'PB_BOTKEY: "(.*)"', main_page).groups()[0]
        client_name = str(random.randint(1337, 9696913371337)).rjust(13, '0')
        response_raw = session.post(
                f'https://miapi.pandorabots.com/talk?'
                f'botkey={botkey}&'
                f'input={text}&'
                f'client_name={client_name}&'
                f'sessionid=null&'
                f'channel=6').text
        try:
            response_json = json.loads(response_raw)
        except json.JSONDecodeError:
            response_json = {'responses': ["<i can't understand it>"]}
        response = '\n\n'.join(response_json['responses'])
        return response