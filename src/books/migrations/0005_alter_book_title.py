# Generated by Django 5.0.6 on 2024-07-04 12:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.booktitle'),
        ),
    ]