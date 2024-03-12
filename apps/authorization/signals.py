from .models import Accounts
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..common.utils import send_email
from datetime import datetime

@receiver(post_save, sender=Accounts)
def create_new_account(sender, instance, created, **kwargs):
    print("signal fired")
    # send sms if new account is created
    if created:
        today = datetime.now().date()
        data = {
            "name": instance.name,
            "date": f'{today.day} {today.strftime("%b")}, {today.year}'
        }
        try:
            send_email(
                subject="CropGnosis",
                to=[instance.email],
                html_template="user_registration_success.html",
                data=data
            )
        except Exception as e:
            print(e)
            # add to log
