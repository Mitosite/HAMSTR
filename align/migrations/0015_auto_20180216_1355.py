# Generated by Django 2.0.2 on 2018-02-16 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('align', '0014_auto_20180216_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pairedjob',
            name='adapters',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pairedjob',
            name='key',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
