#!/usr/bin/python
# coding=utf-8

__version__ = "1.0.0"

from json import loads
import requests
from robot.api.deco import keyword
from robot.api.deco import library
from Utils.Logger import LOGGER

@library
class RequestsKeywords(object):
    
    ROBOT_LIBARARY_SCOPE = "GLOBAL"
    """
    Http requests api keywords.
    """
    def __init__(self, url):
        self.url = url
        self.response = None

    @keyword(name="set url", tags=['requests'])
    def set_url(self, url):
        if url:
            self.url = url

    @keyword(name="get full url", tags=['requests'])
    def get_full_url(self, url):
        url_separator = '' if url.startswith('/') else '/'
        full_url = '{}{}{}'.format(self.url, url_separator, url)
        LOGGER.debug("get {0}".format(full_url))
        return full_url

    @keyword(name="get", tags=['requests'])
    def get(self, url, params=None, **kwargs):
        full_url = self.get_full_url(url)
        try:
            self.response = requests.get(full_url, params=params, **kwargs)
        except requests.RequestException as e:
            LOGGER.error(r"unable to get page content: {}".format(e))
            raise requests.RequestException(exc=e)
        return self.response

    @keyword(name="post", tags=['requests'])
    def post(self, url, data=None, json=None, **kwargs):
        full_url = self.get_full_url(url)
        self.response = requests.post(full_url, data=data, json=json, **kwargs)
        return self.response

    @keyword(name="patch", tags=['requests'])
    def patch(self, url, data=None, **kwargs):
        full_url = self.get_full_url(url)
        self.response = requests.patch(full_url, data=data, **kwargs)
        return self.response

    @keyword(name="put", tags=['requests'])
    def put(self, url, data=None, **kwargs):
        full_url = self.get_full_url(url)
        self.response = requests.put(full_url, data=data, **kwargs)
        return self.response

    @keyword(name="delete", tags=['requests'])
    def delete(self, url, **kwargs):
        full_url = self.get_full_url(url)
        self.response = requests.delete(full_url, **kwargs)
        return self.response

    @keyword(name="put file", tags=['requests', 'http'])
    def put_file(self, url, upload_files, header=None, params=None):
        full_url = self.get_full_url(url)
        if os.path.exists(upload_files) is False:
            raise AssertionError("{} not exists!".format(upload_files))

        files = {"file": open(upload_files, 'rb')}
        self.response = requests.put(full_url, files=files, headers=header, params=params)
        return self.response

    @keyword(name="post file", tags=['requests', 'http'])
    def post_file(self, url, upload_files, data=None, json=None, **kwargs):
        full_url = self.get_full_url(url)
        if os.path.exists(upload_files) is False:
            raise AssertionError("{} not exists!".format(upload_files))
        files = {'file': open(upload_files, 'rb')}
        self.response = requests.post(full_url, files=files, data=data, json=json, *kwargs)
        return self.response

    @keyword(name="get http code", tags=['requests'])
    def get_http_code(self):
        r"""Get response Http Status Code
        :return: Http Status Code
        """
        return self.response.status_code

    @keyword(name="get response code", tags=['requests'])
    def get_response_code(self):
        r"""Get response text code
        :return: Response Code
        """
        response_text_dict = loads(self.response.text)
        return response_text_dict['code']

    @keyword(name="get response text", tags=['requests'])
    def get_response_text(self):
        r"""Get response text
        :return: Http response text
        """
        return self.response.text

    @keyword(name="get response file", tags=['requests'])
    def get_response_file(self, file_dir, file_name):
        r"""Get response file
        :param file_dir: File directory
        :param file_name: File name
        :return: File paths
        """
        file = '{}/{}'.format(file_dir, file_name)
        if os.path.exists(file):
            LOGGER.console("删除文件：" + file)
            os.remove(file)
        Logger.console(file)
        with open(file, "wb") as f:
            for chunk in self.response.iter_content(1024):
                f.write(chunk)
        return file


if __name__ == "__main__":
    r = RequestsKeywords("https://www.baidu.com/")
    headers = {'Accept': '*/*'}
    r.get('/')
    print(r.get_http_code())
    print(r.get_response_text())
