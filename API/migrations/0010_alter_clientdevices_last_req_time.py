# Generated by Django 4.0 on 2022-09-05 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0009_clientdevices_last_req_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientdevices',
            name='last_req_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
