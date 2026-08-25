# Generated manually to preserve the default ordering declared on both models.

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movement',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name']},
        ),
    ]
