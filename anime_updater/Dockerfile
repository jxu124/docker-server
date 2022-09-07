FROM python:3.7.13-slim
WORKDIR /
RUN apt update && apt install -y transmission-cli && apt-get autoclean && rm -rf /var/lib/apt/lists/* && \
    pip install opencc cfscrape --no-cache-dir
ADD anime_updater.py /
RUN echo "\
while [ 1 ] \n\
do \n\
    python anime_updater.py -q anime_query.txt \n\
    sleep 60  \n\
done \n\
" > entrypoint.sh && chmod +x entrypoint.sh && cat entrypoint.sh
CMD ["sh", "entrypoint.sh"]
