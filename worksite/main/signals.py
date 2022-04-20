from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User
from .mongo_models import UserMongodb


@receiver(post_save, sender=User, weak=False)
def update_mongodb(sender, instance, **kwargs):
    print('Сигнал работает')
    user = UserMongodb.objects.using('mongo_database').filter(user_id=instance.pk)
    print(user)
    if user.first() is None:
        UserMongodb.objects.using('mongo_database').create(
                    user_id=instance.pk,
                    username=instance.username,
                    email=instance.email,
                    is_active=instance.is_active,
                    is_staff=instance.is_staff,
                    created_at=instance.created_at,
                    updated_at=instance.updated_at,
                )

    # users = User.objects.all()
    # for obj in users:
    #     if UserMongodb.objects.filter(user_id=obj.pk) is None:
    #         UserMongodb.objects.create(
    #             user_id=obj.pk,
    #             username=obj.username,
    #             email=obj.email,
    #             is_active=obj.is_active,
    #             is_staff=obj.is_staff,
    #             created_at=obj.created_at,
    #             updated_at=obj.updated_at,
    #         )


# post_save.connect(update_mongodb, sender=User, weak=False)
