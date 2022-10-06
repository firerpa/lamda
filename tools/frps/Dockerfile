FROM alpine:3.15
LABEL maintainer="rev1si0n <ihaven0emmail@gmail.com>"

COPY entry /usr/bin
RUN chmod 755 /usr/bin/entry

ENV VERSION=0.44.0
ENV PLAT=linux_386

ENV SOURCESMIRROR=mirrors.ustc.edu.cn
RUN sed -i "s/dl-cdn.alpinelinux.org/${SOURCESMIRROR}/g" /etc/apk/repositories
RUN apk add bash curl jq

WORKDIR /tmp

ENV DOWNLOADURL=https://github.com/fatedier/frp/releases/download/v${VERSION}/frp_${VERSION}_${PLAT}.tar.gz
RUN wget ${DOWNLOADURL} -O - | tar -xz

RUN cp frp_${VERSION}_${PLAT}/frps /usr/bin
WORKDIR /

EXPOSE 6009/tcp 6119/tcp
ENTRYPOINT ["entry"]
