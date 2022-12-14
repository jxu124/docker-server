
# Docker-Server

[![Docker Test CI](https://github.com/jxu124/docker-server/actions/workflows/build_docker.yml/badge.svg)](https://github.com/jxu124/docker-server/actions/workflows/build_docker.yml)


### Step 1: Add user & password
```bash
adduser antony
```

### Step 2: Install Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt-get install docker-compose-plugin
```

### Step 3: Apply acme.sh
```bash
mkdir -p docker/acme.sh && cd docker
sudo docker pull neilpang/acme.sh
docker run --rm -it -v "${PWD}/acme.sh/config":/acme.sh --net=host neilpang/acme.sh --set-default-ca --server letsencrypt
docker run --rm -it -v "${PWD}/acme.sh/config":/acme.sh --net=host neilpang/acme.sh --issue -d example.com -d *.example.com --dns --yes-I-know-dns-manual-mode-enough-go-ahead-please
docker run --rm -it -v "${PWD}/acme.sh/config":/acme.sh --net=host neilpang/acme.sh --issue -d example.com -d *.example.com --dns --yes-I-know-dns-manual-mode-enough-go-ahead-please --renew
```

### Step 4: Build docker-compose
```bash
git clone https://github.com/jxu124/docker-server
sh upload_unmask.sh
rm -r traefik/config/example.com
cp -r acme.sh/config/example.com traefik/config
```

### Step 5: Start Containers
```bash
docker compose up -d
```

### Frequency Commands
```bash
docker build . -t antonyxu/v2ray
docker login
docker push antonyxu/v2ray
openssl x509 -in acme.sh/config/example.com/example.com.cer -noout -dates  # 测试证书的过期时间
```

### Documents
> https://doc.traefik.io/traefik/
