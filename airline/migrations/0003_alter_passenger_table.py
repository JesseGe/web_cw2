# Generated by Django 4.1.7 on 2023-05-09 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("airline", "0002_order_passenger_id_alter_passenger_table"),
    ]

    operations = [
        migrations.AlterModelTable(name="passenger", table="passenger",),
    ]
