# Generated by Django 2.2.15 on 2020-09-19 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_auto_20200919_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='bank',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Zenith Bank'), (1, 'Fidelity Bank'), (2, 'Access Bank')], null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Submitted'), (1, 'Processing'), (2, 'Paid'), (4, 'Allocated')], null=True),
        ),
    ]
