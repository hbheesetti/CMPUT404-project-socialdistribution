import requests
import base64
from rest_framework.response import Response
from rest_framework import status
from author.models import *

def getNodeAuthor_social_distro(author_id):
    url = 'https://social-distro.herokuapp.com/api/authors/'
    username = 'team24'
    password = 'team24'
    url = url + author_id + '/'

    credentials = f'{username}:{password}'
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    authorization_header = f'Basic {encoded_credentials}'
    headers = {'Authorization': authorization_header}

    response = requests.get(url, headers=headers)

    status_code = response.status_code
   

    if status_code == 200:
        json_response = response.json()
        return(json_response, status_code)
    else: return (None, status_code)


def getNodeAuthor_Yoshi(author_id):
    url = 'https://yoshi-connect.herokuapp.com/authors/'

    url = url + author_id

    response = requests.get(url)
    status_code = response.status_code
    
    if status_code == 200:
        json_response = response.json()
        return(json_response, status_code)
    else: return (None, status_code)

def getNodeAuthor_App2(author_id):
    url = 'https://killme.herokuapp.com/authors/'

    url = url + author_id

    print("in node 2 authors")

    response = requests.get(url)
    status_code = response.status_code
    
    if status_code == 200:
        json_response = response.json()
        return(json_response, status_code)
    else: return (None, status_code)

def getNodeAllAuthors_Yoshi():
    url = 'https://yoshi-connect.herokuapp.com/authors'
    response = requests.get(url)
    status_code = response.status_code
    json_response = response.json()
    authors = json_response['items']
    return authors

def getNodeAllAuthors_App2():
    url = 'https://killme.herokuapp.com/authors/'
    hosturl = "https://killme.herokuapp.com/"

    username = 'app1team15'
    password = 'hari1234'

    session = requests.Session()
    session.auth = (username, password)

    auth = session.post(hosturl)
    response = session.get(url)

    json_response = response.json()
    authors = json_response['data']
    return authors

def getNodeAllAuthors_distro():
    url = 'https://social-distro.herokuapp.com/api/authors/'

    username = 'team24'
    password = 'team24'
    #remote1:r3mot31
    credentials = f'{username}:{password}'
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    authorization_header = f'Basic {encoded_credentials}'
    headers = {'Authorization': authorization_header}

    response = requests.get(url, headers=headers)
   
    status_code = response.status_code
    json_response = response.json()
    authors = json_response['results']
    return authors


def checkDisplayName(list, displayName):
    author_list = []
    for item in list:
        if item["displayName"] == displayName:
            author_list.append(item)
    return author_list
    
def getRemoteAuthorsDisplayName(displayName):
    author1 = checkDisplayName(getNodeAllAuthors_Yoshi(), displayName)
    author2 = checkDisplayName(getNodeAllAuthors_App2(), displayName)
    author3 = checkDisplayName(getNodeAllAuthors_distro(), displayName)
    authorList = author1 + author2 + author3
    return authorList



def check_author(author_id):
    '''Checks if the author exists on any of our remote connections'''
    response1, code1 = getNodeAuthor_Yoshi(author_id)
    response2, code2 = getNodeAuthor_social_distro(author_id)
    if code1 == 200:
        return response1, code1
    if code2 == 200:
        return response2, code2
    

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
        return author
    


def getRemoteAuthorsById(id):
    author1, found = checkId(getNodeAllAuthors_Yoshi(), id)
    if found == False:
        author2, found = checkId(getNodeAllAuthors_App2(), id)
        if found == False:
            author3, found = checkId(getNodeAllAuthors_distro(), id)
            if found == False:
                return "author not found", False
            else:
                return author3, True
        else:
            return author2, True
    else:
        return author1, True

def checkId(list, id):
    author = {}
    found = False
    for item in list:
        item_id = getAuthorId(item["id"])
        if item_id == id:
            author = item
            found = True
    return author, found

def getAuthorId(url):
    arr = url.split("/")
    return arr[-1]
