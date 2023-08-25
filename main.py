import logging
import os
import sys
from base64 import b64encode

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://www.routerlogin.net"
CMD_MAPPING = {
    "enable": "always",
    "disable": "never",
}


def basic_auth(username, password):
    # https://stackoverflow.com/questions/6999565/python-https-get-with-basic-authentication
    token = b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def get_session():
    token = basic_auth(
        os.environ.get("NETGEAR_USERNAME"), os.environ.get("NETGEAR_PASSWORD")
    )
    s = requests.sessions.Session()
    _ = s.get(f"{BASE_URL}/start.htm")

    s.headers.update(
        {
            "Authorization": token,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        }
    )
    return s


def get_form_action(s):
    r = s.get(
        f"{BASE_URL}/BKS_service.htm",
    )
    r.raise_for_status()

    soup = BeautifulSoup(r.content, "html.parser")
    form = soup.css.select("#target")
    tag = form.pop()
    action = tag.attrs.get("action")

    return action


def write_settings(s, form_action, value):
    r = s.post(
        f"{BASE_URL}/{form_action}",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=f"apply=Apply&skeyword={value}&ruleSelect=0&select=-1",
    )
    r.raise_for_status()


def main(args):
    if len(args) > 1:
        command = CMD_MAPPING.get(args[1])
        if not command:
            logging.error(
                "No input command provided. Should be either `enable` or `disable`"
            )
            sys.exit(1)
    else:
        logging.error(
            "No input command provided. Should be either `enable` or `disable`"
        )
        sys.exit(1)

    s = get_session()
    form_action = get_form_action(s)
    write_settings(s, form_action, command)


if __name__ == "__main__":
    main(sys.argv)
