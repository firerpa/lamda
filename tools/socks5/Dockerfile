FROM alpine:3.15
# this will produce large image but IDC
LABEL maintainer="rev1si0n <lamda.devel@gmail.com>"

ENV SOURCESMIRROR=mirrors.ustc.edu.cn
RUN sed -i "s/dl-cdn.alpinelinux.org/${SOURCESMIRROR}/g" /etc/apk/repositories

COPY entry /usr/bin

RUN apk add bash make g++ git

RUN mkdir -p /tmp/workdir
WORKDIR /tmp/workdir

RUN wget https://www.inet.no/dante/files/dante-1.4.3.tar.gz -O - | tar -xz
WORKDIR /tmp/workdir/dante-1.4.3

ENV ac_cv_func_sched_setscheduler=no
RUN ./configure --disable-client && make -j $(nproc)
RUN cp sockd/sockd /usr/bin

RUN rm -rf /tmp/workdir

WORKDIR /

EXPOSE 1080/tcp 1080/udp 50000:55000/udp
ENTRYPOINT ["entry"]
