from author.basic_auth import BasicAuthenticator
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.shortcuts import get_object_or_404
from .models import Post
from .models import *
from .pagination import CustomCommentPagination
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from social.pagination import CustomPagination
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import base64
from client import *
from .image_renderer import JPEGRenderer, PNGRenderer


custom_parameter = openapi.Parameter(
    name='custom_param',
    in_=openapi.IN_QUERY,
    description='A custom parameter for the POST request',
    type=openapi.TYPE_STRING,
    required=True,
)

response_schema_dictposts = {
    "200": openapi.Response(
        description="Successful Operation",
        examples={
            "application/json": {
    "results": [
        {
            "type": "post",
            "title": "Funny post",
            "id": "5ad63a2b-4890-47b8-bc24-979a96941863",
            "description": "This is a funny joke. Laugh.",
            "contentType": "text/plain",
            "content": "I tried to catch fog the other day, I Mist.",
            "author": {
                "type": "author",
                "id": "866ff975-bb49-4c75-8cc8-10e2a6af44a0",
                "displayName": "Fahad",
                "url": "",
                "profileImage": ""
            },
            "categories": [
                "Funny"
            ],
            "comments": "/comments/",
            "published": "2023-03-03T14:45:41.208691-07:00",
            "visibility": "PUBLIC"
        },
        {
            "type": "post",
            "title": "Sad post",
            "id": "3e227dbd-986f-4f3b-9872-2f81d9c6335f",
            "description": "Sad post,Cry",
            "contentType": "text/plain",
            "content": "Hi this is very sad :(",
            "author": {
                "type": "author",
                "id": "866ff975-bb49-4c75-8cc8-10e2a6af44a0",
                "displayName": "Fahad",
                "url": "",
                "profileImage": ""
            },
            "categories": [
                "Sad"
            ],
            "comments": "/comments/",
            "published": "2023-03-03T14:47:10.782792-07:00",
            "visibility": "PUBLIC"
        }
    ]
}
        }
        
    )}

response_schema_dictpost = {
    "200": openapi.Response(
        description="Successful Operation",
        examples={
            "application/json": {
    "type": "post",
    "title": "Sad post",
    "id": "3e227dbd-986f-4f3b-9872-2f81d9c6335f",
    "description": "Sad post,Cry",
    "contentType": "text/plain",
    "content": "Hi this is very sad :(",
    "author": {
        "type": "author",
        "id": "866ff975-bb49-4c75-8cc8-10e2a6af44a0",
        "displayName": "Fahad",
        "url": "",
        "profileImage": ""
    },
    "categories": [
        "Sad"
    ],
    "comments": "/comments/",
    "published": "2023-03-03T14:47:10.782792-07:00",
    "visibility": "PUBLIC"
}
        }
        
    )}

response_schema_dictdelete = {
    
    "204":openapi.Response(description="Successful Deletion",)}


response_schema_dictComments = {
    "200": openapi.Response(
        description="Successful Operation",
        examples={
            "application/json": [
    {
        "type": "comment",
        "author": {
            "type": "author",
            "id": "866ff975-bb49-4c75-8cc8-10e2a6af44a0",
            "displayName": "Fahad",
            "url": "",
            "profileImage": ""
        },
        "comment": "Wow haha funny dude!",
        "contentType": "text/plain",
        "published": "2023-03-03T15:03:31.309896-07:00",
        "id": "412be771-19bf-4452-9e84-549a52916951"
    }
]
        }
    )}


ObjectsLikedGet = {
    200: openapi.Response(
        description='Sucessfully retrieve Liked objects',
        examples={'application/json': {
  "type": "liked",
  "items": [
    {
      "summary": "TomHardyUpdated Likes your post",
      "type": "Like",
      "author": {
        "type": "author",
        "id": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
        "url": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
        "host": "",
        "displayName": "TomHardyUpdated",
        "github": "",
        "profileImage": ""
      },
      "object": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/c62938df-7b80-481a-bfda-07e768df6561"
    }
  ]
}}
    )
}

