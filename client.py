import requests
import base64
import json
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

# helper functions that make foreign formats similar to ours
def clean_dict(dirty):
    result = {}
    for key,value in dirty.items():
        # if the type for some key is not str, make it an empty
        # str so that the format matches ours
        if type(value) != str:
            value = ''
        result[key] = value

    return result

def handle_image(dirty):
    # our image posts use the image field to store images
    # foreign formats use "content" to store them
    if dirty.get('content') is not None:
        dirty['image'] = dirty['content']
    elif dirty.get('description') is not None:
        dirty['image'] = dirty['description']
    # base64imagefield HATES base64 images that don't have
    # proper padding, so this is to make sure that it works
    if dirty['image'][-1] != '=':
        dirty['image'] += '='
    return dirty

# get the authorID for a foreign author
def handle_author(dirty):
    a = dirty.get("author").split('/')[-1]
    return a

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
    url = 'https://sociallydistributed.herokuapp.com/authors/'
    hosturl = 'https://sociallydistributed.herokuapp.com/'

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




def getNodeAuthor_App2(author_id):
    url = 'https://sociallydistributed.herokuapp.com/authors/'
    hosturl = 'https://sociallydistributed.herokuapp.com/'

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



def getNodePost_app2(author_id):
    url = 'https://sociallydistributed.herokuapp.com/posts/authors/'
    hosturl = 'https://sociallydistributed.herokuapp.com/'

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





def postFollow(data, author_id):
    #"type": "Follow",
    #"actor":{"id":"cfd9d228-44df-4a95-836f-c0cb050c7ad6"},
    #"object":{"id":"971fa387-b101-4276-891f-d970f2cf0cad"}

    author, status_code = getNodeAuthor_App2(author_id)
    if status_code != 200:
        error_msg = "Author id not found"
        return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
    else:
        url =  settings.HOST_NAME + 'authors/'+ author_id +'/inbox'
        username = 'superuser'
        password = 'password'
        data['actor'] = author
        request_data = data
        
        '''"author:"urltoauthor", "object":"urltoobject", "type":"Follow", "Summary":"username liked your post"'''
        request_data = {"author":data.actor, "object":data.object, "type":"Follow", "Summary":"A Follow Request"}
    #Make summary manually 
    credentials = f'{username}:{password}'
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    authorization_header = f'Basic {encoded_credentials}'
    headers = {'Authorization': authorization_header}
    # This should in theory work for the Yoshi APP, Not ready yet so testing when they get it done 
    response = requests.post(url, headers=headers, data=request_data)

    #Check if they return an HTTP response, IF not do HTTP response 200 OK 
    if response.status_code == 200:
        return Response("OK", status=status.HTTP_200_OK)

    ''' Our Way to send a follow request.  
    "type":"Follow",
        "actor": {
                "id": "c164d06a-a922-4535-9c3d-d3ec2cfc4e9a"
                },
        "object": {
            "id": "b7cbbd87-3da4-48a2-ab97-ee0331276412"
                }'''

def getNodeAuthor(author_id):

    author, status_code = getNodeAuthor_App2(author_id)
    if status_code != 200:
        return None, status_code
    return author