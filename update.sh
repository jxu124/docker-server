#!/bin/sh
git reset --hard
git pull
sh upload_unmask.sh
rsync ./* ../docker -avu
