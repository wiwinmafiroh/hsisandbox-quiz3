# Generated by Django 4.0.4 on 2022-04-13 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evaluasi_harian', '0002_rename_nilaipeserta_nilaievaluasi_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lembarevaluasi',
            name='durasi',
        ),
        migrations.CreateModel(
            name='TotalNilai',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_nilai', models.FloatField(default=0, null=True)),
                ('predikat', models.CharField(choices=[('Mumtaz Murtafi', '100'), ('Mumtaz', '90-99'), ('Jayyid Jiddan', '80-89'), ('Jayyid', '70-79'), ('Maqbul', '50-69'), ('Rasib', '1-49'), ('Ghayyib', '0')], default='Ghayyib', max_length=50)),
                ('peserta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluasi_harian.peserta')),
            ],
            options={
                'verbose_name_plural': 'Total Nilai',
            },
        ),
    ]
