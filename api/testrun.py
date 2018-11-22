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
    # expect_dict = json.loads(expect)
    check_field = ""
    result = False
    for expect_dict in json.loads(expect):
        if expect_dict.get('field') == 'content':
            check_field = resp.text
        elif expect_dict.get('field') == 'status':
            check_field = resp.status_code
        elif expect_dict.get('field') == 'header':
            check_field = str(resp.headers)
        elif expect_dict.get('specifiedField'):
            query = expect_dict.get("specifiedField")
            check_field = query_json(resp.json(), query)
        result, response_data = check_result(check_field, expect_dict.get("matchRule"), expect_dict.get("assertString"))
        if not result:
            return "Fail", response_data

    # if resp.status_code != 200:
    #     test_result = "Fail"
    #     response_data = resp.text
    #     return test_result, response_data
    #
    # if resp.text.count(expect) > 0:
    #     test_result = "Pass"
    # else:
    #     test_result = "Fail"
    # resp_dic = resp.json()
    # for expect_key, expect_value in json.loads(expect).items():
    #     if resp_dic.get(expect_key) is not None:
    #         if resp_dic[expect_key] == expect_value:
    #             test_result = "Pass"
    #         else:
    #             test_result = "Fail"
    #     else:
    #         test_result = "Fail"
    return "Pass", resp.text


def parse_data(strs):
    data = json.loads(strs)
    dict_data = {}
    if data is not None:
        for h in data:
            dict_data[h.get('name')] = h.get('value')
    return dict_data


def check_result(field, match_rule, assert_string):
    if match_rule == "contains":
        if field.count(assert_string) > 0:
            return True, field
        else:
            return False, field
    elif match_rule == "equals":
        if field == assert_string:
            return True, field
        else:
            return False, field
    elif match_rule == "gt":
        if field > assert_string:
            return True, field
        else:
            return False, field
    elif match_rule == "lt":
        if field < assert_string:
            return True, field
        else:
            return False, field


# 用aa.bb的形式查询json数据{"aa":{"bb":2},"cc":3}中的值
# 比如上面aa.bb查询出来的值为2
def query_json(json_data, query_string):
    for key in query_string.split("."):
        if isinstance(json_data, list):
            key = int(key)
        json_data = json_data[key]
    return json_data
