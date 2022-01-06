from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from rest_framework import viewsets, filters
from .models import Book, Author, Catalog
from .serializers import BookSerializer, AuthorSerializer, BookShortSerializer, CatalogShortSerializer, \
    CatalogSerializer
from django_filters.rest_framework import DjangoFilterBackend


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
def get_genres(request):
    response = {}
    for key, value in Book.GENRE_CHOICES:
        response[key] = value
    return Response(response, status=HTTP_200_OK)


class BookViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['genre', 'author']
    search_fields = ['title']

    def get_serializer_class(self):
        if self.action == 'list':
            return BookShortSerializer
        return BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        # genre = self.request.query_params.get('genre')
        # if genre is not None:
        #     queryset = queryset.filter(genre=genre)
        # author_id = self.request.query_params.get('author')
        # if author_id is not None:
        #     queryset = queryset.filter(author__id=author_id)
        # author_id = self.request.query_params.get('author')
        # if author_id is not None:
        #     queryset = queryset.filter(author__id=author_id)
        return queryset


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.all()

    ADD = 'ADD'
    DEL = 'DEL'

    def get_serializer_class(self):
        print(self.action)
        if self.action == 'list':
            return CatalogShortSerializer
        return CatalogSerializer

    def catalog_action(self, request, action):
        catalog = self.get_object()
        id = request.data['id']
        if id is None:
            return Response('Book id is not specified')
        if action == self.ADD:
            catalog.books.add(id)
            response = {'status': 'book added'}
        elif action == self.DEL:
            catalog.books.remove(id)
            response = {'status': 'book removed'}
        catalog.save()
        return Response(response)

    @action(detail=True, methods=['post'])
    def add_book(self, request, pk=None):
        action = self.ADD
        print(pk)
        return self.catalog_action(request, action)

    @action(detail=True, methods=['post'])
    def delete_book(self, request, pk=None):
        action = self.DEL
        return self.catalog_action(request, action)


