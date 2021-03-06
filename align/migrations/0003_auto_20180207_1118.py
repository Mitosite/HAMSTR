# Generated by Django 2.0.1 on 2018-02-07 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('align', '0002_alnindex'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paired_job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Single_job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_filename', models.TextField()),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='Double',
        ),
        migrations.DeleteModel(
            name='Single',
        ),
        migrations.RemoveField(
            model_name='alnindex',
            name='Name',
        ),
        migrations.RemoveField(
            model_name='alnindex',
            name='compfile',
        ),
        migrations.RemoveField(
            model_name='alnindex',
            name='date',
        ),
        migrations.AddField(
            model_name='alnindex',
            name='BWA_idx_path',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='alnindex',
            name='Bt2_idx_path',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='alnindex',
            name='NGM_idx_path',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='alnindex',
            name='Naln_idx_path',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='alnindex',
            name='S3dp_idx_path',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='alnindex',
            name='SMALT_idx_path',
            field=models.TextField(null=True),
        ),
    ]
