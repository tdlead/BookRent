# Generated by Django 5.0.6 on 2024-07-04 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='return_date',
            field=models.DateField(blank=True, help_text='actual returned date', null=True),
        ),
    ]
