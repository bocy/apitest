from requests import request
import json
import logging

logger = logging.getLogger("apitest")


def run_test(method, url, params, expect):
    test_result = False
    params_data = None
    post_data = None
    if method.upper() == "POST":
        post_data = params
    elif method.upper() == "GET":
        params_data = params

    resp = request(method, url, params=params_data, data=post_data)
    logger.info(resp.status_code)
    if resp.status_code != 200:
        test_result = False
        response_data = resp.text
        return test_result, response_data

    resp_dic = resp.json()
    for expect_key, expect_value in json.loads(expect).items():
        if resp_dic.get(expect_key) is not None:
            if resp_dic[expect_key] == expect_value:
                test_result = True
            else:
                test_result = False
        else:
            test_result = False
    return test_result, resp.text


