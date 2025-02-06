# Generated by Django 5.1.4 on 2025-01-08 23:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0005_bill_paymenttransaction_servicecharge"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="log",
            options={"ordering": ["-date"]},
        ),
        migrations.AddField(
            model_name="log",
            name="unit_backup",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="log",
            name="action",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="log",
            name="date",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="log",
            name="inventory_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cms.inventory",
            ),
        ),
        migrations.AlterField(
            model_name="log",
            name="supplier_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cms.supplier",
            ),
        ),
    ]
