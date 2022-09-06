FROM alpine:3.12 as certs
# RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
RUN apk --update add ca-certificates

FROM scratch
COPY --from=certs /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

EXPOSE 80
# ADD https://github.com/hacdias/webdav/releases/download/v4.2.0/linux-amd64-webdav.tar.gz /
ADD ./linux-amd64-webdav.tar.gz /

ENTRYPOINT [ "/webdav" ]