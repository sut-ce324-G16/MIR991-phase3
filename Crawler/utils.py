import random
import time

from bs4 import BeautifulSoup


class Extractor:
    @staticmethod
    def get_page_content(url, driver):
        driver.get(url)
        time.sleep(random.Random().uniform(1, 5))
        content = driver.page_source.encode('utf-8').strip()
        return BeautifulSoup(content, "html.parser")

    @staticmethod
    def extract_title(content: BeautifulSoup):
        return content.find("title").string.split("|")[0]

    @staticmethod
    def extract_year(content: BeautifulSoup):
        return content.find("span", attrs={"class": "year"}).string.strip()

    @staticmethod
    def extract_authors(content: BeautifulSoup):
        result = []

        authors_div = content.find("div", attrs={"class": "authors"})
        authors = authors_div.find_all("a", attrs={"class": "au-target author link"})
        for author in authors:
            result.append(author.text.strip())

        return result

    @staticmethod
    def extract_abstract(content: BeautifulSoup):
        abstract_caption = content.find("h3", attrs={"class": "caption"}, text="Abstract")
        return abstract_caption.find_next_sibling("p").text

    @staticmethod
    def extract_references(content: BeautifulSoup):
        result = []
        link_prefix = "https://academic.microsoft.com/"

        references = content.find_all("div", attrs={"class": "primary_paper"})
        for reference in references:
            rel_path = reference.find("a")['href'].split("/reference")[0]
            result.append(link_prefix + rel_path)

        return result
