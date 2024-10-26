# Generated by Django 5.1 on 2024-10-26 15:21

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0012_alter_drugentry_options_alter_drugentry_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_available', models.BooleanField(default=True)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('selling_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_products', to='product.drugentry')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ShopProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='shop_profiles/')),
                ('address', models.TextField()),
                ('opening_time', models.TimeField()),
                ('closing_time', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shops', to=settings.AUTH_USER_MODEL)),
                ('products', models.ManyToManyField(through='shop.ShopProduct', to='product.drugentry')),
            ],
        ),
        migrations.AddField(
            model_name='shopproduct',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_products', to='shop.shopprofile'),
        ),
        migrations.AlterUniqueTogether(
            name='shopproduct',
            unique_together={('shop', 'product')},
        ),
    ]
