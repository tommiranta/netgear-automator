import logging
import os
import sys
from base64 import b64encode

from playwright.sync_api import sync_playwright

BASE_URL = "http://www.routerlogin.net"


def basic_auth(username, password):
    # https://stackoverflow.com/questions/6999565/python-https-get-with-basic-authentication
    token = b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def find_element_by_attribute_value(page, role, attribute, value):
    elements = page.get_by_role(role).all()
    for element in elements:
        attribute_value = element.get_attribute(attribute)
        if attribute_value == value:
            return element


def select_radio_element(page, value):
    element = find_element_by_attribute_value(page, "radio", "value", value)
    if element:
        element.click()
        logging.info(f"selected {value}")


def click_button(page, value):
    element = find_element_by_attribute_value(page, "button", "value", value)
    if element:
        element.click()
        logging.info(f"clicked {value}")


def main(args):
    if len(args) > 1:
        command = args[1]
        if command not in ["enable", "disable"]:
            logging.error(
                "No input command provided. Should be either `enable` or `disable`"
            )
            sys.exit(1)
    else:
        logging.error(
            "No input command provided. Should be either `enable` or `disable`"
        )
        sys.exit(1)

    with sync_playwright() as p:
        token = basic_auth(
            os.environ.get("NETGEAR_USERNAME"), os.environ.get("NETGEAR_PASSWORD")
        )

        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{BASE_URL}/start.htm")
        context.set_extra_http_headers(
            {
                "Authorization": token,
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            }
        )
        page.goto(f"{BASE_URL}/BKS_service.htm")

        if command == "enable":
            select_radio_element(page, "always")
        else:
            select_radio_element(page, "never")
        click_button(page, "Apply")


if __name__ == "__main__":
    main(sys.argv)
