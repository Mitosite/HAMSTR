# Generated by Django 2.0.2 on 2018-02-28 11:59

import align.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('align', '0031_auto_20180226_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singlejob',
            name='readsfile',
            field=models.FileField(default='/project/home17/whb17/public_html/randtestreads.fasta', upload_to='', validators=[align.validators.validate_file_extension]),
        ),
    ]