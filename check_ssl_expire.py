from urllib.request import ssl, socket
from datetime import datetime

check_url_file = str("url_check_23.conf")
url_dict = {}


def url_to_dict():
    with open(check_url_file, "r") as cf:
        for line in cf:
            if line.startswith("#") or line.lstrip() == "":
                continue
            else:
                LINE_LIST = line.split(":")
                check_port = LINE_LIST[1].rstrip()
                url_dict[LINE_LIST[0]] = check_port


context = ssl.create_default_context()


def check_expire():
    for hostname, port in url_dict.items():
        url = hostname
        try:
            with socket.create_connection((url, port), timeout=2) as sock:
                with context.wrap_socket(sock, server_hostname=url) as ssock:
                    IP_ADDR = socket.gethostbyname(url)
                    cert_data = ssock.getpeercert()
                    expire_date = cert_data["notAfter"]
                    serial_number = cert_data["serialNumber"]
                    print("{0:<20} {1:<15} (Expire Date: {2}, Serial Number: {3})".format(url, IP_ADDR, expire_date, serial_number))
        except socket.timeout:
            print("{0:<20s} Connection timed out".format(url))
        except Exception as e:
            print("{0:<20s} Error: {1}".format(url, str(e)))


if __name__ == "__main__":
    url_to_dict()
    check_expire()