# Namecheap-DDNS

Namecheap DDNS auto-updater with Pushover notifications. 

## Variables to provide

| Environment Variable | Description |
| -------------------- | ----------- |
| `NAMECHEAP_HOST` | Host for the Namecheap domain. (ie: `@`) |
| `NAMECHEAP_DOMAIN` | Your domain name (ie: `example.com`) |
| `NAMECHEAP_DDNS_PASSWORD` | `Dynamic DNS Password` in Namecheap |
| `PUSHOVER_USER_TOKEN` | `User Key` in Pushover |
| `PUSHOVER_APP_TOKEN` | `API Token/Key` in Pushover |
| `CHECK_PERIOD` | Period in seconds for which the IP check is done (ie: `30` for 30 seconds) |

## Building & Running

1. `git submodule update --recursive`
2. `python /path/to/Namecheap-DDNS/core/Application.py /path/to/Namecheap-DDNS.config`

## Features

### IP Monitoring Service

Uses the ipify.org API to obtain the current external IP of the computer. If it detects that the IP has changed, it is going to trigger a DDNS request to Namecheap

### Namecheap DDNS

Uses dynamicdns.park-your-domain.com to update the IP of the host and domain mentioned in the environment variables. 

### Pushover Notifier

When the IP is updated, a Pushover notification will be sent. Furthermore, if the application container fails to update the IP, a Pushover notification will also be sent.

## Service configuration

### Namecheap configuration

Here is a template configuration in order to enable the Dynamic DNS feature.

1. Under your domain, in the tab "Advanced DNS", add a host record with the following arguments:
   1. Type: `A+ Dyamic DNS Record`
   1. Host: `@`
   1. Value: `8.8.8.8` (note: Will be changed by the DDNS)
   1. TTL: `Automatic`
1. Still in the "Advanced DNS" tab, enable the `Dynamic DNS` feature. Note the `Dynamic DNS Password`.

### Pushover configuration

1. On Pushover, note the `User Key` displayed at the top left.
1. Create an application:
   1. Click on "Create an Application/API Token"
   1. Enter a name and description of your choice for the application
   1. Note the `API Token/Key`
