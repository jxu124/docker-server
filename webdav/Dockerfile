FROM alpine:3.12 as certs
# RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
RUN apk --update add ca-certificates wget
RUN wget https://github.com/hacdias/webdav/releases/download/v4.2.0/linux-amd64-webdav.tar.gz && \
    mkdir /webdav && tar -zxvf linux-amd64-webdav.tar.gz -C /webdav
    

FROM scratch
COPY --from=certs /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=certs /webdav/* /

EXPOSE 80
ENTRYPOINT [ "/webdav" ]
