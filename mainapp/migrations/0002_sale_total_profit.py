# Generated by Django 3.2 on 2021-07-16 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale_total',
            name='profit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]