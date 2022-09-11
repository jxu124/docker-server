#/bin/sh

# ==========================================================================================
# Set your hostname & username & password
MY_HOSTNAME=example.com
MY_USERNAME=admin
MY_PASSWORD=admin
MY_V2RAY_PASSWORD=v2ray

# Set your ID & Token from dash.cloudflare.com
# https://github.com/acmesh-official/acme.sh/wiki/dnsapi
CF_Zone_ID="1234567890abcdef"
CF_Account_ID="1234567890abcdef"
CF_Token="1234567890abcdef"
# ==========================================================================================

cd `dirname $0`

######## cert issue ########
docker run --rm -it -v "${PWD}/acme.sh/config":/acme.sh neilpang/acme.sh --set-default-ca --server letsencrypt
docker run --rm -it -v "${PWD}/acme.sh/config":/acme.sh \
    -e CF_Zone_ID=$CF_Zone_ID \
    -e CF_Account_ID=$CF_Account_ID \
    -e CF_Token=$CF_Token \
    neilpang/acme.sh --issue --dns dns_cf -d ${MY_HOSTNAME} -d *.${MY_HOSTNAME}
rsync -avu ${PWD}/acme.sh/config/${MY_HOSTNAME} traefik/config/


######## unmask private infomation ########
UNPW_APR1=$(docker run -it --rm httpd:alpine htpasswd -n ${MY_USERNAME} ${MY_PASSWORD})
UNPW_BCRY=$(docker run -it --rm httpd:alpine htpasswd -nbBC 10 ${MY_USERNAME} ${MY_PASSWORD})
PW_BCRY=$(echo ${UNPW_BCRY} | awk '{split($1, arr, ":"); print arr[2]}')

# README
# traefik/config/providers.yml
sed -i "s%example.com%${MY_HOSTNAME}%g" traefik/config/providers.yml
sed -i "s%admin:\$apr1\$4nuBhmL6\$rIfXGmd2OotIIp.2iW9XF/%${UNPW_APR1}%g" traefik/config/providers.yml
# v2ray/config/config.json
sed -i "s%yourpassword%${MY_V2RAY_PASSWORD}%g" v2ray/config/config.json
# webdav/config/config.yaml
sed -i "s%example.com%${MY_HOSTNAME}%g" webdav/config/config.yaml
sed -i "s%admin%${MY_USERNAME}%g" webdav/config/config.yaml
sed -i "s%123456%{bcrypt}${PW_BCRY}%g" webdav/config/config.yaml
# transmission/config/settings.json
sed -i "s%\"rpc-username\": \"admin\"%\"rpc-username\": ${MY_USERNAME}%g" transmission/config/settings.json
sed -i "s%\"rpc-password\": \"[^\"]*\"%\"rpc-password\": \"${MY_PASSWORD}\"%g" transmission/config/settings.json


# Renew
# cd /root/docker
# docker run --rm -it -v "${PWD}/acme.sh/config":/acme.sh neilpang/acme.sh --issue --dns dns_cf -d ${MY_HOSTNAME} -d *.${MY_HOSTNAME}
# rsync -avu ${PWD}/acme.sh/config/${MY_HOSTNAME} traefik/config/
