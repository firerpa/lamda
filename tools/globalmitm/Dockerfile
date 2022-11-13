FROM debian:bullseye-slim

LABEL maintainer="rev1si0n <ihaven0emmail@gmail.com>"

ENV PYPIMIRROR=https://mirrors.ustc.edu.cn/pypi/web/simple
ENV SSCLIENT=https://github.com/shadowsocks/go-shadowsocks2/releases/download/v0.1.5/shadowsocks2-linux.gz
ENV SOURCESMIRROR=mirrors.ustc.edu.cn

RUN sed -i "s/deb.debian.org/${SOURCESMIRROR}/g" /etc/apt/sources.list
RUN sed -i "s|security.debian.org/debian-security|${SOURCESMIRROR}/debian-security|g" /etc/apt/sources.list

RUN apt-get update && apt-get -y upgrade
RUN apt install -y adb wget privoxy dnsutils python3 python3-pip

COPY startmitm.py /usr/bin
COPY globalmitm/entry /usr/bin/mitm
COPY requirements.txt /

RUN wget ${SSCLIENT} -O - | gzip -d> /usr/bin/go-shadowsocks2
RUN chmod 755 /usr/bin/go-shadowsocks2

RUN chmod 755 /usr/bin/mitm
RUN chmod 755 /usr/bin/startmitm.py

RUN pip3 install --no-cache-dir -i ${PYPIMIRROR} -r /requirements.txt
WORKDIR /root

EXPOSE 53/udp 8118/tcp 1234/tcp
ENTRYPOINT [ "mitm" ]