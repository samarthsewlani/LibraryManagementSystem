# Generated by Django 3.0.4 on 2020-05-03 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_booktype_publication_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='booktype',
            name='pub_date',
            field=models.CharField(default='2000-01-01', max_length=10),
        ),
    ]
