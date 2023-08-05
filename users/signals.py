from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from .tasks import send_email


# @receiver(post_save, sender=CustomUser)
def send_welcome_message(sender, instance, created, **kwargs):
    user = instance
    if created:
        if user.email:
            send_email.delay(
                subject='Welcome To GoodReads!',
                message=f"Hello {user.username}, Welcome to the GoodReads community.Enjoy the books and comments.",
                recipient_list=[user.email]
            )


post_save.connect(send_welcome_message, sender=CustomUser)
