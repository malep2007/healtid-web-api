# Generated by Django 2.1.7 on 2019-07-02 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('preference', '0006_auto_20190702_1010'),
        ('outlets', '0006_remove_outlet_preference'),
    ]

    operations = [
        migrations.AddField(
            model_name='outlet',
            name='preference',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='preference.OutletPreference'),
        ),
        migrations.AlterField(
            model_name='outlet',
            name='prefix_id',
            field=models.CharField(max_length=50),
        ),
    ]
