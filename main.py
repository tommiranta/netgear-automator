import configparser
import logging
import os
import sys
from base64 import b64encode

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def get_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


def basic_auth(username, password):
    # https://stackoverflow.com/questions/6999565/python-https-get-with-basic-authentication
    token = b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def get_session(config):
    token = basic_auth(
        os.environ.get("NETGEAR_USERNAME"), os.environ.get("NETGEAR_PASSWORD")
    )
    s = requests.sessions.Session()
    res = s.get(f"{config.get('base_url')}/{config.get('start_page')}")

    s.headers.update(
        {
            "Authorization": token,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        }
    )

    if config.get("confirm_login_page") in res.url:
        logging.info("Force login.")
        form_action = get_form_action_url(
            s,
            f"{config.get('base_url')}/{config.get('confirm_login_page')}",
        )
        write_settings(
            s,
            f"{config.get('base_url')}/{form_action}",
            config.get("confirm_login_data"),
        )
    return s


def get_form_action_url(s, url):
    r = s.get(url)
    r.raise_for_status()

    soup = BeautifulSoup(r.content, "html.parser")
    form = soup.css.select("#target")
    tag = form.pop()
    action = tag.attrs.get("action")

    return action


def write_settings(s, url, data):
    r = s.post(
        url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=data,
    )
    r.raise_for_status()


def main(args):
    load_dotenv()
    config = get_config()

    if len(args) > 1:
        command = args[1]
        if command not in config:
            logging.error("Invalid action provided. Check your config.ini.")
            sys.exit(1)
    else:
        logging.error("No action provided. Choose one defined in the configuration.")
        sys.exit(1)

    action = config[command]
    # [print(k) for k, v in action.items()]
    s = get_session(action)
    form_action = get_form_action_url(
        s,
        f"{action.get('base_url')}/{action.get('page')}",
    )
    write_settings(s, f"{action.get('base_url')}/{form_action}", action.get("data"))


if __name__ == "__main__":
    main(sys.argv)
