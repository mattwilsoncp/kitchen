# Generated by Django 2.0.1 on 2018-02-11 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0015_auto_20180211_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time_units',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cooking_time_unit', to='kitchen.Unit'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='preparation_time_units',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preparation_time_unit', to='kitchen.Unit'),
        ),
    ]