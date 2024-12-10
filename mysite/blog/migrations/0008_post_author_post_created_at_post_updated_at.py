import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def set_author_default(apps, schema_editor):
    # Get the User model
    User = apps.get_model(settings.AUTH_USER_MODEL)
    default_user = User.objects.first()  # Use the first user in the database as default
    if not default_user:
        raise Exception("No user exists to set as the default author.")
    # Get the Post model and update all records
    Post = apps.get_model('blog', 'Post')
    for post in Post.objects.filter(author__isnull=True):
        post.author = default_user
        post.save()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_remove_post_dislikes_remove_post_likes_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='posts',
                to=settings.AUTH_USER_MODEL,
                null=True  # Allow temporarily null values
            ),
        ),
        migrations.AddField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.RunPython(set_author_default),  # Set a default author for existing posts
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='posts',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
