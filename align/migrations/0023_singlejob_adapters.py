# Generated by Django 2.0.2 on 2018-02-20 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('align', '0022_pairedjob_singlejob'),
    ]

    operations = [
        migrations.AddField(
            model_name='singlejob',
            name='adapters',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
