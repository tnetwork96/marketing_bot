FROM arm64v8/ubuntu:18.04
WORKDIR /home/marketing-bot
ENV PYTHONPATH /home/marketing-bot
COPY . ./
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