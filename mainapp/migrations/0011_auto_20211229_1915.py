# Generated by Django 3.2.6 on 2021-12-29 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_alter_sale_total_sold_att'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale_total',
            name='sold_att',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='stock_total',
            name='added_at',
            field=models.DateField(),
        ),
    ]
