# Generated by Django 2.0.1 on 2018-02-19 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0023_auto_20180217_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='site_permission',
            field=models.BooleanField(default=False),
        ),
    ]