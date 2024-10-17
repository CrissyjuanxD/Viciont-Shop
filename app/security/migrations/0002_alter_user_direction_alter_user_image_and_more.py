# Generated by Django 4.2 on 2024-07-04 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='direction',
            field=models.CharField(max_length=200, verbose_name='Direccion'),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(max_length=1024, upload_to='users/', verbose_name='Archive image'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=50, verbose_name='Telefono'),
        ),
    ]
