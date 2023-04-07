import requests
import base64
from rest_framework.response import Response
from rest_framework import status

from Remote.auth import *
from Remote.Authors import *
from datetime import datetime, date
import json

import time

params= {
    "size": 5,
    "page": 1 
}

def getAllPosts_app2():
    url = 'https://sociallydistributed.herokuapp.com/posts/public'

    headers = app2_headers()
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    if status_code == 200:
        json_response = response.json()
        json_response = json_response["items"]
        json_response = json_response[:5]
        return(json_response)
    else: return ([])
    
def getAllPublicPosts():
    posts1 = getAllPosts_app2()
    print("yoshi")
    posts =  posts1
    print("all", posts)
    return posts

# def getNodePost_social_distro(author_id):
#     url = 'https://social-distro.herokuapp.com/api/authors/'

#     url = url + author_id + '/posts/'

#     response = requests.get(url, headers=distro_headers(), params=params)
#     status_code = response.status_code
#     if status_code == 200:
#         json_response = response.json()
#         return(json_response)
    
# def getAllPosts_Distro():
#     authors = getNodeAllAuthors_distro()
#     posts = []
#     for author in authors:
#         author_id = getAuthorId(author["id"])
#         items = getNodePost_social_distro(author_id)
#         items = items["results"]
#         for item in items:
#             if item['visibility'] == 'PUBLIC':
#                 posts.append(item)
#     return posts

# def getNodePosts_P2(author_id):
#     url = 'https://p2psd.herokuapp.com/authors/'

#     url = url + author_id + '/posts/'

#     response = requests.get(url, headers=p2_headers())
#     status_code = response.status_code
#     if status_code == 200:
#         json_response = response.json()
#         return(json_response)

# def getAllPosts_P2():
#     authors = getNodeAllAuthors_P2()
#     posts = []
#     for author in authors:
#         author_id = getAuthorId(author["id"])
#         items = getNodePosts_P2(author_id)
#         items = items["items"]
#         for item in items:
#             while len(posts) <= 5:
#                 if item['visibility'] == 'PUBLIC':
#                     posts.append(item)
#     return posts

def sendPost(host, data, auth_id):
    print(data)
    print(host)
    print(auth_id)
    
    response = Response("r")
    if 'sociallydistributed' in host:
        response, status_code = sendPostApp2(data, auth_id)
    print("returning their response")
    return response

def sendPostApp2(data, auth_id):
    url = 'https://sociallydistributed.herokuapp.com/authors/' + auth_id + '/inbox'
    #setup data
    response = requests.post(url=url, headers=app2_headers(), data=data)
    status_code = response.status_code
    json_response = response.json()
    return json_response, status_code

def clean_post(data):
    if "type" in data:
        data.pop("type")
    if "comments" in data:
        data.pop("comments")
    if data.get("id") is not None:
        data["id"] = data["id"][:-1] if data["id"].endswith('/') else data["id"]
        data["id"] = data["id"].split("/")[-1]


    return data

# post for yoshi connect:
# 
#
# {"type":"post",
# "title":"Fake post",
# "id":"http://localhost:3000/authors/08a779b240624ff899823d1024ff3aa1/posts/2da30761567a4f708a77bd5f337126d3",
# source":"http://localhost:3000/authors/08a779b240624ff899823d1024ff3aa1/posts/2da30761567a4f708a77bd5f337126d3",
# origin":"http://localhost:3000/authors/08a779b240624ff899823d1024ff3aa1/posts/2da30761567a4f708a77bd5f337126d3",
# description":"Fake description",
# contentType":"text/plain",
# content":"Fake Content",
# "author": {  
#       "type":"author",
#       "id":"http://localhost:3000/authors/08a779b240624ff899823d1024ff3aa1",
#       "host":"http://localhost:3000/",
#       "displayName":"Tommy",
#       "url":"http://localhost:3000/authors/08a779b240624ff899823d1024ff3aa1",
#       "github":"Fake url",
#       "profileImage":"Fake image",
#       },
# categories[0]:"Empty",
# comments:"http://localhost:3000/authors/08a779b240624ff899823d1024ff3aa1/posts/2da30761567a4f708a77bd5f337126d3",
# published:"2015-03-09T13:07:04+00:00",
# visibility:"PUBLIC",
# unlisted:"false" 
# }