# Generated by Django 2.1.7 on 2019-03-21 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=244)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=244, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Outlet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=244)),
                ('address_line1', models.CharField(max_length=244)),
                ('address_line2', models.CharField(max_length=244)),
                ('lga', models.CharField(max_length=244)),
                ('phone_number', models.CharField(max_length=25)),
                ('date_launched', models.DateField()),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.Business')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='outlets.City')),
            ],
        ),
        migrations.CreateModel(
            name='OutletKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=244)),
            ],
        ),
        migrations.AddField(
            model_name='outlet',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='outlets.OutletKind'),
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='outlets.Country'),
        ),
        migrations.AlterUniqueTogether(
            name='outlet',
            unique_together={('name', 'business')},
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together={('name', 'country')},
        ),
    ]