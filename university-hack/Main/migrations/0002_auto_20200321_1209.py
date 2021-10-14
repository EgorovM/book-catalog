# Generated by Django 3.0.4 on 2020-03-21 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='reviews',
            new_name='review',
        ),
        migrations.AddField(
            model_name='book',
            name='book_link',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.CharField(default='', max_length=100),
        ),
    ]