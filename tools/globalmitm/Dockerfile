FROM debian:bullseye-slim

LABEL maintainer="rev1si0n <ihaven0emmail@gmail.com>"

ENV PYPIMIRROR=https://mirrors.ustc.edu.cn/pypi/web/simple
ENV GOST=https://github.com/ginuerzh/gost/releases/download/v2.11.4/gost-linux-386-2.11.4.gz
ENV SOURCESMIRROR=mirrors.ustc.edu.cn

RUN sed -i "s/deb.debian.org/${SOURCESMIRROR}/g" /etc/apt/sources.list
RUN sed -i "s|security.debian.org/debian-security|${SOURCESMIRROR}/debian-security|g" /etc/apt/sources.list

RUN apt-get update && apt-get -y upgrade
RUN apt install -y adb gcc wget dnsutils python3 python3-pip

RUN wget ${GOST} -O - | gzip -d> /usr/bin/gost

COPY globalmitm/DNS2SOCKS /
RUN gcc DNS2SOCKS.c -o /usr/bin/DNS2SOCKS -lpthread

COPY startmitm.py /usr/bin
COPY globalmitm/entry /usr/bin/mitm
COPY requirements.txt /

RUN chmod 755 /usr/bin/gost
RUN chmod 755 /usr/bin/startmitm.py
RUN chmod 755 /usr/bin/mitm

RUN pip3 install --no-cache-dir -i ${PYPIMIRROR} -r /requirements.txt
WORKDIR /root

EXPOSE 53/udp 8118/tcp 1234/tcp
ENTRYPOINT [ "mitm" ]