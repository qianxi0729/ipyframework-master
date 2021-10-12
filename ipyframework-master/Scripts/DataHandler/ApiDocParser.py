#!/usr/bin/python
# coding=utf-8
# Copyright 2018 yaitza. All Rights Reserved.
#
#     https://yaitza.github.io/
#
# My Code hope to useful for you.
# ===================================================================

from json import load
from urllib import request
import os
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.level = logging.DEBUG

__author__ = "yaitza"
__date__ = "2018-07-10 17:45"

test_suite_mapping = {
    u'产品模块接口': 'product',
    u'内容管理接口': 'cms',
    u'商品模块接口': 'good',
    u'商机意向模块接口': 'intention',
    u'地区接口': 'area',
    u'客服模块': 'online_service',
    u'权限模块接口': 'departments',
    u'消息模块接口': 'messages',
    u'用户模块接口': 'accounts',
    u'认证模块接口': 'auth',
    u'大屏机消息转发模块': 'board',
    u'预约试驾模块接口': 'drive',
    u'预置消息模块接口': 'predefine_message',
    u'定时调度模块接口': 'schedule',
    u'服务模块': 'service',
    u'服务招请': 'station_service',
    u'系统模块接口': 'system',
    u'车辆模块': 'trucks',
    u'钱包模块接口': 'wallet',
    u'操作日志模块接口': 'operate_log',
    u'视频模块APP接口': 'video_App',
    u'视频模块WEB接口': 'video_web',
    u'用户开票信息接口': 'invoices',
    u'重卡论坛对接模块': 'bbs',
    u'优惠券模块接口': 'coupon',
    u'内容接口': 'contents',
    u'发运模块接口': 'deliver',
    u'金融模块': 'CreditWorthiness',
    u'地区接口': 'area',
    u'系统模块接口': 'System',
    u'内容管理接口': 'cms',
    u'体验店模块': 'Sales_Shop',
    u'untagged': 'untagged'
}

robot_template_content = "*** Settings ***\n" \
                         "Documentation\n" \
                         "...    suit: %s\n" \
                         "...    name: %s\n" \
                         "...    version: %s\n" \
                         "...    type: %s\n\n" \
                         "Resource    ../../resources/requests.robot\n\n" \
                         "*** Variables ***\n" \
                         "${TEST_DATA_PATH}    ${CURDIR}/../../test_data/%s\n\n" \
                         "*** Test Cases ***\n" \
                         "Default Query\n" \
                         "    [tags]  TODO\n" \
                         "    log  TODO\n" \
                         "#    [Template]  GET WITH PARAMETERS  \n" \
                         "%s  ${TEST_DATA_PATH}/%s.json"


