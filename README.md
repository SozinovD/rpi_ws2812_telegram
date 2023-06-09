# rpi_ws2812_telegram

*THIS THING JUST PINGS HOSTS*

Just making up near-real-world usecases for my RPi0W as former SRE engineer to train my Python skills

Sometimes i need to ping several hosts for debuggind purposes for couple hours, so it's more handy to look at LEDs and immediatly see what's up with hosts than to add them to monitoring or keep several terminal windows open

![Example setup](https://github.com/SozinovD/rpi_ws2812_telegram/blob/main/photos/photo_2023-03-24_12-34-05.jpg)


## Requiements

### Hardware
* RaspberryPi or any pin-to-pin compatible SBC (OrangePi, BananaPi or Radxa should also be okay)
* ws2812 hat for Raspberry. I use this https://www.waveshare.com/wiki/RGB_LED_HAT
### Software
* Python >=3.7.3
* rpi_ws281x library (`python3 -m pip install rpi_ws281x`)
* telebot library (`python3 -m pip install telebot`)

## Installation

0. In Telegram go to BotFather and create a new bot (https://core.telegram.org/bots/tutorial)

1. Install python3 and git to you SBC:

`sudo apt update && sudo apt install git python3 -y`

2. Clone this git repo to your device and go to project's dir:

`git clone https://github.com/SozinovD/rpi_ws2812_telegram; cd rpi_ws2812_telegram`

3. Install requirements:

`python3 -m pip install -r requirements.txt`

4. Change api_key in tg.ini file, so file looks like this:

```
[TELEGRAM]
api_key = AAABBBCCC:DDDEEEFFFFFFF
admin_id = <ADMIN_USER_ID>
```

5. Make script "run_all.sh" executable and run it:

`chmod +x run_all.sh; ./run_all.sh`

6. Send message to your bot, it will reply that you are not permitted to use it and will return your user_id. Add your user_id to tg.ini file, so it looks like this:

```
[TELEGRAM]
api_key = AAABBBCCC:DDDEEEFFFFFFF
admin_id = 123123123123
```

7. Now you can add and delete hosts from monitoring, also you can change brightness of all LEDs and color of UP and DOWN host states by sending these commands to bot (always add '/' in front of command):

```
add_host - add host to monitoring
del_host - del host from monitoring by LED
show_hosts - show all hosts in config
chng_bright - change LED brightness
chng_up_color - change color for UP hosts
chng_down_color - change color for DOWN hosts
show_conf - show full current config
list_files - list files in ~/files subdir
rm_file - remove file from subdir
send_file - send file back to chat
```
