#!/bin/sh
cd transmission && docker build . -t antonyxu/transmission && cd ..
cd v2ray && docker build . -t antonyxu/v2ray && cd ..
cd webdav && docker build . -t antonyxu/webdav && cd ..
