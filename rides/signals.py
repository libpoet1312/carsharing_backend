from django.db.models.signals import m2m_changed
from notifications.signals import notify
from .models import Ride


# def join_request_handler(sender, instance, created, **kwargs):
#     notify.send(instance, verb='Join Request Added')
#
#
# m2m_changed.connect(join_request_handler, sender=Ride.joinRequests)


# def notify(user, actor, verb, action='', target='', description=''):
#     n = user.notification.create(
#          actor=actor, verb=verb, action=action,
#          target=target, description=description)
#     return n
