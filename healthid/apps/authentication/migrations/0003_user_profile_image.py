# Generated by Django 2.1.7 on 2019-04-03 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20190322_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
