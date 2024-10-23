# Generated by Django 5.1.2 on 2024-10-23 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('desc', models.TextField()),
                ('disease', models.CharField(max_length=63)),
                ('drug_type', models.CharField(max_length=31)),
                ('drug_form', models.CharField(max_length=31)),
                ('price', models.IntegerField()),
                ('stock', models.IntegerField()),
                ('age_range', models.IntegerField()),
            ],
        ),
    ]
