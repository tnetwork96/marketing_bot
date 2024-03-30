#!/bin/sh
sudo docker build . -t marketing-bot
sudo docker run -dit marketing-bot