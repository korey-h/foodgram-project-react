from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions')

    subscription = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers')

    class Meta:
        unique_together = ['user', 'subscription']
