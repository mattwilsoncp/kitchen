# Generated by Django 2.0.1 on 2018-02-22 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0025_auto_20180222_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='store',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='kitchen.Store'),
        ),
    ]