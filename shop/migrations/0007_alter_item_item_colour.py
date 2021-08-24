# Generated by Django 3.2.5 on 2021-08-21 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_item_item_colour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_colour',
            field=models.CharField(blank=True, choices=[('FA', 'False'), ('BL', 'Black'), ('PK', 'Pink'), ('RD', 'Red'), ('BL', 'Blue'), ('GR', 'Green')], max_length=2, null=True),
        ),
    ]