# Generated by Django 2.1.7 on 2019-05-21 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20190519_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='max_tries',
            field=models.IntegerField(default=3),
        ),
    ]
