#!/bin/sh
# 
if [ ! "$(git pull)"=="Already up to date.\n" ]
    git reset --hard
    git pull
    sh upload_unmask.sh
    rsync ./* ../docker -avu
fi

# docker pull httpd:alpine
# htpasswd -nbBC 10 USER topsecret
