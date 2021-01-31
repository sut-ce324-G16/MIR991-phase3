import random
import time

from bs4 import BeautifulSoup


def pars_link(link):
    link = link.split("/reference")[0]

    link_prefix = "https://academic.microsoft.com/"
    if not link.startswith(link_prefix):
        link = link_prefix + link

    return link


class BadPaperException(Exception):
    pass


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
        if abstract_caption is None:
            raise BadPaperException(Extractor.extract_other_versions(content))
        return abstract_caption.find_next_sibling("p").text

    @staticmethod
    def extract_references(content: BeautifulSoup):
        # check references count
        data_divs = content.find_all("div", attrs={"class": "data"})
        for div in data_divs:
            name = div.find("div", attrs={"class": "name"}).text.strip()
            if name.lower() == "references":
                count = int(div.find("div", attrs={"class": "count"}).text.strip())
                if count == 0:
                    return []
                break

        result = []

        references = content.find_all("div", attrs={"class": "primary_paper"})
        for reference in references:
            result.append(pars_link(reference.find("a")['href']))

        return result

    @staticmethod
    def extract_other_versions(content: BeautifulSoup):
        other_versions_caption = content.find("h3", attrs={"class": "caption"}, text="Other Versions")
        if other_versions_caption is None:
            return ""

        link_div = other_versions_caption.find_next_sibling("div")
        return pars_link(link_div.find("a")['href'])
