# Generated by Django 3.1.5 on 2021-03-19 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_profile_online'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='online',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]