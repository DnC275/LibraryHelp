from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from .models import Book, Author, Catalog
from .serializers import BookSerializer, AuthorSerializer, BookShortSerializer, CatalogShortSerializer, CatalogSerializer


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


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return BookShortSerializer
        return BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.all()

    def get_serializer_class(self):
        print(self.action)
        if self.action == 'list':
            return CatalogShortSerializer
        return CatalogSerializer

    @action(detail=True, methods=['post'])
    def add_book(self, request, pk=None):
        catalog = self.get_object()
        id = request.data['id']
        catalog.books.add(id)
        catalog.save()
        return Response({'status': 'book added'})





class BookToCatalogViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Catalog.objects.all()

    def update(self, request, *args, **kwargs):
        id = kwargs['pk']
        catalog = Catalog.objects.all(pk=id)
        catalog.books.add(request.data)
