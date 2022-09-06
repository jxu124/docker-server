FROM alpine:3.12
WORKDIR /home/user
# RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
RUN apk update && \
    apk add transmission-daemon && \
    apk add -U tzdata && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    apk del tzdata
RUN echo -e '\
deluser user \n\
delgroup user \n\
addgroup user -g ${TM_GID} \n\
adduser user -u ${TM_UID} -G user -D \n\
chown -R user:user /home/user \n\
if [ ! -f /home/user/.config/transmission-daemon/settings.json ]; then \n\
    su - user -c "/usr/bin/transmission-daemon && sleep 10s && pkill transmission-daemon && sleep 1s" \n\
    sed -i "s%\"rpc-whitelist-enabled\": true%\"rpc-whitelist-enabled\": false%g" /home/user/.config/transmission-daemon/settings.json \n\
    sed -i "s%\"rpc-authentication-required\": false%\"rpc-authentication-required\": true%g" /home/user/.config/transmission-daemon/settings.json \n\
    cat /home/user/.config/transmission-daemon/settings.json \n\
fi \n\
rm /home/user/.config/transmission-daemon/transmission.log \n\
su - user -c "/usr/bin/transmission-daemon -e /home/user/.config/transmission-daemon/transmission.log" \n\
tail -f /home/user/.config/transmission-daemon/transmission.log \n\
' > entrypoint.sh && chmod +x entrypoint.sh
ADD https://github.com/ronggang/transmission-web-control/raw/master/release/install-tr-control-cn.sh /home/user/
RUN chmod +x install-tr-control-cn.sh && echo "1" | sh install-tr-control-cn.sh && rm install-tr-control-cn.sh
CMD ["/bin/sh", "entrypoint.sh"]
