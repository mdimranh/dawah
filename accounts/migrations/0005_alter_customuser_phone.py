# Generated by Django 3.2.3 on 2021-07-04 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, default=None, max_length=20, unique=True, verbose_name='phone'),
        ),
    ]
