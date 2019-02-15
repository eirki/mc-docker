FROM ubuntu:16.04

RUN useradd -m mc && \
    mkdir -p /home/mc/render && \
    cd /home/mc

WORKDIR /home/mc/

COPY 1.13.2.jar /home/mc/minecraft.jar

RUN apt-get update && \
	apt-get install -y build-essential python-pillow python-dev python-numpy python-pip git && \
	git clone --single-branch --branch minecraft113 https://github.com/overviewer/Minecraft-Overviewer.git && \
	python /home/mc/Minecraft-Overviewer/setup.py build

RUN pip install requests

RUN chown mc:mc -R /home/mc/
RUN chown mc:mc -R /home/mc/render

USER mc

COPY renderconfig.py /home/mc/renderconfig.py
COPY download.py /home/mc/download.py
COPY entrypoint.sh /home/mc/entrypoint.sh

ENTRYPOINT ["bash", "-e", "entrypoint.sh"]