PostsGet = {
    "200": openapi.Response(
        description="Successfully retrieved posts",
        examples={
            "application/json": {
  "count": 1,
  "next": 'null',
  "previous": 'null',
  "results": [
    {
      "type": "post",
      "title": "Testing",
      "id": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/c62938df-7b80-481a-bfda-07e768df6561",
      "source": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/c62938df-7b80-481a-bfda-07e768df6561",
      "origin": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/c62938df-7b80-481a-bfda-07e768df6561",
      "description": "Good",
      "contentType": "text/plain",
      "content": "Yes",
      "author": {
        "type": "author",
        "id": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
        "url": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
        "host": "",
        "displayName": "TomHardyUpdated",
        "github": "",
        "profileImage": ""
      },
      "categories": [
        "Hi"
      ],
      "count": 0,
      "comments": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/c62938df-7b80-481a-bfda-07e768df6561/comments/",
      "commentsSrc": [],
      "published": "2023-03-23T15:18:18.709951-07:00",
      "visibility": "PUBLIC"
    }
  ]
}
        }
    )}

PostsPOST = {
    "200": openapi.Response(
        description="Successfully created post",
        examples={
            "application/json": {
  "type": "post",
  "title": "test",
  "id": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece",
  "source": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece",
  "origin": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece",
  "description": "testing testy test",
  "contentType": "text/plain",
  "content": "test",
  "author": {
    "type": "author",
    "id": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
    "url": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
    "host": "",
    "displayName": "TomHardyUpdated",
    "github": "",
    "profileImage": ""
  },
  "categories": [
    ""
  ],
  "count": 0,
  "comments": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece/comments/",
  "commentsSrc": [],
  "published": "2023-03-23T16:39:41.602108-07:00",
  "visibility": "PUBLIC"
}
        }
    )}

IndividualPOSTGet = {
    "200": openapi.Response(
        description="Successfully Retrieved individual post",
        examples={
            "application/json": {
  "type": "post",
  "title": "test",
  "id": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece",
  "source": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece",
  "origin": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece",
  "description": "testing testy test",
  "contentType": "text/plain",
  "content": "test",
  "author": {
    "type": "author",
    "id": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
    "url": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
    "host": "",
    "displayName": "TomHardyUpdated",
    "github": "",
    "profileImage": ""
  },
  "categories": [
    ""
  ],
  "count": 0,
  "comments": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece/comments/",
  "commentsSrc": [],
  "published": "2023-03-23T16:39:41.602108-07:00",
  "visibility": "PUBLIC"
}
        }
    )}

IndividualPOSTPost = {
    "200": openapi.Response(
        description="Successfully Updated individual post",
        examples={
            "application/json": {
  "type": "post",
  "title": "Updated POST!!!",
  "id": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece",
  "source": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece",
  "origin": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece",
  "description": "testing testy test",
  "contentType": "text/plain",
  "content": "test",
  "author": {
    "type": "author",
    "id": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
    "url": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
    "host": "",
    "displayName": "TomHardyUpdated",
    "github": "",
    "profileImage": ""
  },
  "categories": [
    ""
  ],
  "count": 0,
  "comments": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece/comments/",
  "commentsSrc": [],
  "published": "2023-03-23T16:39:41.602108-07:00",
  "visibility": "PUBLIC"
}
        }
    )}

CreateComment = {
    "200": openapi.Response(
        description="Successfully Created comment",
        examples={
            "application/json": {
  "type": "comment",
  "author": {
    "type": "author",
    "id": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
    "url": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
    "host": "",
    "displayName": "LaraCroft",
    "github": "",
    "profileImage": ""
  },
  "comment": "hi",
  "contentType": "text/plain",
  "published": "2023-03-23T17:04:10.945180-07:00",
  "id": "http://127.0.0.1:8000/posts/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6/posts/2aa56a61-85df-4dee-8b00-7c2cabf2b161/comments/c5c03638-47ce-412f-b23c-d785c2ea7525"
}
        }
    )}


