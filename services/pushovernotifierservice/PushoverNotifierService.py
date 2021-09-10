import requests

from core.Service import Service
from topics.notification.Notification import Notification

from topics.notification.NotificationLevel import NotificationLevel


class PushoverNotifierService(Service):

    def initialize(self):
        self.core.dataRouter.subscribe(Notification, self.notify)
        self.app_token = self.config['AppToken']
        self.user_token = self.config['UserToken']
        self.pushoverUrl = 'https://api.pushover.net/1/messages.json'

    def start(self):
        pass

    def notify(self, notification):
        content = {"token": self.app_token,
                   "user": self.user_token,
                   "message": notification.message,
                   "priority": self.getPriority(notification.notification_level)
                   }

        resp = "-"
        try:
            resp = requests.post(self.pushoverUrl, content)
        except Exception as e:
            self.core.logger.log("Error: Failed to send notification to Pushover", e)

        if resp.status_code == 200:
            pass
        else:
            self.core.logger.log('Error: PushoverNotifierService resulted in error code ' + resp.status_code +
                                 '. JSON is: ' + resp.json())

    def getPriority(self, notificationLevel):
        if notificationLevel == NotificationLevel.Error:
            return self.config['ErrorPriority']
        elif notificationLevel == NotificationLevel.Info:
            return self.config['InfoPriority']
        else:
            self.core.logger.log('Error: Failed to resolve notification level')

