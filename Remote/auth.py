import base64

def app2_headers():
    username = 'app2team15'
    password = 'hari1234'
    credentials = f'{username}:{password}'
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    authorization_header = f'Basic {encoded_credentials}'
    headers = {'Authorization': authorization_header}
    return headers

def distro_headers():
    username = 'team24'
    password = 'team24'
    credentials = f'{username}:{password}'
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    authorization_header = f'Basic {encoded_credentials}'
    headers = {'Authorization': authorization_header}
    return headers

def yoshi_headers():
    username = 'minion'
    password = 'minion'
    credentials = f'{username}:{password}'
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    authorization_header = f'Basic {encoded_credentials}'
    headers = {'Authorization': authorization_header}
    return headers

def p2_headers():
    authorization_header = f'Basic cDJwYWRtaW46cDJwYWRtaW4='
    headers = {'Authorization': authorization_header}
    return headers