GetComments = {
    "200": openapi.Response(
        description="Successfully Retrieve comment",
        examples={
            "application/json": {
  "count": 1,
  "next": 'null',
  "previous": 'null',
  "results": [
    {
      "type": "comment",
      "author": {
        "type": "author",
        "id": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
        "url": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
        "host": "",
        "displayName": "LaraCroft",
        "github": "",
        "profileImage": ""
      },
      "comment": "hi",
      "contentType": "text/plain",
      "published": "2023-03-23T17:04:10.945180-07:00",
      "id": "http://127.0.0.1:8000/posts/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6/posts/2aa56a61-85df-4dee-8b00-7c2cabf2b161/comments/c5c03638-47ce-412f-b23c-d785c2ea7525"
    }
  ]
}
        }
    )}


GetCommentLikes =  {
    "200": openapi.Response(
        description="Successfully Retrieve comment likes",
        examples={
            "application/json": [
  {
    "summary": "TomHardyUpdated Likes your comment",
    "type": "Like",
    "author": {
      "type": "author",
      "id": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
      "url": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
      "host": "",
      "displayName": "TomHardyUpdated",
      "github": "",
      "profileImage": ""
    },
    "object": "http://127.0.0.1:8000/posts/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6/posts/2aa56a61-85df-4dee-8b00-7c2cabf2b161/comments/c5c03638-47ce-412f-b23c-d785c2ea7525"
  }
]
        }
    )}




GetInvdividualComment = {
    "200": openapi.Response(
        description="Successfully Retrieved comments",
        examples={
            "application/json": {
  "type": "comment",
  "author": {
    "type": "author",
    "id": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
    "url": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
    "host": "",
    "displayName": "LaraCroft",
    "github": "",
    "profileImage": ""
  },
  "comment": "hi",
  "contentType": "text/plain",
  "published": "2023-03-23T17:04:10.945180-07:00",
  "id": "http://127.0.0.1:8000/posts/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6/posts/2aa56a61-85df-4dee-8b00-7c2cabf2b161/comments/c5c03638-47ce-412f-b23c-d785c2ea7525"
}
        }
    )}


PostLikes = {
    "200": openapi.Response(
        description="Successfully Retrieved Likes on a post",
        examples={
            "application/json": [
  {
    "summary": "LaraCroft Likes your post",
    "type": "Like",
    "author": {
      "type": "author",
      "id": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
      "url": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
      "host": "",
      "displayName": "LaraCroft",
      "github": "",
      "profileImage": ""
    },
    "object": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/c62938df-7b80-481a-bfda-07e768df6561"
  },
  {
    "summary": "TomHardyUpdated Likes your post",
    "type": "Like",
    "author": {
      "type": "author",
      "id": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
      "url": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
      "host": "",
      "displayName": "TomHardyUpdated",
      "github": "",
      "profileImage": ""
    },
    "object": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/c62938df-7b80-481a-bfda-07e768df6561"
  }
]
        }

    )}

Publicpostget = {
    "200": openapi.Response(
        description="Successfully Retrieved All public posts",
        examples={
            "application/json":{
    "id": "https://social-distro.herokuapp.com/authors/team24/posts/helloworld",
    "title": "Hello World!",
    "source": 'null',
    "origin": 'null',
    "description": "Our first post",
    "contentType": "text/plain",
    "content": "Hello from team 24!",
    "categories": [],
    "published": "2023-03-24T17:53:09.628104Z",
    "visibility": "PUBLIC",
    "unlisted": 'false',
    "author_id": "https://social-distro.herokuapp.com/authors/team24"
  }

        }

    )}

