# Generated by Django 2.0.1 on 2018-02-17 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0018_auto_20180216_1750'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='unit',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipe_url',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]