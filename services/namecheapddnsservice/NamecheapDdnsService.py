
import requests
import threading
import time

from core.Service import Service
from topics.ipchangenotification.IpChangeNotification import IpChangeNotification
from topics.notification.Notification import Notification
from topics.notification.NotificationLevel import NotificationLevel


class NamecheapDdnsService(Service):

    def initialize(self):
        self.core.dataRouter.subscribe(IpChangeNotification, self.updateIp)
        self.url_pattern = 'https://dynamicdns.park-your-domain.com/update?host={host}&domain={domain}&password={password}'
        self.ipChangeThread = None
        self.ipChangeThreadSemaphore = threading.Semaphore()
        self.core.dataRouter.subscribe(IpChangeNotification, self.updateIp)

    def start(self):
        pass

    def updateIp(self, ip_change_notification):
        self.ipChangeThreadSemaphore.acquire()
        if self.ipChangeThread is not None:
            self.ipChangeThread.stopIpChange()
        self.ipChangeThread = IpChangeThread(ip_change_notification, self.config, self.core, self.url_pattern)
        threading.Thread(target=self.ipChangeThread.changeIp).start()
        self.ipChangeThreadSemaphore.release()


class IpChangeThread:

    def __init__(self, ip_change_notification, config, core, url_pattern):
        self.interruptThread = False
        self.ip_change_notification = ip_change_notification
        self.config = config
        self.url_pattern = url_pattern
        self.core = core

    def changeIp(self):
        while self.interruptThread is False:
            host = self.config['Host']
            domain = self.config['Domain']
            password = self.config['Password']
            repeatPeriodInSec = self.config.getint('RepeatPeriodInSec')

            url = self.url_pattern.format(host=host, domain=domain, password=password)
            resp = "-"
            try:
                resp = requests.get(url)
            except Exception as e:
                self.core.dataRouter.publish(Notification("Failed to update IP", NotificationLevel.Error))
                self.core.logger.log("Error: NamecheapDdnsService returned the following error: ", e)
            if resp.status_code == 200:
                self.core.dataRouter.publish(
                    Notification("Updated IP of " + domain + " to IP " + self.ip_change_notification.new_ip, NotificationLevel.Info))
                self.interruptThread = True
            else:
                self.core.logger.log('Failed to update : ' + resp.json())
                self.core.dataRouter.publish(
                    Notification("Failed to update Namecheap's IP to " + self.ip_change_notification.new_ip, NotificationLevel.Error))

            time.sleep(repeatPeriodInSec)

    def stopIpChange(self):
        self.interruptThread = True

