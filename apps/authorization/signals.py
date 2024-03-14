from .models import Accounts
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..common.utils.email import Email
from datetime import datetime

@receiver(post_save, sender=Accounts)
def create_new_account(sender, instance, created, **kwargs):
    print("signal fired")
    # send sms if new account is created and user is not a staff
    if created and not instance.is_farmer_staff:
        today = datetime.now().date()
        data = {
            "name": instance.name,
            "date": f'{today.day} {today.strftime("%b")}, {today.year}'
        }

        # different template for farmer and mentor
        html_template = "user_registration_success.html" if instance.user_type == "FARMER" else "mentor_registration_success.html"
        try:
            email_obj = Email()
            email_obj.send_email(
                subject="CropGnosis",
                to=[instance.email],
                html_template=html_template,
                data=data
            )
        except Exception as e:
            print(e)
            # add to log
