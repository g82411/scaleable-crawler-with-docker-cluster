# Celery RabbitMQ Ptt 爬蟲  

### origin source:[scaleable-crawler-with-docker-cluster](https://github.com/tonywangcn/scaleable-crawler-with-docker-cluster)
### origin article:[How to build a scaleable crawler to crawl million pages with a single machine in just 2 hours](https://medium.com/@tonywangcn/how-to-build-a-scaleable-crawler-to-crawl-million-pages-with-a-single-machine-in-just-2-hours-ab3e238d1c22)

## Description:  
  根據上面的那兩篇文章改寫的ptt爬蟲
## Requirements:
  - Docker
  - python 3.6
  - bs4
  - requests

## 執行方式:
  1. docker-compose create
  2. docker-compose build
  3. docker-compose up -d
  4. docker-compose scale worker=5
  5. python -m test_celery.run_tasks
