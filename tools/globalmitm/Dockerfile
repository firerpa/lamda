FROM debian:bullseye-slim

LABEL maintainer="rev1si0n <lamda.devel@gmail.com>"

ENV VERSION=2.11.4
ENV PLAT=linux-386

ENV PYPIMIRROR=https://mirrors.ustc.edu.cn/pypi/web/simple
ENV GOST=https://github.com/ginuerzh/gost/releases/download/v${VERSION}/gost-${PLAT}-${VERSION}.gz
ENV BINDIR=/usr/local/bin

WORKDIR /tmp
RUN apt-get update && apt-get -y upgrade && apt install -y adb gcc wget dnsutils python3 python3-pip

RUN wget ${GOST} -O - | gzip -d> ${BINDIR}/gost

COPY startmitm.py ${BINDIR}
COPY globalmitm/entry ${BINDIR}
COPY globalmitm/DNS2SOCKS.c /tmp
COPY requirements.txt /tmp

RUN gcc -pthread DNS2SOCKS.c -o ${BINDIR}/DNS2SOCKS
RUN pip3 install -i ${PYPIMIRROR} --no-cache-dir -r requirements.txt

RUN chmod 755 ${BINDIR}/*
ENV PATH=${BINDIR}:${PATH}

WORKDIR /root
EXPOSE 53/udp 8118/tcp 1234/tcp
ENTRYPOINT [ "entry" ]