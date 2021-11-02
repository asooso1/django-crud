# Generated by Django 3.2.7 on 2021-10-31 13:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(related_name='follwoings', to=settings.AUTH_USER_MODEL),
        ),
    ]
