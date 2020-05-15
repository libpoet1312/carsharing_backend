from django.apps import AppConfig


class RiderequestsConfig(AppConfig):
    name = 'rideRequests'

    def ready(self):
        import rideRequests.signals
