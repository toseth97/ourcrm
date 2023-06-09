# Generated by Django 4.2 on 2023-04-28 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_customer_profile_pix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pix',
            field=models.ImageField(default='default_user.png', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out For Delivery', 'Out For Delivery'), ('Delivered', 'Delivered')], default=('Pending', 'Pending'), max_length=200, null=True),
        ),
    ]
