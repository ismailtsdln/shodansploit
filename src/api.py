import requests
import json

class ShodanAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.shodan.io"
        self.exploit_url = "https://exploits.shodan.io/api"

    def _request(self, url, params=None):
        """
        Generic request handler with error handling.
        """
        if params is None:
            params = {}
        
        params['key'] = self.api_key
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        except ValueError:
            return {"error": "Failed to decode JSON response"}

    # Host API
    def host(self, ip):
        return self._request(f"{self.base_url}/shodan/host/{ip}")

    def host_count(self, query):
        return self._request(f"{self.base_url}/shodan/host/count", params={"query": query})

    def host_search(self, query):
        return self._request(f"{self.base_url}/shodan/host/search", params={"query": query})

    def host_tokens(self, query):
        return self._request(f"{self.base_url}/shodan/host/search/tokens", params={"query": query})

    def ports(self):
        return self._request(f"{self.base_url}/shodan/ports")

    # DNS API
    def dns_resolve(self, hostnames):
        return self._request(f"{self.base_url}/dns/resolve", params={"hostnames": hostnames})

    def dns_reverse(self, ips):
        return self._request(f"{self.base_url}/dns/reverse", params={"ips": ips})

    # Labs API
    def honeyscore(self, ip):
        return self._request(f"{self.base_url}/labs/honeyscore/{ip}")

    # Account & Tools API
    def profile(self):
        return self._request(f"{self.base_url}/account/profile")

    def myip(self):
        return self._request(f"{self.base_url}/tools/myip")

    def httpheaders(self):
        return self._request(f"{self.base_url}/tools/httpheaders")

    def api_info(self):
        return self._request(f"{self.base_url}/api-info")

    # Exploits API
    def exploit_search(self, query_type, query):
        q = f"{query_type}:{query}"
        return self._request(f"{self.exploit_url}/search", params={"query": q})
