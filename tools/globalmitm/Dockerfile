FROM debian:bullseye-slim

ENV PYPIMIRROR=https://mirrors.ustc.edu.cn/pypi/web/simple
ENV SSCLIENT=https://github.com/shadowsocks/go-shadowsocks2/releases/download/v0.1.5/shadowsocks2-linux.gz
ENV SOURCESMIRROR=mirrors.ustc.edu.cn

RUN sed -i "s/deb.debian.org/${SOURCESMIRROR}/g" /etc/apt/sources.list
RUN sed -i "s|security.debian.org/debian-security|${SOURCESMIRROR}/debian-security|g" /etc/apt/sources.list

RUN apt-get update && apt-get -y upgrade
RUN apt install -y git adb wget privoxy python3 python3-pip

COPY entry /usr/bin/mitm
RUN chmod 755 /usr/bin/mitm

WORKDIR /tmp

RUN git clone https://github.com/rev1si0n/lamda
RUN pip3 install -i ${PYPIMIRROR} -r lamda/tools/requirements.txt
RUN pip3 install -i ${PYPIMIRROR} packaging

RUN cp lamda/tools/startmitm.py /usr/bin
RUN chmod 755 /usr/bin/startmitm.py

RUN wget ${SSCLIENT} -O - | gzip -d> /usr/bin/go-shadowsocks2
RUN chmod 755 /usr/bin/go-shadowsocks2

RUN ( timeout 5 mitmdump; exit 0 ) && rm -rf lamda
WORKDIR /root

EXPOSE 53/tcp 53/udp 8118/tcp
ENTRYPOINT [ "mitm" ]
