# Generated by Django 3.2.6 on 2022-04-04 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upserve', '0002_auto_20220404_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserve',
            name='pending',
            field=models.BooleanField(default=False),
        ),
    ]
