
import configparser
import json
import time
import requests

from core.Service import Service
from topics.ipchangenotification.IpChangeNotification import IpChangeNotification
from topics.notification.Notification import Notification
from topics.notification.NotificationLevel import NotificationLevel


class SelfIpMonitoringService(Service):

    def initialize(self):
        self.ipMonitoringHostname = 'https://api.ipify.org?format=json'
        self.lastIp = "<First start>"
        self.lastIpCheckResultSuccessful = True
        self.monitoringPeriodInSec = self.config.getfloat('IpCheckIntervalInSeconds')

    def start(self):

        while True:
            currentIp = "--"
            try:
                currentIp = self.getIp()
            except Exception as e:
                self.core.logger.log('Error getting the IP: ' + e)
                if self.lastIpCheckResultSuccessful:
                    self.core.dataRouter.publish(Notification(str(e), NotificationLevel.Error))

                self.lastIpCheckResultSuccessful = False
            else:
                if not self.lastIp == currentIp:
                    self.core.logger.log('Old IP is' + self.lastIp + ', new IP is ' + currentIp + ', changing IP...')
                    self.core.dataRouter.publish(IpChangeNotification(currentIp))
                    self.lastIp = currentIp
                self.lastIpCheckResultSuccessful = True

            time.sleep(self.monitoringPeriodInSec)

    def getIp(self):
        url = 'https://api.ipify.org?format=json'
        resp = requests.get(url)
        if resp.status_code != 200:
            raise Exception('Obtaining the host\'s IP address failed for the following reason: ' + resp.json())

        ip = "--"

        try:
            ip = resp.json()['ip']
        except Exception as e:
            raise Exception('Could not obtain the ip from the response.')

        return ip


