import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

api_url='https://pgorelease.nianticlabs.com/plfe/rpc'
login_url='https://sso.pokemon.com/sso/login?service=https%3A%2F%2Fsso.pokemon.com%2Fsso%2Foauth2.0%2FcallbackAuthorize'
login_oauth='https://sso.pokemon.com/sso/oauth2.0/accessToken'

proxies = {
  'http': 'http://127.0.0.1:8888',
  'https': 'http://127.0.0.1:8888',
}
use_proxy=False
debug=True

google=True
pub=None

s=requests.session()
if use_proxy:
	s.proxies.update(proxies)
	s.verify=False
s.headers.update({'User-Agent':'Niantic App'})
#public
API_URL = 'https://pgorelease.nianticlabs.com/plfe/rpc'
LOGIN_URL = 'https://sso.pokemon.com/sso/login?service=https%3A%2F%2Fsso.pokemon.com%2Fsso%2Foauth2.0%2FcallbackAuthorize'
LOGIN_OAUTH = 'https://sso.pokemon.com/sso/oauth2.0/accessToken'
PTC_CLIENT_SECRET = 'w8ScCUXJQc6kXKw8FiOhd8Fixzht18Dq3PEVkUCP5ZPxtgyWsbTvWHFLm2wNY0JR'

SESSION = requests.session()
SESSION.headers.update({'User-Agent': 'Niantic App'})
if use_proxy:
	SESSION.proxies.update(proxies)
	SESSION.verify = False
DEBUG = True