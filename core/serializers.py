from rest_framework import serializers
from .models import Book, Author, Catalog
from rest_framework.fields import empty
from django.core.exceptions import ValidationError

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'books_count']


class AuthorShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'full_name', 'books_count']


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]


class BookShortSerializer(serializers.ModelSerializer):
    genre = ChoiceField(choices=Book.GENRE_CHOICES, required=False)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre']

    def to_representation(self, instance):
        self.fields['author'] = AuthorShortSerializer(read_only=True)
        return super(BookShortSerializer, self).to_representation(instance)


class BookSerializer(BookShortSerializer):

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'author', 'genre', 'publication_year']


class CatalogShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ['id', 'title', 'books_count']


class CatalogSerializer(CatalogShortSerializer):
    books = BookShortSerializer(many=True, read_only=True)

    class Meta:
        model = Catalog
        fields = ['id', 'title', 'books']
        
    def run_validation(self, data=empty):
        book_ids = data.pop('books', None)
        data = super(CatalogSerializer, self).run_validation(data)
        if book_ids:
            for id in book_ids:
                if type(id) != int:
                    raise ValidationError(message="Id not int")
                exist = Book.objects.filter(id=id).exists()
                if not exist:
                    raise ValidationError(message=f'Book with id %d does not exist' % id)
        data['books'] = book_ids
        return data

    def create(self, validated_data):
        books = validated_data.pop('books', None)
        instance = super(CatalogSerializer, self).create(validated_data)
        if books:
            for id in books:
                instance.books.add(id)
        return instance

    def update(self, instance, validated_data):
        books = validated_data.pop('books', None)
        instance = super(CatalogSerializer, self).update(instance, validated_data)
        if books:
            instance.books.clear()
            for id in books:
                instance.books.add(id)
        return instance


