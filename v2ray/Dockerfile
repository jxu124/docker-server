FROM alpine:3.12 as builder
ADD https://github.com/v2fly/v2ray-core/releases/download/v4.45.2/v2ray-linux-64.zip /
# ADD ./v2ray-linux-64.zip /
RUN mkdir -p /etc/v2ray && \
    apk add unzip && \
    unzip /v2ray-linux-64.zip -d /etc/v2ray && \
    chmod +x /etc/v2ray/v2ray

FROM alpine:3.12
LABEL maintainer="antonyxu"
COPY --from=builder /etc/v2ray /etc/v2ray
WORKDIR /etc/v2ray
CMD [ "/etc/v2ray/v2ray" ]
