# Generated by Django 4.2 on 2023-04-18 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_tags_order_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
