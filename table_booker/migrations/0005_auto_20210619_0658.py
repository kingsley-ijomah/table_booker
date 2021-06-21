# Generated by Django 3.0.8 on 2021-06-19 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('table_booker', '0004_auto_20210619_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='restaurant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='setting', to='table_booker.Restaurant'),
        ),
    ]
