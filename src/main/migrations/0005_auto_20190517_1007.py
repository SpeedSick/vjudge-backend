# Generated by Django 2.1.7 on 2019-05-17 10:07

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_auto_20190517_0810'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='courseparticipant',
            unique_together={('student', 'course')},
        ),
    ]