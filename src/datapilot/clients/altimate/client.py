import logging

import requests


class APIClient:
    def __init__(self, api_token="", base_url="", tenant=""):
        self.api_token = api_token
        self.base_url = base_url
        self.tenant = tenant
        self.logger = logging.getLogger(self.__class__.__name__)

    def _get_headers(self):
        headers = {
            "Content-Type": "application/json",
        }

        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"

        if self.tenant:
            headers["x-tenant"] = self.tenant

        return headers

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        self.logger.debug(f"Sending GET request for tenant {self.tenant} at url: {url}")
        print(f"Sending GET request for tenant {self.tenant} at url: {url}")
        response = requests.get(url, headers=headers, params=params)
        self.logger.debug(f"Received GET response with status: {response.status_code }")
        return response.json() if response.status_code == 200 else None

    def post(self, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        self.logger.debug(f"Sending POST request for tenant {self.tenant} at url: {url}")
        response = requests.post(url, headers=headers, json=data)
        self.logger.debug(f"Received POST response with status: {response.status_code }")

        return response

    def put(self, endpoint, data):
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        self.logger.debug(f"Sending PUT request for tenant {self.tenant} at url: {url}")
        response = requests.put(url, data=data)
        self.logger.debug(f"Received PUT response with status: {response.status_code}")
        return response