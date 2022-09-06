FROM python:3.7.13-slim
WORKDIR /
ADD anime_updater.py
RUN pip install opencc cfscrape --no-cache-dir
CMD ["python", "anime_updater.py"]
