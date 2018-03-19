# Generated by Django 2.0.2 on 2018-02-19 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('align', '0019_auto_20180216_1626'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Pairedjob',
        ),
        migrations.DeleteModel(
            name='Singlejob',
        ),
        migrations.AddField(
            model_name='uploadfile',
            name='randkey',
            field=models.CharField(default='0000000000', max_length=101),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='file',
            field=models.FileField(default='/project/home17/whb17/public_html/randtestreads.fasta', upload_to=''),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='title',
            field=models.CharField(default='sample', max_length=50),
        ),
    ]
