from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        # if extra_fields.get('is_superuser') is not True:
        #     raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class User(AbstractBaseUser):
    email = models.EmailField('Email address', db_index=True, max_length=32, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, db_index=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()


class Author(models.Model):
    first_name = models.CharField(max_length=150, db_index=True)
    last_name = models.CharField(max_length=150)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    GENRE_CHOICES = [
        ('WG', 'Without genre'),
        ('BL', 'Business literature'),
        ('DT', 'Detectives and Thrillers'),
        ('NF', 'Nonfiction'),
        ('DR', 'Dramaturgy'),
        ('SE', 'Science and Education'),
    ]

    title = models.CharField('Book title', db_index=True, max_length=128)
    description = models.TextField(null=True, blank=True)
    available = models.BooleanField(default=True, db_index=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, db_index=True)
    genre = models.CharField(max_length=2, choices=GENRE_CHOICES, default='WG', db_index=True)


class Catalog(models.Model):
    title = models.CharField('Book title', db_index=True, max_length=128)
    books = models.ManyToManyField(Book)
