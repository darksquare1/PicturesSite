# Generated by Django 4.2.7 on 2023-11-09 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('njp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pic',
            name='photo_thumb_nail',
            field=models.ImageField(blank=True, upload_to='users/thumbs/%Y/%m/%d/', verbose_name='thumbnail'),
        ),
    ]