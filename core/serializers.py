from rest_framework import serializers
from .models import Book, Author, Catalog


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name']


class AuthorShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'full_name']


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]


class BookShortSerializer(serializers.ModelSerializer):
    genre = ChoiceField(choices=Book.GENRE_CHOICES)

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
        fields = ['id', 'title']


class CatalogSerializer(CatalogShortSerializer):
    books = BookShortSerializer(read_only=True, many=True)

    class Meta:
        model = Catalog
        fields = ['id', 'title', 'books']

# class BookToCatalogSerializer
