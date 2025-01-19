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

# Define lines in the sample file which we can skip (since we're allowed to
# just skip lines that are too messy)
CAN_SKIP_SAMPLE_TXT = {
    "https://www.eprimo.de:::karinkuepper@hotmail.de:Diddilein.0815:Profiles:h1uuk71a.default-1551943278195",
    "https://www.facebook.com:::damianurrea@yahoo.com:cocoloco87:Profiles:1lyubw9l.default-1514016732105",
}


def parse_line(line, skippable_lines=None, get_ip=False, delay_ip_placeholder="LATER"):
    if skippable_lines is not None and line in skippable_lines:
        return None
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
            if get_ip:
                try:
                    ip = socket.gethostbyname(tld)
                except socket.gaierror:
                    # If there's an error looking up the TLD, set the IP to None
                    ip = None
            else:
                ip = delay_ip_placeholder  # We'll figure out the IPs of valid domains n parallel later
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

    parsed_lines = []
    for line in tqdm.tqdm(lines):
        parsed = parse_line(line, skippable_lines=CAN_SKIP_SAMPLE_TXT)
        parsed_lines.append(parsed)


if __name__ == "__main__":
    parse_file("sample.txt")
