# Generated by Django 2.0.3 on 2018-12-25 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_percent', models.DecimalField(decimal_places=8, max_digits=20)),
                ('total_ques', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user_a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_a_model', to=settings.AUTH_USER_MODEL)),
                ('user_b', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_b_model', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]