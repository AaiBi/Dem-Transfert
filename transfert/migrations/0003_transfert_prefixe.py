# Generated by Django 3.2.9 on 2022-01-31 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfert', '0002_alter_transfert_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfert',
            name='prefixe',
            field=models.CharField(default='', max_length=300),
        ),
    ]
