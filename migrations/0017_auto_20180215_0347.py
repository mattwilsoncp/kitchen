# Generated by Django 2.0.1 on 2018-02-15 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0016_auto_20180211_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='recipe_photo',
            field=models.FileField(blank=True, upload_to='recipe_photos/'),
        ),
    ]