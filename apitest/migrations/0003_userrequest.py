# Generated by Django 4.1.4 on 2023-02-09 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0002_alter_testmodel_address_alter_testmodel_age_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requests', models.JSONField(default=dict)),
            ],
            options={
                'verbose_name': 'User request',
                'verbose_name_plural': 'User requests',
            },
        ),
    ]
