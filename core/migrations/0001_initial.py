# Generated by Django 4.0 on 2022-01-03 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(db_index=True, max_length=32, verbose_name='Email address')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
