# Generated by Django 2.1.7 on 2019-05-02 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('outlets', '0004_outlet_preference'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovedDeliveryFormat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConsultantRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consultation_name', models.CharField(max_length=80)),
                ('description', models.CharField(max_length=100)),
                ('price_per_session', models.IntegerField()),
                ('approved_delivery_formats', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultation.ApprovedDeliveryFormat')),
                ('consultant_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultation.ConsultantRole')),
            ],
        ),
        migrations.CreateModel(
            name='ExpectedTimeDuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='consultation',
            name='expected_time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultation.ExpectedTimeDuration'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='outlet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='outlets.Outlet'),
        ),
        migrations.AlterUniqueTogether(
            name='consultation',
            unique_together={('consultation_name', 'approved_delivery_formats', 'expected_time')},
        ),
    ]
