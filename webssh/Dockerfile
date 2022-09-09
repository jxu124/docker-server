FROM python:3.7.13-slim

RUN pip install webssh --no-cache-dir && \
    rm -rf /tmp/* /var/tmp/*

EXPOSE 8888

ENTRYPOINT ["wssh", "--address=0.0.0.0", "--port=8888"]
