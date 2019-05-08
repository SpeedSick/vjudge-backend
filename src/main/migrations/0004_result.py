# Generated by Django 2.1.7 on 2019-05-03 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20190503_0734'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='main.Submission')),
            ],
        ),
    ]