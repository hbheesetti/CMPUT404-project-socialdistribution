import requests
import base64
from rest_framework.response import Response
from rest_framework import status

from Remote.auth import *
from Remote.Authors import *
from datetime import datetime, date
import json

def getNodePost_Yoshi(author_id):
    url = 'https://yoshi-connect.herokuapp.com/authors/'

    url = url + author_id + '/posts/'
    
    response = requests.get(url)
    status_code = response.status_code
   
    if status_code == 200:
        json_response = response.json()
        return(json_response, status_code)
    else: return (None, status_code)


def getAllPosts_app2():
    url = 'https://sociallydistributed.herokuapp.com/posts/public'

    headers = app2_headers()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        return(json_response)

def getAllPosts_Yoshi():
    authors = getNodeAllAuthors_Yoshi()
    posts = []
    for author in authors:
        author_id = getAuthorId(author["id"])
        items,_ = getNodePost_Yoshi(author_id)
        items = items["items"]
        posts = posts + items
    return posts

def getNodePost_social_distro(author_id):
    url = 'https://social-distro.herokuapp.com/api/authors/'

    url = url + author_id + '/posts/'

    response = requests.get(url, headers=distro_headers())
    status_code = response.status_code
    if status_code == 200:
        json_response = response.json()
        print(json_response)
        return(json_response)
    
def getAllPosts_Distro():
    authors = getNodeAllAuthors_distro()
    posts = []
    for author in authors:
        author_id = getAuthorId(author["id"])
        items = getNodePost_social_distro(author_id)
        items = items["results"]
        for item in items:
            if item['visibility'] == 'PUBLIC':
                posts.append(item)
    return posts

def getAllPublicPosts():
    posts1 = getAllPosts_app2()
    posts2 = getAllPosts_Yoshi()
    posts3 = getAllPosts_Distro()
    posts = posts1+ posts2 + posts3
    return posts

def sendPost(host, data, auth_id):
    if 'yoshi' in host:
        response, status_code = sendPostYoshi(data, auth_id)
    elif 'social-distro' in host:
        response, status_code = sendPostDistro(data, auth_id)
    elif 'killme' in host:
        response, status_code = sendPostApp2(data, auth_id)
    return response

def sendPostYoshi(data, auth_id):
    url = 'https://yoshi-connect.herokuapp.com/authors/' + auth_id + '/inbox'


    #update the data to be sent in proper format maybe
    
    response = requests.post(url=url, headers=yoshi_headers(), data=data)
    status_code = response.status_code
    json_response = response.json()
    return json_response, status_code

def sendPostDistro(data, auth_id):
    url = 'https://social-distro.herokuapp.com/api/authors/' + auth_id + '/inbox'
    #setup data
    response = requests.post(url=url, headers=distro_headers(), data=data)
    status_code = response.status_code
    json_response = response.json()
    return json_response, status_code


def sendPostApp2(data, auth_id):
    url = 'https://killme.herokuapp.com/authors/' + auth_id + '/inbox'
    #setup data
    response = requests.post(url=url, headers=app2_headers(), data=data)
    status_code = response.status_code
    json_response = response.json()
    return json_response, status_code

# url = 'https://killme.herokuapp.com/authors/'
#     hosturl = "https://killme.herokuapp.com/"

#     username = 'app1team15'
#     password = 'hari1234'

#     session = requests.Session()
#     session.auth = (username, password)

#     auth = session.post(hosturl)
#     response = session.get(url)

#     json_response = response.json()
#     authors = json_response['data']
#     return authors