#!/bin/sh

echo "Find update!"
git reset --hard
git pull
sh upload_unmask.sh
rsync ./* ../docker -avu

# docker pull httpd:alpine
# htpasswd -nbBC 10 USER topsecret
