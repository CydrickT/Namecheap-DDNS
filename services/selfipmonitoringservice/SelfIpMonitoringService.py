
import configparser
import json
import time
import requests
from urllib3.exceptions import NewConnectionError

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
                self.core.logger.logError("Failed to obtain IP.", e)
                if self.lastIpCheckResultSuccessful:
                    self.core.dataRouter.publish(Notification(str(e), NotificationLevel.Error))

                self.lastIpCheckResultSuccessful = False
            else:
                if not self.lastIp == currentIp:
                    self.core.logger.log('Old IP is ' + self.lastIp + ', new IP is ' + currentIp + ', changing IP.')
                    self.core.dataRouter.publish(IpChangeNotification(currentIp))
                    self.lastIp = currentIp
                else:
                    self.core.logger.log('Old IP is ' + self.lastIp + ', new IP is ' + currentIp + ', same IP detected.')
                self.lastIpCheckResultSuccessful = True

            time.sleep(self.monitoringPeriodInSec)

    def getIp(self):

        try:
            resp = requests.get(self.ipMonitoringHostname)
            ip = resp.json()['ip']

            if resp.status_code == 200:
                return ip
            else:
                raise Exception('Obtaining the host\'s IP address failed for the following reason: ' + resp.json())

        except Exception as e:
            raise Exception('Could not obtain the ip from the response.')






