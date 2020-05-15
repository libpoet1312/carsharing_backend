from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
import django.dispatch
from .models import Request
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

User = get_user_model()



