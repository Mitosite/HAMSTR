# Generated by Django 2.0.2 on 2018-02-23 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('align', '0028_auto_20180223_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfile',
            name='randkey',
            field=models.CharField(default='0000000000', max_length=101),
        ),
    ]
