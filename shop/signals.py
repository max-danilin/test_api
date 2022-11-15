from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_email_task
from .models import ShoppingCart


@receiver(post_save, sender=ShoppingCart)
def save_image_to_model(sender, instance, **kwargs):
    send_email_task.delay(sender, instance)