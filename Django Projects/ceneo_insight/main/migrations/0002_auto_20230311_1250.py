from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='recomendation',
            field=models.CharField(max_length=30),
        ),
    ]
