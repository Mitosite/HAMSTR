# Generated by Django 2.0.2 on 2018-02-22 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('align', '0026_auto_20180221_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='ent_key',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default='0000000000', max_length=10)),
            ],
        ),
    ]