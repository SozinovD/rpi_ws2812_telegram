#!/bin/bash

sudo nohup ./led_handler.py &
nohup ./telegram_handler.py &
