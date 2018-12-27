# Generated by Django 2.0.3 on 2018-12-27 18:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlike',
            name='liked_user',
            field=models.ManyToManyField(blank=True, related_name='liked_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
