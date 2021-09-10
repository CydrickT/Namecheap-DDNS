from topics.notification.NotificationLevel import NotificationLevel


class Notification:
    def __init__(self, message, notification_level=NotificationLevel.Info):
        self.message = message
        self.notification_level = notification_level

