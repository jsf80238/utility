import re
from playwright.sync_api import Browser, Page, expect, sync_playwright

BASE_SEARCH_STRING = "https://www.google.com/search?q="

extra_list = ("jobs", "careers")

employer_list = (
    "humana",
    "comerica",
)


def get_link_with_name(page: Page, name: str) -> str:
    for link in page.get_by_role("link", name=name).all():
        return link.get_attribute('href')
        break
    return None


def search_employer(browser: Browser, name: str) -> list:
    result = list()
    page = browser.new_page()
    for extra in extra_list:
        full_search_string = BASE_SEARCH_STRING + name + "+" + extra
        page.goto(full_search_string, timeout=10000)
        result.append(get_link_with_name(page, name))
        if result:
            break
    page.close()
    return result


with sync_playwright() as p, p.chromium.launch() as browser:
    for employer_name in employer_list:
        print()
        print(employer_name)
        print(search_employer(browser, employer_name))
