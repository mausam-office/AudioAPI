# Generated by Django 4.0 on 2022-09-02 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_audio_is_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='audio_base64_text',
            field=models.TextField(default=''),
        ),
    ]
