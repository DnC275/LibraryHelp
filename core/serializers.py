from rest_framework import serializers
from .models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name']


class AuthorShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['full_name']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'author']

    def to_representation(self, instance):
        self.fields['author'] = AuthorShortSerializer(read_only=True)
        return super(BookSerializer, self).to_representation(instance)
