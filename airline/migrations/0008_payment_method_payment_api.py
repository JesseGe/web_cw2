# Generated by Django 4.1.7 on 2023-05-10 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("airline", "0007_alter_order_ticket_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment_method",
            name="payment_api",
            field=models.CharField(max_length=200, null=True),
        ),
    ]