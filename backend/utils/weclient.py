# -*-coding:utf-8 -*-
from urllib import urlencode
import requests
from simplejson.errors import JSONDecodeError
from requests.exceptions import BaseHTTPError


class WeHttpClient(object):
    """
       发送http请求获取结果，可以返回整个整个请求的相关信息的json串
    """
    def __init__(self, host, headers={}, params=None, files=None):
        self.url = host
        self.headers = headers
        self.params = params
        self.files = files

    def send(self, method='GET'):
        # 跟据请求参数确认请求地址,送发送不同类型的请求
        address = self.url + '?' + urlencode(self.params) \
            if self.params is not None and (method == 'GET' or method == 'DELETE') else self.url
        if method == 'GET':
            return requests.get(address, headers=self.headers)
        elif method == 'DELETE':
            return requests.delete(address, headers=self.headers)
        elif method == 'POST':
            return requests.post(address,
                                 data=self.params,
                                 headers=self.headers,
                                 files=self.files,
                                 allow_redirects=True)
        elif method == 'PUT':
            return requests.put(address,
                                data=self.params,
                                headers=self.headers,
                                files=self.files,
                                allow_redirects=True)
        else:
            raise ValueError(u'method is must be in ["GET", "POST", "PUT", "DELETE"]')
        return None

    def http_header(self, method="GET"):
        """
        :param method: 请求方法
        :return:
        """
        res = self.send(method=method)
        data = res.headers
        return data

    def body(self, method="GET"):
        """
        将请求结果分类为Json和html
        :param method: 请求方法
        :return:
        """
        res = self.send(method=method)
        try:
            content = res.json()
            result_type = 'json'
        except JSONDecodeError:
            content = res.content
            result_type = 'html'
        except BaseHTTPError as e:
            result_type = 'error'
            content = e
        return {'type': result_type, 'content': content}

    def result(self, method="GET"):
        """
        初始化请求的接口数据
        :param method: 请求方法
        :return:
        """
        try:
            res = self.send(method=method)
            content = res.json()
            result_type = 'json'
        except JSONDecodeError:
            content = res.content.decode('utf-8')
            result_type = 'html'
        except Exception as e:
            result_type = 'error'
            content = str(e)
            return None
        request_result = {
            'url': res.url,
            'time': res.elapsed.microseconds/1000,
            'body': {'type': result_type, 'content': content},
            'status': res.status_code,
            'headers': res.headers
        }
        return request_result