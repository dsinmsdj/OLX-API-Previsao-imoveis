import requests
import pandas as pd

import ast
from datetime import datetime, timedelta

class OlxApiWrapper:

    CLIENT_NAME = 'GIA Imoveis'
    CLIENT_ID = 200352
    CLIENT_SECRET = '4hiiQxEiiaTA1diavjDcL3veI0B1dLfouQ3kbKrGNNVYUBBM'
    SCOPE = 'v2 read write'
    URL = 'https://www.olx.pt'
    GRANTS_TYPES = {'refresh_token': 'refresh_token', 'client_credentials': 'client_credentials'}
    TOKEN_REQUEST_PATH = '/api/open/oauth/token'
    TOKEN_REQUEST_PAYLOAD = {
        'grant_type': GRANTS_TYPES['client_credentials'], 
        'client_id': CLIENT_ID, 
        'client_secret': CLIENT_SECRET,
        'scope': SCOPE
        }
    REFRESH_TOKEN_REQUEST_PAYLOAD = {
        'grant_type': GRANTS_TYPES['refresh_token'], 
        'client_id': CLIENT_ID, 
        'client_secret': CLIENT_SECRET,
        'scope': SCOPE
        }

    session = None
    token = {}

    def __init__(self) -> None:
        self.session = requests.Session()
    
    def get_access_token(self) -> None:
        try:
            df: pd.DataFrame = pd.read_pickle('token')
            self.token = df.to_dict()['token']

        except FileNotFoundError:
            response = self.session.post(url=self.URL + self.TOKEN_REQUEST_PATH, data=self.TOKEN_REQUEST_PAYLOAD)
            self.response_dict = ast.literal_eval(response.content.decode('UTF-8'))
            self.token['value'] = self.response_dict['access_token']
            self.token['type'] = self.response_dict['token_type']
            self.token['scope'] = self.response_dict['scope']
            self.token['expire_date'] = (datetime.now() + timedelta(seconds=self.response_dict['expires_in'])).strftime('%Y/%d/%m %H:%M:%S')
            token_df = pd.Series(self.token).to_frame('token')
            token_df.to_pickle('token')

    def token_expired(self) -> bool:
        expiration_date: datetime = datetime.strptime(self.token['expire_date'], '%Y/%d/%m %H:%M:%S')
        Return True if datetime.now() > expiration_date else False
