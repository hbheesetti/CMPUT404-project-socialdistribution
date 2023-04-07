import requests
import base64
from rest_framework.response import Response
from rest_framework import status
import json
from Remote.auth import *
# from auth import *
params = {
    "size" : 100
}

# def getNodeAuthor_social_distro(author_id):
#     url = 'https://social-distro.herokuapp.com/api/authors/'
#     username = 'team24'
#     password = 'team24'
#     url = url + author_id + '/'

#     credentials = f'{username}:{password}'
#     encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
#     authorization_header = f'Basic {encoded_credentials}'
#     headers = {'Authorization': authorization_header}

#     response = requests.get(url, headers=headers)

#     status_code = response.status_code
   

#     if status_code == 200:
#         json_response = response.json()
#         return(json_response)
#     else: return ([])


# def getNodeAuthor_P2(author_id):
#     headers = p2_headers()
#     url = "https://p2psd.herokuapp.com/authors/" + author_id
#     response = requests.get(url, headers=headers)

#     status_code = response.status_code
#     if status_code == 200:
#         json_response = response.json()
#         return(json_response)
#     else: return ([])

# def getNodeAllAuthors_distro():
#     url = 'https://social-distro.herokuapp.com/api/authors/'

#     username = 'team24'
#     password = 'team24'
#     #remote1:r3mot31
#     credentials = f'{username}:{password}'
#     encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
#     authorization_header = f'Basic {encoded_credentials}'
#     headers = {'Authorization': authorization_header}

#     response = requests.get(url, headers=headers, params=params)
   
#     status_code = response.status_code
#     json_response = response.json()
#     authors = json_response['results']
#     return authors


# def getNodeAllAuthors_P2():
#     headers = p2_headers()
#     url = "https://p2psd.herokuapp.com/authors"
#     response = requests.get(url, headers=headers)
   
#     status_code = response.status_code
#     json_response = response.json()
#     authors = json_response['items']
#     print(authors)
#     return authors

def getNodeAuthor_App2(author_id):
    url = 'https://sociallydistributed.herokuapp.com/authors/'

    url = url + author_id

    response = requests.get(url)
    status_code = response.status_code
    
    if status_code == 200:
        json_response = response.json()
        return(json_response)
    else: return ([])

def getNodeAllAuthors_App2():
    url = 'https://sociallydistributed.herokuapp.com/authors/'

    headers = app2_headers()
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    if status_code == 200:
        json_response = response.json()
        authors = json_response['items']
        return(authors)
    else: return ([])

def checkDisplayName(list, displayName):
    author_list = []
    for item in list:
        if item["displayName"] == displayName:
            author_list.append(item)
    return author_list
    
def getRemoteAuthorsDisplayName(displayName):
    # author1 = checkDisplayName(getNodeAllAuthors_Yoshi(), displayName)
    author2 = checkDisplayName(getNodeAllAuthors_App2(), displayName)
    # author3 = checkDisplayName(getNodeAllAuthors_distro(), displayName) 
    # author4 = checkDisplayName(getNodeAllAuthors_P2(), displayName)
    print(author2)
    authorList = author2
    print(authorList)
    return authorList

def getAuthorId(url):
    arr = url.split("/")
    return arr[-1]

def checkId(list, id):
    author = {}
    found = False
    for item in list:
        item_id = getAuthorId(item["id"])
        if item_id == id:
            author = item
            found = True
    return author, found

def getRemoteAuthorsById(id):

    author2, found = checkId(getNodeAllAuthors_App2(), id)
    if found == False:
        return "author not found", False
    else:
        return author2, True
    
def clean_author(author):
    if type(author) is dict:

        if "type" in author:
            del author["type"]
        if "pronouns" in author:
            del author["pronouns"]
        if "email" in author:
            del author["email"]
        if "about" in author:
            del author["about"]
        if author["github"] is None or author["github"] == 'null':
            author["github"] = ''
        if author["profileImage"] is None or author["profileImage"] == 'null':
            author["github"] = ''
        if "_id" in author:
            author["id"] = author["_id"]
            del author["_id"]
        if 'authorId' in author:
            author["id"] = author["authorId"]
            del author["authorId"]
        author["id"] = author["id"][:-1] if author["id"].endswith('/') else author["id"]
        author["id"] = author["id"].split("/")[-1]
        
        return author