class post_list(APIView, PageNumberPagination):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = CustomPagination

    # ref: https://auganrymkhan.com/tutorial/implementing-a-custom-configured-pagination-in-django-rest-framework-using-listapiview-and-apiview
    @property
    def paginator(self):
        """The paginator instance associated with the view, or `None`."""
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator
    
    @swagger_auto_schema(responses =PostsGet, operation_summary="List all Posts for an Author")
    def get(self, request, pk_a):
        """
        Get the list of posts on our website
        """
        author = Author.objects.get(id=pk_a)
        
        # filter the posts and then paginate
        # privacy is all handled when post is created, except for image posts

        posts = Post.objects.filter(author=author)
        posts = self.paginator.paginate_queryset(posts, self.request, view=self)

        serializer = PostSerializer(posts, many=True)
        
        return self.paginator.get_paginated_response(serializer.data, "posts")

    @swagger_auto_schema(responses = PostsPOST, operation_summary="Create a new Post for an Author",request_body=openapi.Schema( type=openapi.TYPE_STRING,description='A raw text input for the POST request',example = {
     "type":"post",
     "title":"test",
     "description":"testing testy test",
     "contentType":"text/plain",
     "content":"test"
}))
    def post(self, request, pk_a):
        """
        New post for an Author
        Request: include mandatory fields of a post, not including author, id, origin, source, type, count, comments, commentsSrc, published
        """
        pk = str(uuid.uuid4())
        try:
            author = Author.objects.get(pk=pk_a)
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)

        # handle an image post
        if 'image' in request.data['contentType']:
            # format is similar to post: a JSON object with: { title, contentType, content, image }
            # image is passed in as a base64 string. it should look like data:image/png;base64,LOTSOFLETTERS
            # the image serializer saves the base64 image into the database as an actual image file
            serializer = ImageSerializer(data=request.data, context={'author_id': pk_a, 'id':pk})
        # otherwise, handle as normal post
        else:
            serializer = PostSerializer(data=request.data, context={'author_id': pk_a, 'id':pk})

        # save post if valid
        if serializer.is_valid():
            post = serializer.save()
            # pass in the shared authors on post creation and share to other users' inboxes
            share_object(post,author,request.data['authors'])
            return Response(serializer.data, status=status.HTTP_200_OK)
        # 400 on incorrect serializer data
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]    
    @swagger_auto_schema(responses = GetInvdividualComment, operation_summary="List specific comment")
    def get(self, request, pk_a, pk, pk_m):
        """
        Get the specific comment
        """
        try:
            # get a specific comment 
            comment = Comment.objects.get(id=pk_m)
            serializer = CommentSerializer(comment, many=False)
            return Response(serializer.data)
        # 404 if comment doesn't exist
        except Comment.DoesNotExist: 
            error_msg = "Comment not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        
