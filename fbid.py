import urllib.request as request
import re

def get_id(alias):
    id_regex = r"(?:page_id|profile_id)=(\d+)"
    print(f"Getting ID of {alias}...")
    response = request.urlopen(f"https://www.facebook.com/{alias}")
    page_source = response.read().decode("utf-8")
    id = re.search(id_regex, page_source).group(1)
    return id