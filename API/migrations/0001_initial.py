# Generated by Django 4.0 on 2022-08-31 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=150)),
                ('audio_base64', models.CharField(max_length=130000)),
            ],
        ),
    ]
