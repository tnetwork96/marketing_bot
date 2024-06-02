from jinja2 import Template
import subprocess
from core.util.file_handler import FileHandler

cookies = FileHandler.read_file("cookie_list.txt").split("\n")

docker_compose_template = \
    Template("""
version: '3'
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
  marketing_service:
    # command: ["./script.sh", "botname"]
    # command: python3 main_simulator.py {{ bot_name }} &
    build:
      context: .
      dockerfile: botfile
    volumes:
        - ./:/home/marketing-bot
networks:
  - my-network
networks:
  my-network:
    driver: bridge
""")

docker_file_template = \
    Template("""
FROM arm64v8/ubuntu:18.04
WORKDIR /home/marketing-bot
ENV PYTHONPATH /home/marketing-bot
#COPY . ./
RUN apt update
RUN apt install -y python3.8 python3-pip wget
RUN apt install -y firefox
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-arm7hf.tar.gz
RUN tar -xf geckodriver-v0.23.0-arm7hf.tar.gz
RUN rm geckodriver-v0.23.0-arm7hf.tar.gz
RUN chmod a+x geckodriver
RUN mv geckodriver /usr/local/bin/
RUN python3 -m pip install --upgrade pip
RUN pip3 install selenium==3.141.0
ADD requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
CMD ["./script.sh", "botname"]
# RUN nohup python3 main_simulator.py {{ bot_name }} &
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