from django.db.models.signals import post_save
from django.dispatch import receiver

from wheat.models import Users, Basket


# @receiver(post_save, sender=Users)
# def create_basket_for_user(sender, instance, created, **kwargs):
#     print('сигнал сработал')
#     if created:
#         Basket.objects.create(user_id=instance.user_id, products={})