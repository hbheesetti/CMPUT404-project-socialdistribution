import requests
import base64
import json

# helper function that makes foreign formats similar to ours
def clean_dict(dirty):
    result = {}
    for key,value in dirty.items():
        # if the type for some key is not str, make it an empty
        # str so that the format matches ours
        if key == "categories":
            category = ''
            for item in value:
                category += item
            value = category
        elif key == "unlisted":
            if value == True:
                result["visibility"] = "UNLISTED"
        elif type(value) != str:
            value = ''
        result[key] = value
    return result

# helper function that works on lists of foreign formats
def clean_list(dirty):
    result = []
    for i in dirty:
        # send it to the cleaner function
        result.append(clean_dict(i))
    # JSON-ifying the result for now will just be handled outside the function
    return result
        
# def getNodeAuthors_social_distro():

#     #https://social-distro.herokuapp.com/api/authors/15/
#     url = 'https://social-distro.herokuapp.com/api/authors/'

#     username = 'remote1'
#     password = 'r3mot31'
#     #remote1:r3mot31
#     credentials = f'{username}:{password}'
#     encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
#     authorization_header = f'Basic {encoded_credentials}'
#     headers = {'Authorization': authorization_header}

#     response = requests.get(url, headers=headers)
   
#     status_code = response.status_code
#     json_response = response.json()
#     authors = json_response['results']
#     return authors


def getNodeApp2():
    #https://social-distro.herokuapp.com/api/authors/15/
    url = 'https://killme.herokuapp.com/authors/'
    hosturl = 'https://killme.herokuapp.com/'

    username = 'app1team15'
    password = 'hari1234'
    #remote1:r3mot31

    session = requests.Session()
    session.auth = (username, password)

    auth = session.post(hosturl)
    response = session.get(url)

    # credentials = f'{username}:{password}'
    # encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    # authorization_header = f'Basic {encoded_credentials}'
    # headers = {'Authorization': authorization_header}

    # response = requests.get(url, headers=headers)
   
    #status_code = response.status_code
    json_response = response.json()
    authors = json_response['data']

    return authors

def getNodeAuthors_Yoshi():
    url = 'https://yoshi-connect.herokuapp.com/authors'
    #base64encoded username: minion and password: minion
    # authorization = 'minion:minion'
    # encoded_authorization = base64.b64encode(authorization.encode("utf-8"))
    # authroization_header = 'Basic ' + encoded_authorization
    # headers = {'Authorization': authroization_header}
    
    response = requests.get(url)
    status_code = response.status_code
    # response = requests.get(url, headers=headers)
    json_response = response.json()
    authors = json_response['items']

    return authors


def getNodeAuthor_Yoshi(author_id):
    url = 'https://yoshi-connect.herokuapp.com/authors/'

    url = url + author_id

    response = requests.get(url)
    status_code = response.status_code
    
    if status_code == 200:
        json_response = response.json()
       
        return(json_response, status_code)
    else: return (None, status_code)

#29c546d45f564a27871838825e3dbecb
# getNodeAuthor_Yoshi('asgasdfgdsfgd')
# getNodeAuthor_Yoshi('29c546d45f564a27871838825e3dbecb')

def getNodeAuthor_social_distro(author_id):
    url = 'https://social-distro.herokuapp.com/api/authors/'

    url = url + author_id + '/'

    response = requests.get(url,auth=("team15","team15"))
    status_code = response.status_code
   
    if status_code == 200:
        json_response = response.json()
        json_response = json.dumps(clean_dict(json_response))

        return(json_response, status_code)
    else: return (None, status_code)

def getNodeAuthors_social_distro():
    url = 'https://social-distro.herokuapp.com/api/authors/'

    response = requests.get(url,auth=("team15","team15"))
    status_code = response.status_code
    # response = requests.get(url, headers=headers)
    json_response = response.json()

    # clean the response
    authors = json.dumps(clean_list(json_response['results']))

    return authors

####### GET POSTS

def getNodePost_Yoshi(author_id):
    url = 'https://yoshi-connect.herokuapp.com/authors/'

    url = url + author_id + '/posts/'
    
    response = requests.get(url)
    status_code = response.status_code
   
    if status_code == 200:
        json_response = response.json()
        return(json_response, status_code)
    else: return (None, status_code)

def getNodePost_app2(author_id):
    url = 'https://killme.herokuapp.com/posts/authors/'
    hosturl = 'https://killme.herokuapp.com/'

    url = url + author_id + '/posts/'
    username = 'app1team15'
    password = 'hari1234'
    #remote1:r3mot31

    session = requests.Session()
    session.auth = (username, password)

    auth = session.post(hosturl)
    response = session.get(url)
    
    # credentials = f'{username}:{password}'
    # encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    # authorization_header = f'Basic {encoded_credentials}'
    # headers = {'Authorization': authorization_header}

    # response = requests.get(url, headers=headers)
    #  response = requests.get(url)
    status_code = response.status_code
    if status_code == 200:
        json_response = response.json()
        return(json_response)

#29c546d45f564a27871838825e3dbecb
# getNodeAuthor_Yoshi('asgasdfgdsfgd')
# getNodeAuthor_Yoshi('29c546d45f564a27871838825e3dbecb')

def getNodePost_social_distro(author_id):
    url = 'https://social-distro.herokuapp.com/api/authors/'

    url = url + author_id + '/posts/'
    username = 'team15'
    password = 'team15'
    #remote1:r3mot31

    session = requests.Session()
    session.auth = (username, password)

    auth = session.post(url)
    response = session.get(url)
    
    # credentials = f'{username}:{password}'
    # encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    # authorization_header = f'Basic {encoded_credentials}'
    # headers = {'Authorization': authorization_header}

    # response = requests.get(url, headers=headers)
    #  response = requests.get(url)
    status_code = response.status_code
    if status_code == 200:
        json_response = response.json()
        
        json_response = json.dumps(clean_list(json_response['results']))

        return(json_response)

# import socket

# bytes_to_read = 4096
# HOST = 'yoshi-connect.herokuapp.com'

# def get(port):

#     request = b"GET /authors HTTP/1.1\nHost:" + HOST.encode("utf-8") + b"\n\n"

#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect((HOST, port))
#     s.send(request)

#     s.shutdown(socket.SHUT_WR)

#     result = s.recv(bytes_to_read)
#     print(result.decode())
#     # while(len(result) > 0):

#     #         print(result)
#     #         result = s.recv(bytes_to_read)
#     s.close()


    
# get(80)