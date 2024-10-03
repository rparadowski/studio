# Generated by Django 3.2.24 on 2024-03-22 23:30
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('contentcuration', '0146_drop_taskresult_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formatpreset',
            name='id',
            field=models.CharField(choices=[('high_res_video', 'High Resolution'), ('low_res_video', 'Low Resolution'), ('video_thumbnail', 'Thumbnail'), ('video_subtitle', 'Subtitle'), ('video_dependency', 'Video (dependency)'), ('audio', 'Audio'), ('audio_thumbnail', 'Thumbnail'), ('audio_dependency', 'audio (dependency)'), ('document', 'Document'), ('epub', 'ePub Document'), ('document_thumbnail', 'Thumbnail'), ('exercise', 'Exercise'), ('exercise_thumbnail', 'Thumbnail'), ('exercise_image', 'Exercise Image'), ('exercise_graphie', 'Exercise Graphie'), ('channel_thumbnail', 'Channel Thumbnail'), ('topic_thumbnail', 'Thumbnail'), ('html5_zip', 'HTML5 Zip'), ('html5_dependency', 'HTML5 Dependency (Zip format)'), ('html5_thumbnail', 'HTML5 Thumbnail'), ('h5p', 'H5P Zip'), ('h5p_thumbnail', 'H5P Thumbnail'), ('zim', 'Zim'), ('zim_thumbnail', 'Zim Thumbnail'), ('qti', 'QTI Zip'), ('qti_thumbnail', 'QTI Thumbnail'), ('slideshow_image', 'Slideshow Image'), ('slideshow_thumbnail', 'Slideshow Thumbnail'), ('slideshow_manifest', 'Slideshow Manifest'), ('imscp_zip', 'IMSCP Zip')], max_length=150, primary_key=True, serialize=False),
        ),
    ]
