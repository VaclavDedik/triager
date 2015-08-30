import requests


class Jira(object):
    def __init__(self, url):
        self.url = url

    def find_all(self, jql, fields=None, offset=0, limit=None):
        # Prepare request url
        get_url = self.url
        if not get_url.endswith("/"):
            get_url += "/"

        get_url += "search?jql=%s" % jql

        if fields:
            get_url += "&fields=%s" % fields
        if offset:
            get_url += "&startAt=%s" % offset
        if limit:
            get_url += "&maxResults=%s" % limit

        # Execute request
        r = requests.get(get_url)
        if not r.ok:
            r.raise_for_status()

        # Parse json
        issues = r.json()['issues']
        return issues
