# Generated by Django 2.1.7 on 2019-03-28 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outlets', '0002_receipt_register'),
    ]

    operations = [
        migrations.RenameField(
            model_name='register',
            old_name='outlet',
            new_name='assigned_outlet',
        ),
        migrations.RenameField(
            model_name='register',
            old_name='receipt',
            new_name='assigned_receipt',
        ),
    ]
