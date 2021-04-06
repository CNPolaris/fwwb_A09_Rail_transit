# Generated by Django 3.1.5 on 2021-04-06 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_auto_20210319_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='gitName',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='mail',
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='introduction',
            field=models.TextField(blank=True, max_length=100),
        ),
    ]
