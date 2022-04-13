from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from .mongo_models import UserMongodb


@receiver(post_save, sender=User)
def update_mongodb():
    users = User.objects.all()
    for obj in users:
        if UserMongodb.objects.filter(user_id=obj.pk) is None:
            UserMongodb.objects.create(
                user_id=obj.pk,
                username=obj.username,
                email=obj.email,
                is_active=obj.is_active,
                is_staff=obj.is_staff,
                created_at=obj.created_at,
                updated_at=obj.updated_at,
            )
