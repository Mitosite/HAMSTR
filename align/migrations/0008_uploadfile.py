# Generated by Django 2.0.1 on 2018-02-12 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('align', '0007_auto_20180209_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='')),
            ],
        ),
    ]
