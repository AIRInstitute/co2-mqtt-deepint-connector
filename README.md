# MQTT to Deep Intelligence connector for the proyect CO2

Connector to read data from MQTT and dump it into [Deep Intelligence](https://deepint.net/). Also retrieves the MQTT's topic relation with Deep Intelligence Source information from the project's API.

## How to install tool

First install prerequisites
```bash
sudo apt update
sudo apt install python3 python3-pip -y
```
Then install tool, for that purpose go to the repository root and run the following command

```bash
sudo python3 -m pip install . --upgrade
```

## Usage

Once installed, the application can be accesed via terminal with the command `co2-mqtt-deepint-connector`. A execution example is attached bellow:
```bash
co2-mqtt-deepint-connector 212.128.140.31 2780 JKM1wuXItbZ0JRF8ZdaNE6PW9iGmND2_Kyq2KVnG1MIPch_czSLXC1N24GLWjAZszI4eQrQuxRvdUxsNtF0KLw example-id 1 False
```

It also attaches a help mode as follows:
```
co2-mqtt-deepint-connector --help
Usage: co2-mqtt-deepint-connector [OPTIONS] [MQTT_BROKER] [MQTT_PORT]
                                  [MQTT_USER] [MQTT_PASSWORD] [CONFIG_URL]
                                  [DEEPINT_AUTH_TOKEN] [MQTT_CLIENT_ID]
                                  [MQTT_NUM_MESSAGE_LIMIT] [QUIET_MODE_SET]

  While running dumps messages received from MQTT into deepint.

Arguments:
  [MQTT_BROKER]             MQTT's broker IP
  [MQTT_PORT]               MQTT's broker port
  [MQTT_USER]               MQTT's broker user
  [MQTT_PASSWORD]           MQTT's broker password
  [CONFIG_URL]              URL of the mapping (between MQTT and Deep
                            Intelligence) configuration server's endpoint.

  [DEEPINT_AUTH_TOKEN]      Authentication token for AIR Institute
  [MQTT_CLIENT_ID]          MQTT's client id. If not provided, an UUIDv4 will
                            be generated

  [MQTT_NUM_MESSAGE_LIMIT]  number of messages to store before dumpt to AIR
                            Institute. If set to 0 each message is send
                            [default: 10]

  [QUIET_MODE_SET]           if set to true no logging information is
                             provided.  [default: False]


Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.
  ```

## How to deploy tool

For deploying the application in the `deploy` folder, two deployment medium are attached:
- A Linux Systemd unit
- A PM2 deployment script

### Install Linux Systemd Unit

1. install package as follows in `Usage` function
2. go to deploy folder
3. configure systemd unit replacing the variables between `<` and `>`
4. copy the unit file to folder `/etc/systemd/system` as follows: `cp deploy/co2-mqtt-deepint-connector.service /etc/systemd/system/co2-mqtt-deepint-connector.service`
5. enable unit with `sudo systemctl enable co2-mqtt-deepint-connector.service`
6. start service with `sudo systemctl start co2-mqtt-deepint-connector.service`

```
[Unit] 
Description=MQTT Deep Intelligence connector
After=multiuser.target
StartLimitIntervalSec=0 
 
[Service] 
Type=simple
ExecStart=co2-mqtt-deepint-connector <MQTT_BROKER> <MQTT_PORT> <MQTT_USER> <MQTT_PASSWORD> <CONFIG_URL> <DEEPINT_AUTH_TOKEN> <MQTT_CLIENT_ID> <MQTT_NUM_MESSAGE_LIMIT> <QUIET_MODE_SET> 
 
[Install] 
WantedBy=multi-user.target
```

### Install PM2 file

1. install Node.js and npm with `sudo apt install nodejs npm -y`
2. install PM2 with `sudo npm install -g pm2`
3. configure systemd unit replacing the variables between `<` and `>`
4. register the serbvice with `sudo pm2 start co2-mqtt-deepint-connector.pm2.json`
5. enable the service with `sudo pm2 startup`

```
{
  "apps" : [
    {
      "name": "co2-mqtt-deepint-connector",
      "interpreter": "/bin/bash",
      "script": "co2-mqtt-deepint-connector",
      "args": "<MQTT_BROKER> <MQTT_PORT> <MQTT_USER> <MQTT_PASSWORD> <CONFIG_URL> <DEEPINT_AUTH_TOKEN> <MQTT_CLIENT_ID> <MQTT_NUM_MESSAGE_LIMIT> <QUIET_MODE_SET>",
      "out_file": "/var/log/co2-mqtt-deepint-connector.log",
      "error_file": "/var/log/co2-mqtt-deepint-connector.log"
    }
  ]
}
```
