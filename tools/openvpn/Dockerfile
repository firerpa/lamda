FROM alpine:3.15

LABEL maintainer="rev1si0n <lamda.devel@gmail.com>"

ENV VARS=/etc/openvpn/easy-rsa/vars
ENV OVPNCONFIG=/etc/openvpn/config.ovpn
ENV SOURCESMIRROR=mirrors.ustc.edu.cn

RUN sed -i "s/dl-cdn.alpinelinux.org/${SOURCESMIRROR}/g" /etc/apk/repositories

COPY entry /usr/bin/run
COPY ovpn-server-new /usr/bin
COPY ovpn-client-profile /usr/bin
COPY ovpn-client-revoke /usr/bin
COPY ovpn-client-new /usr/bin

COPY config.ovpn /root
COPY vars /root

RUN apk add openvpn easy-rsa bash curl jq

RUN ln -sf /usr/share/easy-rsa/easyrsa /usr/bin/easyrsa
RUN ln -sf ${VARS} /usr/share/easy-rsa/vars

WORKDIR /etc/openvpn
