# Generated by Django 3.2 on 2021-06-13 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_stock_item_current'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock_item',
            name='current1',
            field=models.PositiveIntegerField(default=1),
        ),
    ]