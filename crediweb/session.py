import requests


class CWSession(requests.Session):
    def __init__(self, useragent="CrediWeb crawler"):
        super(CWSession, self).__init__()

        self.headers = {
            'User-Agent': useragent,
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, compress'}
