""" Link-Checker
Author: Finn LeSueur
Last Modified: 11/04/2020
"""

import configparser
from datetime import datetime
import re
import requests
from email.mime.text import MIMEText
from subprocess import Popen, PIPE
import sys

URLS = {}

def main():
    """ Control the script. """
    start_time = datetime.now()

    config = configparser.ConfigParser()
    config.read("config")
    if len(sys.argv) == 2:
        sitemap = sys.argv[1]
    else:
        sitemap = config["default"]["sitemap_url"]
    raw = requests.get(sitemap)

    responses = {}
    responses["all_urls"] = {}
    responses["pages"] = {}

    pages = parse_sitemap(raw.text)
    page_count = 1
    for page in pages[:2]:
        urls = get_text_of(page)
        responses = check_page_anchors(page, urls, responses)
        page_count += 1
    output(responses, start_time, config)


def parse_sitemap(sitemap):
    """ Parses a sitemap as text
    for all page URLs and returns them.
    """
    return re.findall(r'<loc>(.*)<\/loc>', sitemap)

def get_text_of(page):
    """ Takes a URL and requests that URL,
    and returns its sitemap.
    """
    raw = requests.get(page)
    return get_html_achors_of(raw.text)

def get_html_achors_of(text):
    """ Finds and returns all URLs from
    anchor elements in HTML text.
    """
    return re.findall(r'<a.*href=\"(\S*)\".*>.*</a>', text)

def check_page_anchors(page, links, responses):
    """ Checks the status of a URL and
    diligently fills out the dicitonary
    containing all the responses.
    """
    p = dict()
    p["good"] = 0
    p["bad"] = 0
    p["errors"] = dict()
    for link in links:
        if link not in responses["all_urls"]:
            try:
                raw = requests.get(link)
                responses["all_urls"][link] = raw.status_code
            except:
                responses["all_urls"][link] = "unknown"
        if responses["all_urls"][link] == requests.codes.ok:
            p["good"] += 1
        else:
            p["bad"] += 1
            p["errors"][link] = responses["all_urls"][link]
    responses["pages"][page] = p
    return responses

def output(responses, start_time, config):
    """ Reads through the dictionary of
    responses and makes a nice output
    to send to a file.
    """
    passed = 0
    failed = 0
    errors = "Pages with Errors (status code & URL):\n"
    okays = "\nPages without Errors:\n"
    for page in responses["pages"]:
        if responses["pages"][page]["bad"] == 0:
            passed += 1
            okays += "    {0}\n".format(page)
        else:
            failed += 1
            errors += "\n{0}\n".format(page)
            for url in responses["pages"][page]["errors"]:
                errors += "    ({0}): {1}\n".format(responses["pages"][page]["errors"][url], url)

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H%m%S")
    with open("reports/{0}.txt".format(dt_string), 'w') as file:
        file.write("Summary\n    Check took {2}s\n    Pages with Errors: {0}\n    Pages without Errors: {1}\n\n".format(failed, passed, datetime.now() - start_time))
        file.write(errors)
        file.write(okays)
    file.close() 

    if config["default"]["email_log"]:
        with open("reports/{0}.txt".format(dt_string), 'r') as content_file:
            content = content_file.read()
        msg = MIMEText(content)
        msg["From"] = config["default"]["from_email"]
        msg["To"] = config["default"]["to_email"]
        msg["Subject"] = config["default"]["email_subject"]
        p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
        p.communicate(msg.as_string().encode())

if __name__ == "__main__":
    main()
