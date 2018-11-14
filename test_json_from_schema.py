#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json

import faker
import jsonschema
import requests
from jsonschema.exceptions import ValidationError

import jsonprovider


def generate_request(request_json_schema):
    '''
    通过schema生成随机测试数据
    :param request_json_schema:
    :return:
    '''
    fake = faker.Faker()
    fake.add_provider(jsonprovider.JSONProvider)
    request_body = fake.json(json.load(open(request_json_schema)))
    print(request_body)
    return request_body


def check_json_schema(response, schema):
    '''
    通过json_schema检查返回的json串
    :param response:
    :param schema:
    :return:
    '''
    result = True
    try:
        jsonschema.validate(response, schema)
    except ValidationError, e:
        print("fail")
        result = False
    return result


if __name__ == '__main__':
    # 生成request body
    body = generate_request("schema_file/create_config_request_schemas.json")
    # 使用request库发送post请求
    url = "https://dev.honcloud.honeywell.com.cn:8080/dashboard/clustercentre/configmng/newconfig/addconfig"
    headers = {"Content-Type": "application/json", "authorization": "48a5eb61-914e-4b3a-a7a3-0b25f72d06d7"}
    response = requests.post(url, data=body, headers=headers)
    print(response.json())
    response_json=response.json()
    response_schema="schema_file/create_config_response_schemas.json"
    # 用生成的response的schema来检查
    result=check_json_schema(response_json,response_schema)
    print(result)

