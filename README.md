# rpi_ws2812_telegram

*THIS THING JUST PINGS HOSTS*

Hi, it's more of a fun than really usefull project

Just making up near-real-world usecases for my RPi0W as former SRE engineer to train my Python skills

## Requiements

### Hardware
* RaspberryPi or any pin-to-pin compatible SBC (OrangePi, BananaPi or Radxa should also be okay)
* ws2812 hat for Raspberry. I use this https://www.waveshare.com/wiki/RGB_LED_HAT
### Software
* Python >=3.7.3
* rpi_ws281x library (`python3 -m pip install rpi_ws281x`)
* telebot library (`python3 -m pip install telebot`)

## Installation

1. Install python3 and git

`sudo apt update && sudo apt install git python3 -y`

2. Clone this git repo to your device

`git clone https://github.com/SozinovD/rpi_ws2812_telegram; cd rpi_ws2812_telegram`

3. Change api_key in tg.ini file, so file looks like this:

[TELEGRAM]

api_key = AAABBBCCC:DDDEEEFFFFFFF

admin_id = <ADMIN_USER_ID>

4. Make script "run_all.sh" executable and run it

`chmod +x run_all.sh; ./run_all.sh`
