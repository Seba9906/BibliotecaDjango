# Generated by Django 4.2.5 on 2023-10-23 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_libro_caratula_remove_libro_modificacion_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='autor',
            name='apellido',
        ),
        migrations.AlterField(
            model_name='autor',
            name='nombre',
            field=models.CharField(max_length=100, verbose_name='Nombre y Apellido del Autor/a'),
        ),
        migrations.AlterField(
            model_name='libro',
            name='genero',
            field=models.CharField(choices=[('FIC', 'Ficción'), ('NFIC', 'No Ficción'), ('SF', 'Ciencia Ficción'), ('MYST', 'Misterio'), ('ROM', 'Romance'), ('DRAMA', 'Drama'), ('FANT', 'Fantasía'), ('BIO', 'Biografía'), ('ACAD', 'Artículos Académicos')], max_length=100),
        ),
        migrations.AlterField(
            model_name='libro',
            name='publicacion',
            field=models.IntegerField(verbose_name='Año de publicación'),
        ),
    ]
