# Generated by Django 4.1.4 on 2023-01-13 05:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['created']},
        ),
    ]
