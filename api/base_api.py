import requests


class BaseAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def _get(self, path: str = '/'):
        resp = requests.get(url=f"{self.base_url}/{path}")
        return resp

    def _post(self, json: dict, path: str = '/', data: dict = None, params: dict = None):
        resp = requests.post(url=f"{self.base_url}/{path}", json=json, data=data, params=params)
        return resp

    def _put(self, json: dict, path: str = '/', data: dict = None, params: dict = None):
        resp = requests.put(url=f"{self.base_url}/{path}", json=json, data=data, params=params)
        return resp

    def _patch(self, json: dict, path: str = '/', data: dict = None, params: dict = None):
        resp = requests.patch(url=f"{self.base_url}/{path}", json=json, data=data, params=params)
        return resp

    def _delete(self, json: dict, path: str = '/', data: dict = None, params: dict = None):
        resp = requests.delete(url=f"{self.base_url}/{path}", json=json, data=data, params=params)
        return resp
