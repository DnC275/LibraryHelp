# Generated by Django 3.2.7 on 2022-01-05 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20220104_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='first_name',
            field=models.CharField(db_index=True, max_length=150),
        ),
    ]