class ApiDocParser(object):
    """ 解析Swagger接口返回接口 """

    def __init__(self, api_url):
        self.url = api_url
        self.swagger_api_data = {}

    def load_url(self):
        with request.urlopen(self.url, None, 30) as apiJson:
            swagger_all_api = load(apiJson)["paths"]

        for api_item in swagger_all_api:
            if not api_item.__contains__("mock"):  # 排除mock接口
                self.swagger_api_data[api_item] = swagger_all_api[api_item]

    @staticmethod
    def is_require_modules(actual_modules, require_modules=None):
        if (require_modules is not None) and (not (actual_modules == require_modules)):
            return False
        return True

    def generate_api_robot(self, version=None, modules=None):
        """ 生成模板robot """
        api_robot = {}
        for api_item in self.swagger_api_data:
            api_info = self.swagger_api_data[api_item]
            for request_type in api_info:
                api_robot_name = ("%s%s" % (request_type, api_item)).replace('/', '_')
                api_modules = api_info[request_type]["tags"][0]
                api_summary = api_info[request_type]["summary"]
                api_name = "Default"
                api_version = "V0.0.0"
                api_change_type = "Exist"
                if api_summary.count('|') == 2:
                    api_name = api_summary.split('|')[0]
                    api_version = api_summary.split('|')[1]
                    api_change_type = api_summary.split('|')[2]
                if is_require_version(api_version, version) and self.is_require_modules(api_modules, modules):
                    robot_template_content_tmp = robot_template_content
                    if not test_suite_mapping.__contains__(api_modules):
                        logger.exception("%s not in %s" % (api_modules, test_suite_mapping.__str__()))
                        continue
                    robot_template_content_tmp = robot_template_content_tmp % (test_suite_mapping[api_modules] +
                                                                               "-" + api_modules,
                                                                               api_name, api_version, api_change_type,
                                                                               test_suite_mapping[api_modules],
                                                                               api_item, api_robot_name)
                    api_robot[test_suite_mapping[api_modules] + "|" + api_robot_name] = robot_template_content_tmp
        return api_robot

    def generate_api_expect_json(self, version=None, modules=None):
        """ 根据swagger生成模板测试数据 """
        api_json = {}
        for api_item in self.swagger_api_data:
            api_info = self.swagger_api_data[api_item]
            for request_type in api_info:
                api_json_name = ("%s%s" % (request_type, api_item)).replace('/', '_')
                api_json_dict = {}
                api_modules = api_info[request_type]["tags"][0]
                api_summary = api_info[request_type]["summary"]
                api_version = None
                api_header = {}
                api_parameter = {}

                if api_summary.__contains__('|'):
                    api_version = api_summary.split('|')[1]

                if is_require_version(api_version, version) and self.is_require_modules(api_modules, modules):
                    print(api_summary)
                    if "parameters" in api_info[request_type]:
                        api_headers = api_info[request_type]["parameters"]
                        for parameter in api_headers:
                            if parameter["in"].__eq__("header"):    # 获取swagger中请求header
                                if 'default' in parameter.keys():
                                    api_header[parameter["name"]] = parameter["default"]
                                else:
                                    api_header[parameter["name"]] = ""

                            if parameter["in"].__eq__("query"):     # 获取swagger中查询入参
                                api_parameter[parameter["name"]] = ""

                        api_json_dict["header"] = api_header
                        api_json_dict["parameter"] = api_parameter
                    api_json_dict["code"] = 200
                    api_json_dict["response"] = {}
                    api_json[test_suite_mapping[api_modules] + "|" + api_json_name] = api_json_dict

        return api_json

    @staticmethod
    def output(api_item_robot, api_item_json, archiving_path=None):
        if isinstance(api_item_robot, dict) and isinstance(api_item_json, dict):
            for api_single in api_item_robot:
                module = api_single.split('|')[0]
                file_name = api_single.split('|')[1]
                directory_robot = "%s/Robot/rest_api/%s" % (archiving_path, module)
                if not os.path.isdir(directory_robot):
                    os.makedirs(directory_robot)

                directory_python = "%s/Robot/test_data/%s" % (archiving_path, module)
                if not os.path.isdir(directory_python):
                    os.makedirs(directory_python)

                path_robot = "%s/Robot/rest_api/%s/%s.robot" % (archiving_path, module, file_name)
                with open(path_robot, 'w', encoding='utf8') as f:
                    f.write(api_item_robot[api_single])
                path_json = "%s/Robot/test_data/%s/%s.json" % (archiving_path, module, file_name)
                with open(path_json, 'w', encoding='utf8') as f:
                    f.write(api_item_json[api_single].__str__().replace('\'', "\""))


def is_require_version(actual_version, require_version=None):
    if (require_version is not None) and (not (actual_version == require_version)):
        return False
    return True


if __name__ == "__main__":
    api_json = ApiDocParser("http://test.31truck.aerohuanyou.com:9527/sany/v2/api-docs")
    api_json.load_url()
    item_list_robot = api_json.generate_api_robot(modules="优惠券模块接口")
    item_list_json = api_json.generate_api_expect_json(modules="优惠券模块接口")
    api_json.output(item_list_robot, item_list_json, r'D:\zh文档\自动化测试')
    # print(item_list.__len__())
