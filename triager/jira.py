import requests


class Jira(object):
    def __init__(self, url):
        self.url = url

    def find_all(self, jql, fields=None, offset=0, limit=1000):
        # Prepare request url
        get_url = self.url
        if not get_url.endswith("/"):
            get_url += "/"

        get_url += "search?jql=%s" % jql

        if fields:
            get_url += "&fields=%s" % fields

        get_url_wlimit = get_url
        if offset:
            get_url_wlimit += "&startAt=%s" % offset
        if limit:
            get_url_wlimit += "&maxResults=%s" % limit

        # Execute request
        result = self.get_request(get_url_wlimit)
        issues = result['issues']

        # Partition if offset on server limited
        if result['maxResults'] < limit:
            new_limit = result['maxResults']
            new_offset = offset + new_limit
            total = result['total']
            
            while new_offset < limit and new_offset < total:
                new_get_url = get_url + "&startAt=%s&maxResults=%s" \
                    % (new_offset, new_limit)
                curr_result = self.get_request(new_get_url)
                issues += curr_result['issues']
                new_offset += new_limit

        return issues

    def get_request(self, url):
        r = requests.get(url)
        if not r.ok:
            r.raise_for_status()

        return r.json()
