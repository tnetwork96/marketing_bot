from jinja2 import Template
import subprocess
from core.util.file_handler import FileHandler

cookies = FileHandler.read_file("cookie_token.txt").split("\n")

docker_compose_template = \
    Template("""
version: '3'
networks:
  my-network:
    driver: bridge
services:
#  telegram_service:
#    command: python3 main_bot.py &
#    restart: always
#    build:
#      context: .
#      dockerfile: telefile
#    networks:
#      - my-network
#  api_service:
#    command: python3 temp_api.py &
#    restart: always
#    build:
#      context: .
#      dockerfile: apifile
#    ports:
#      - "8000:8000"
#    networks:
#      - my-network
  fb_cookies_service_{{ bot_name }}:
    command: python3 main_update_cookie.py {{ bot_name }} &
    build:
      context: .
      dockerfile: botfile
    networks:
      - my-network
""")

docker_file_template = \
    Template("""
FROM arm32v7/python:3.8
#FROM python:3.8
WORKDIR /home/marketing-bot
ENV PYTHONPATH /home/marketing-bot
COPY . ./
RUN apt-get -y update
RUN apt-get install -y firefox-esr
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-arm7hf.tar.gz
RUN tar -xf geckodriver-v0.23.0-arm7hf.tar.gz
RUN rm geckodriver-v0.23.0-arm7hf.tar.gz
RUN chmod a+x geckodriver
RUN mv geckodriver /usr/local/bin/
RUN pip install selenium==3.141.0
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN nohup python3 main_update_cookie.py {{ bot_name }} &
# docker build . -t rune_crawler
# docker run -d rune_crawler
""")

for idx, ck in enumerate(cookies):
    if idx % 2 == 0:
        docker_compose_text = docker_compose_template.render(bot_name=ck)
        docker_compose_text = docker_compose_text.strip()
        with open("docker-compose.yaml", "w") as f:
            f.write(docker_compose_text)
        docker_file_text = docker_file_template.render(bot_name=ck)
        docker_file_text = docker_file_text.strip()
        with open("botfile", "w") as f:
            f.write(docker_file_text)
    else:
        FileHandler.write_file("cookies_selenium.txt", ck.strip(), override=True)
        p = subprocess.Popen("sudo docker-compose up --build -d", stdout=subprocess.PIPE, shell=True)
        a = p.communicate()