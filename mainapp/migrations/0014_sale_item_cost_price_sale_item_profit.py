# Generated by Django 4.0.5 on 2022-06-19 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_delete_return_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale_item',
            name='cost_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='sale_item',
            name='profit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
