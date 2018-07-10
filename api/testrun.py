from requests import request
import json
import logging

logger = logging.getLogger("apitest")


def run_test(method, url, data_format, params, expect, headers):
    params_data = None
    post_data = None

    # 解析参数数据
    if data_format == 'form':
        params = parse_data(params)

    if method.upper() == "POST":
        post_data = params
    elif method.upper() == "GET":
        params_data = params

    # 解析header数据
    header_data = parse_data(headers)

    resp = request(method, url, params=params_data, data=post_data, headers=header_data)
    logger.info(resp.status_code)
    if resp.status_code != 200:
        test_result = "Fail"
        response_data = resp.text
        return test_result, response_data

    if resp.text.count(expect) > 0:
        test_result = "Pass"
    else:
        test_result = "Fail"
    # resp_dic = resp.json()
    # for expect_key, expect_value in json.loads(expect).items():
    #     if resp_dic.get(expect_key) is not None:
    #         if resp_dic[expect_key] == expect_value:
    #             test_result = "Pass"
    #         else:
    #             test_result = "Fail"
    #     else:
    #         test_result = "Fail"
    return test_result, resp.text


def parse_data(strs):
    data = json.loads(strs)
    dict_data = {}
    if data is not None:
        for h in data:
            dict_data[h.get('name')] = h.get('value')
    return dict_data

