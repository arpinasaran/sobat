# Generated by Django 5.1.2 on 2024-10-24 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_drugentry_availibility'),
    ]

    operations = [
        migrations.AddField(
            model_name='drugentry',
            name='img',
            field=models.ImageField(default='image/no-image/', upload_to='image/'),
        ),
    ]
