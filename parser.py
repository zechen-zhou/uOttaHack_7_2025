# *********************************************************************************************
# FILE   NAME:    parser.py
# PROJ   NAME:    uOttaHack 7 - deepcode-challenge
# DESCRIPTION:    Parse breach data from large text files
#
# HOW TO USE:     $ python3 parser.py
#
#
# Contributors:
# - Zechen Zhou     zzhou186@uottawa.ca
# - Benjamin Sam    bsam079@uottawa.ca
#
#
# REVISION HISTORY
# YYYY/MMM/DD     Author                       Comments
# 2025 JAN 18     Zechen Zhou, Benjamin Sam    creation
#
#
#
# *********************************************************************************************

import ipaddress
import socket
import urllib
import urllib.parse
from typing import NamedTuple

import pandas as pd
import tldextract
import tqdm


class LineResult(NamedTuple):
    url: str
    username: str
    password: str
    routable: bool
    tld: str | None
    ip: str | None
    port: int | None
    is_local_ip: bool


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


def parse_line(line, resolve_ips=False, delay_resolve_ips_placeholder="LATER"):
    port = -1
    routable = True
    is_local_ip = False
    password, username, url = line[::-1].split(":", 2)
    url, username, password = url[::-1], username[::-1], password[::-1]
    extract = tldextract.extract(url)
    tld = extract.registered_domain
    # Check to see if the line refers to an android app
    if (
        line.startswith("android://")
        or tld == "android.app"
        or extract.suffix == "android"
        or (extract.subdomain.endswith(".android") and extract.suffix == "")
    ):
        tld = "android.app"
        ip = None
        routable = False
        # Can't verify port for an android app
        port = None
    elif tld == "":
        # the url is an IP address, not a domain
        tld = None
        try:
            ip = ipaddress.ip_address(extract.domain)
            routable = not ip.is_private
        except Exception:
            # If this isn't a recognizable Android app and it isn't a valid IP
            # or domain name, then don't bother determining the port and return
            # whatever data has currently been determined
            return LineResult(
                url, username, password, False, None, None, None, is_local_ip
            )
    else:
        if resolve_ips:
            try:
                ip = socket.gethostbyname(tld)
            except socket.gaierror:
                # If there's an error looking up the TLD, set the IP to None
                ip = None
        else:
            ip = delay_resolve_ips_placeholder  # We'll figure out the IPs of valid domains n parallel later
    # Get the port
    urlp = urllib.parse.urlparse(url)
    # If the port has still not been assigned a valid value, attempt to determine it
    if port is not None:
        # If urlparse can determine the port from the URL use it
        if urlp.port is not None:
            port = urlp.port
        # If the scheme is http or https make a reasonable assumption of the default ports
        elif urlp.scheme == "https" or urlp.scheme == "http":
            port = 80 if urlp.scheme == "http" else 443
        # Otherwise, let the port be None to indicate that the port number
        # can't be reliably determined (e.g. if the line is an Android app, if
        # it contains a domain (that maps to an IP) but no scheme (e.g. FTP,
        # RTSP, etc.), etc.)
        else:
            port = None
    return LineResult(
        url,
        username,
        password,
        routable,
        tld,
        ip if ip is None else str(ip),
        port,
        is_local_ip,
    )


def parse_file(
    fname,
    skippable_lines=None,
    skip_on_error=False,
    return_nones=False,
    return_pandas=True,
):
    with open(fname, encoding="utf-8") as f:
        lines = f.read().splitlines()

    parsed_lines = []
    for line in tqdm.tqdm(lines):
        try:
            parsed = parse_line(line, resolve_ips=False)
        except Exception as e:
            if skip_on_error:
                continue
            elif skippable_lines is not None and line in skippable_lines:
                continue
            else:
                raise RuntimeError(f"Failed to parse line: {line}") from e
        parsed_lines.append(parsed)
    if not return_nones:
        parsed_lines = [item for item in parsed_lines if item is not None]
    if return_pandas:
        return pd.DataFrame(parsed_lines)
    return parsed_lines


if __name__ == "__main__":
    parse_file("sample.txt", skippable_lines=CAN_SKIP_SAMPLE_TXT)
