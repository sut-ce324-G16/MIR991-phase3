import json
import random
import time
from collections import OrderedDict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Crawler.utils import Extractor, BadPaperException


def crawl(count=5000):
    urls = []
    with open("start.txt", "r") as f:
        for url in f.readlines():
            urls.append(url.strip())
        url_set = set(urls)

    # headless run with natural user-agent
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument(
        '--user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"')

    driver = webdriver.Chrome('/Users/sana/Documents/GitHub/MIR991-phase3/Crawler/Driver/chromedriver', options=chrome_options)

    for i in range(count):
        url = urls[i]
        print("url[%u]: %s" % (i + 1, url))
        page_content = Extractor.get_page_content(url, driver)

        # extract page info
        try:
            doc_id = url.split("/")[-1]
            title = Extractor.extract_title(page_content)
            year = Extractor.extract_year(page_content)
            authors = Extractor.extract_authors(page_content)
            abstract = Extractor.extract_abstract(page_content)
            references = Extractor.extract_references(page_content)
        except BadPaperException as e:
            reference = str(e)
            if reference != "" and reference not in url_set:
                url_set.add(reference)
                urls.append(reference)
            continue

        # update URLs
        for reference in references:
            if reference not in url_set:
                url_set.add(reference)
                urls.append(reference)

        # save results
        with open("result.txt", mode="a") as f:
            res = OrderedDict({
                "id": doc_id,
                "title": title,
                "year": year,
                "authors": authors,
                "abstract": abstract,
                "references": references
            })
            f.write(json.dumps(res))
            f.write("\n")

        # sleep before next request
        time.sleep(random.Random().uniform(0.5, 4))

    driver.quit()


if __name__ == '__main__':
    crawl()
