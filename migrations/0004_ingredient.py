# Generated by Django 2.0.1 on 2018-01-31 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0003_auto_20180121_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('generic_name', models.CharField(max_length=100)),
                ('barcode', models.CharField(max_length=100)),
            ],
        ),
    ]