class post_detail(APIView, PageNumberPagination):

    @swagger_auto_schema(responses = IndividualPOSTGet, operation_summary="Get a particular post of an author")
    def get(self, request, pk_a, pk):
        """
        Get a particular post of an author
        """
        try: 
            # try to get the post of this author
            post = Post.objects.get(id = pk)
            authenticated_user = Author.objects.get(id=pk_a)

        except Post.DoesNotExist: 
            # post is not found, so 404
            error_msg = "Post not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)

        if "image/" in post.contentType:
            serializer = ImageSerializer(post)
        else:
            serializer = PostSerializer(post)

        return Response(serializer.data)
    
    #content for creating a new post object
    #{
    # Title, Description, Content type, Content, Categories, Visibility
    # }
    @swagger_auto_schema(responses = IndividualPOSTPost, operation_summary="Update a particular post of an author",request_body=openapi.Schema( type=openapi.TYPE_STRING,description='A raw text input for the POST request',example = {"title":"Updated POST!!!"}))
    def post(self, request, pk_a, pk):       
        """
        Request: only include fields you want to update, not including id or author.
        """     
        # try-except for getting author and post. if either doesn't exist, return 404
        try:
            _ = Author.objects.get(pk=pk_a)
        except Author.DoesNotExist:
            error_msg = "Author not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            error_msg = "Post not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        
        # TODO: FIX AFTER SLASH
        # if post is from this service:
        if post.url == post.origin:
            # if the author is not our guy
            if post.author != _:
                return Response("Cannot edit a post you didnt create", status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
            # handle editing for image post
            if 'image' in request.data['contentType']:
                serializer = ImageSerializer(data=request.data, context={'author_id': pk_a}) 
            # otherwise handle for normal post
            else:
                serializer = PostSerializer(post, data=request.data, partial=True)

            # looking good?    
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            # 400 if the data is not, in fact, looking good
            else: 
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
        # commenting out what seems to be a redundancy
        #serializer = PostSerializer(post, data=request.data, partial=True)
        #if serializer.is_valid():
        #    serializer.save()
        #    return Response(serializer.data)
        # above is old code, should be fine to remove
        # 400 if the post is not from us
        else:
            return Response("Cannot edit a shared post", status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Delete a particular post of an author") 
    def delete(self, request, pk_a, pk):
        """
        Deletes the post given by the particular authorid and postid
        """
        # TODO: check permissions 
        
        # yo dawg we heard you like try-excepts so we put a try-except in your try-except so you
        # can try-except while you try-except
        # try-except for the try-excepts (try if the post exists, 404 if not)
        try: 
            # try-except for checking if the author is real (404 if the accident was not your fault)
            try:
                author = Author.objects.get(id=pk_a)
            except:
                error_msg = "Author not found"
                return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
            # try-except for checking if the post exists (404 if not)
            try:
                post = Post.objects.get(id=pk)
            except:
                error_msg = "Post not found"
                return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
            if post.author != author:
                # if the post author isn't the current author, 405 because this isn't your property
                return Response("Cannot delete a post you dont own", status=status.HTTP_405_METHOD_NOT_ALLOWED)
            post.delete()
            # 204 on deletion 
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Post.DoesNotExist:
            return Response("Post does not exist",status=status.HTTP_404_NOT_FOUND)
      

    @swagger_auto_schema(responses =PostsPOST, operation_summary="Create a post of an author whose id is the specified post id",request_body=openapi.Schema( type=openapi.TYPE_STRING,description='A raw text input for the PUT request',example = {
  "type": "post",
  "title": "test2",
  "description": "testing testy test",
  "contentType": "text/plain",
  "content": "test"
})) 
    def put(self, request, pk_a, pk):
        """
        Request: include mandatory fields of a post, not including author, id, origin, source, type, count, comments, commentsSrc, published
        """
        # try-excepts for getting author and post.
        try:
            author = Author.objects.get(id=pk_a)
            try:
                _ = Post.objects.get(id=pk)
                # 400 if post already exists
                return Response("Post already exists", status=status.HTTP_400_BAD_REQUEST)
            except Post.DoesNotExist:
                # continue to the function if the post does not exist (create the post)
                pass
        except Author.DoesNotExist:
            # 404 if author doesn't exist
            Response("Author does not exist", status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(data=request.data, context={'author_id': pk_a, 'id':pk})
        # if the serializer is good, save the serializer and send the post to all inboxes
        if serializer.is_valid():
            post = serializer.save()
            share_object(post,author,[])
            return Response(serializer.data)
        # 400 if the serializer has errors
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikedView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    # TODO: RESPONSE AND REQUESTS
    
    @swagger_auto_schema(responses = ObjectsLikedGet, operation_summary="List all objects liked by author")
    def get(self, request, pk_a):
        """
        Get the liked objects by author
        TODO: make sure objects are public
        """
        # check if author exists, 404 if not
        try:
            author = Author.objects.get(pk=pk_a)
        except Author.DoesNotExist:
            error_msg = "Author not found"
            return Response(error_msg,status=status.HTTP_404_NOT_FOUND)
        # filter out all liked objects by author
        likes = Like.objects.filter(author=author)
        serializer = LikeSerializer(likes, many=True)
        data = self.get_items(pk_a, serializer.data)
        # return all liked objects
        return Response(data)
    
    def get_items(self,pk_a,data):
        # helper function 
        
        dict = {"type":"liked" }
        items = []
        for item in data:
            items.append(item)

        dict["items"] = items
        return(dict) 
    
class CommentLikesView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    """
    Get the list of likes on our comments
    """
    @swagger_auto_schema(responses=GetCommentLikes,operation_summary="List all likes on a comment")
    def get(self, request, pk_a, pk, pk_m):
        # try to get a comment, 404 if does not exist 
        try:
            comment = Comment.objects.get(id=pk_m)
        except Comment.DoesNotExist:
            error_msg = "Comment not found"
            return Response(error_msg,status=status.HTTP_404_NOT_FOUND)
        # get the likes on that comment
        likes = Like.objects.filter(object=comment.url)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

class PostLikesView(APIView):
    @swagger_auto_schema(operation_summary="Get the likes on a post")
    @authentication_classes([BasicAuthentication])
    @permission_classes([IsAuthenticated])
    def get(self, request, pk_a, pk):
        """
        Get the list of likes on a post
        """
        # safety try-except
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            error_msg = "Post not found"
            return Response(error_msg,status=status.HTTP_404_NOT_FOUND)
        # filter for all the likes on that post
        url = post.url[:-1] if post.url.endswith('/') else post.url
        likes = Like.objects.filter(object=url)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

# specifically for displaying image from the path authors/<str:pk_a>/posts/<str:pk>/image/
class ImageView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    # a renderer for displaying the image
    renderer_classes = [JPEGRenderer, PNGRenderer]

    def get(self, request, pk_a, pk):
        
        try:
            author = Author.objects.get(id=pk_a) 
            post = Post.objects.get(author=author, id=pk)
            # TODO: refactor with auth
            authenticated_user = Author.objects.get(id=pk_a)
        except Post.DoesNotExist:
            error_msg = {"message":"Post does not exist!"}
            return Response(error_msg,status=status.HTTP_404_NOT_FOUND)

        # if the post is not an image post, return a 404
        if post.contentType and 'image' not in post.contentType:
            error_msg = {"message":"Post does not contain an image!"}
            return Response(error_msg,status=status.HTTP_404_NOT_FOUND)

        # if there is no image included in an image post, return a 404
        if not post.image:
            error_msg = {"message":"Post does not contain an image!"}
            return Response(error_msg,status=status.HTTP_404_NOT_FOUND)
        
        # image privacy protection settings
        # unlisted does not need to be addressed here
        # if it is private or friends, only continue if author is trying to access it:
        if "PRIVATE" in post.visibility:
            # check if the author is not the one accessing it, return a 403 if not:
            if post.author != authenticated_user:
                error_msg = {"message":"You do not have access to this image!"}
                return Response(error_msg,status=status.HTTP_403_FORBIDDEN)

        # otherwise, handle it for friends:
        elif "FRIENDS" in post.visibility:
            # if the author or friends are trying to access it, return a 403 if not:
            if post.author not in authenticated_user.friends and post.author != authenticated_user:
                error_msg = {"message":"You do not have access to this image!"}
                return Response(error_msg,status=status.HTTP_403_FORBIDDEN)

        # return the image!
        # post.image refers to an image in the database 
        post_content = post.contentType.split(';')[0]
        return Response(post.image, content_type=post_content, status=status.HTTP_200_OK)

class CommentView(APIView, PageNumberPagination):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    pagination_class = CustomCommentPagination

    # ref: https://auganrymkhan.com/tutorial/implementing-a-custom-configured-pagination-in-django-rest-framework-using-listapiview-and-apiview
    @property
    def paginator(self):
        """The paginator instance associated with the view, or `None`."""
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator
    
    @swagger_auto_schema(responses = GetComments, operation_summary="List all Comments on a post")
    def get(self, request, pk_a, pk):
        try:
            author = Author.objects.get(id=pk_a)
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        
        post = Post.objects.get(id=pk)
        post_data = PostSerializer(post).data
        # filter for all comments on specific post
        comments = Comment.objects.filter(post=post_data['source']) #Changed cause i changed the comment model , post is now the source url of the post, not the post object, done to match with spec
   
        authenticated_user = Author.objects.get(id=pk_a)
        
        # on private posts, friends' comments will only be available to me.
        if "PRIVATE" in post.visibility:
            # so here, when authed user != author, the comments of the friends
            # of the author are filtered out
            if post.author != authenticated_user:
                comments = comments.exclude(author=post.author.friends)
        
        comments_page = self.paginator.paginate_queryset(comments, self.request, view=self)
        serializer = CommentSerializer(comments_page, many=True)
        response = self.paginator.get_paginated_response(serializer.data, post_data['id'], post_data['comments'])
        return response


    @swagger_auto_schema(responses = CreateComment, operation_summary="Create a comment on the post", request_body=openapi.Schema( type=openapi.TYPE_STRING,description='A raw text input for the PUT request', example = {"author_id" : "cfd9d228-44df-4a95-836f-c0cb050c7ad6", "comment": "hi"}))
    def post(self, request,pk_a, pk):
        comment_id = uuid.uuid4()
        # try to get the author, return 404 if ID doesn't exist
        try:
            author = Author.objects.get(pk=pk_a)
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        # try to get the post, return 404 if ID doesn't exist
        try: 
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            error_msg = "Post id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        
        # serialize the comment
        serializer = CommentSerializer(data=request.data, context={"post":post,"id":comment_id, 'author_id':request.data["author_id"]}, partial=True)
        # check serializer
        if serializer.is_valid():
            comment = serializer.save()
            inbox_item = Inbox(content_object=comment, author=post.author)
            inbox_item.save()
            return Response(serializer.data)
        # serializer failure
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# post to url 'authors/<str:origin_author>/posts/<str:post_id>/share/<str:author>'

class ShareView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, origin_author, post_id, author):       
        
        # try to get the author, return 404 if ID doesn't exist
        try:
            sharing_author = Author.objects.get(pk=author)
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        
        # try to get the post, return 404 if ID doesn't exist
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            error_msg = "Post id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        

        # create new post object with different author but same origin
        # new URL 
        current_url = post.get_absolute_url()
        source = current_url.split('share')[0]
        origin = post.origin
        
        new_post = Post(
        title=post.title,
        description=post.description,
        content=post.content,
        contentType=post.contentType,
        author=sharing_author,
        categories=post.categories,
        published=post.published,
        visibility=post.visibility,
        )

        # update the source and origin fields
        new_post.source = source
        new_post.origin = origin

        # save the new post
        new_post.save()
        # this shared_user here is blank
        share_object(new_post,sharing_author,[])
        # serialize post
        if "image/" in new_post.contentType:
            serializer = ImageSerializer(new_post)
        else:
            serializer = PostSerializer(new_post)
        return Response(serializer.data)
    
class PublicPostsView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses =Publicpostget, operation_summary="List all Public posts on all servers")
    def get(self, request):
        posts = Post.objects.filter(visibility='PUBLIC')
        serializer = PostSerializer(posts, many=True)
        data_list = serializer.data
        if (request.GET.get("local") == "true") :
            remotePosts = getAllPublicPosts()
            data_list = data_list + remotePosts
            data_list.sort(key=lambda x: x['published'])
        return Response(data_list)  
        
        
# share a post to an inbox
def share_object(item, author, shared_user):
    inbox_item = Inbox(content_object=item, author=author)
    inbox_item.save()

    # friend post (send to friend inbox)
    if (item.visibility == 'FRIENDS'):
        for friend in author.friends.all():
            inbox_item = Inbox(content_object=item, author=friend)
            inbox_item.save()

    # unlisted post (send only to own inbox)
    elif (item.visibility == 'UNLISTED'):
        if author:
            inbox_item = Inbox(content_object=item, author=author)
            inbox_item.save()

    # private post (send to shared users' inbox)
    elif (item.visibility == 'PRIVATE'):
        for id in shared_user:
            share = Author.objects.get(id=id)
            inbox_item = Inbox(content_object=item, author=share)
            inbox_item.save()
