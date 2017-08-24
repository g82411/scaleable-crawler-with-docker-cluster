from .tasks import pageParsing
import time

if __name__ == '__main__':
    urls = ["http://www.ptt.cc/bbs/Food/index{}.html".format(i) for i in range(6138)]
    for url in urls:
        result = pageParsing.delay(url)
