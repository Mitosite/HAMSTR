# Generated by Django 2.0.2 on 2018-02-23 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('align', '0027_ent_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media')),
            ],
        ),
        migrations.RemoveField(
            model_name='uploadfile',
            name='randkey',
        ),
    ]
