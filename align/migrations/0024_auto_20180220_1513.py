# Generated by Django 2.0.2 on 2018-02-20 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('align', '0023_singlejob_adapters'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pairedjob',
            old_name='adapters',
            new_name='adapter',
        ),
        migrations.RemoveField(
            model_name='singlejob',
            name='adapters',
        ),
        migrations.AddField(
            model_name='singlejob',
            name='adapter',
            field=models.CharField(default='ACGT', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='singlejob',
            name='key',
            field=models.CharField(default='0000000000', max_length=10),
        ),
        migrations.AlterField(
            model_name='pairedjob',
            name='key',
            field=models.CharField(default='0000000000', max_length=10, null=True),
        ),
    ]
