import ipaddress
import socket
import urllib
import urllib.parse
from typing import NamedTuple

import tldextract
import tqdm


class LineResult(NamedTuple):
    url: str
    username: str
    password: str
    routable: bool
    tld: str | None
    ip: str
    port: int


# TODO:
# - handle for Android/non-standard URLs properly
#   - can check the suffix with tldextract?
# - get the title of webpages


def parse_line(line):
    try:
        port = -1
        routable = True
        password, username, url = line[::-1].split(":", 2)
        url, username, password = url[::-1], username[::-1], password[::-1]
        extract = tldextract.extract(url)
        tld = extract.registered_domain
        if tld == "android.app" or extract.suffix == "android":
            ip = None
            routable = False
            # Can't verify port for an android app
            port = None
        elif tld == "":
            # the url is an IP address, not a domain
            tld = None
            try:
                ip = ipaddress.ip_address(extract.domain)
                routable = ip.is_private
            except Exception:
                # If we can't find the IP address or the domain, we can't
                # insert the data into our table schema. Consider the line to
                # be invalid and skip it
                return None
        else:
            # try:
            ###     ip = socket.gethostbyname(tld)
            # except socket.gaierror:
            #     # If there's an error looking up the TLD, set the IP to None
            #     ip = None
            ip = "LATER"
        # Get the port
        urlp = urllib.parse.urlparse(url)
        if port is not None:
            if urlp.port is not None:
                port = urlp.port
            else:
                if urlp.scheme == "https" or urlp.scheme == "http":
                    port = 80 if urlp.scheme == "http" else 443
                else:
                    port = 99999
        return LineResult(url, username, password, routable, tld, str(ip), port)
    except Exception as e:
        raise RuntimeError(f"Failed on: {line}") from e


def parse_file(fname):
    with open(fname) as f:
        lines = f.read().splitlines()
    for line in tqdm.tqdm(lines):
        parse_line(line)


if __name__ == "__main__":
    parse_file("sample.txt")
