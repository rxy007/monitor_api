import requests
import datetime
import hashlib
from email_util import send_eamil
from logger_util import write_log
import json

task_name = 'chat_parsing_assemble'

cron = '0 20 * * *'

prod_host = ['212.129.164.50', '211.159.248.106']*5
url = 'http://{}:9003/nlp_service/level_2/deal/parsing'
test_url = 'http://{}:9016/nlp_service/level_2/deal/parsing'

test_host = ['212.64.103.59']*5

data = {
        "from_id": "AF611D6BCDC6C3C0598F407AC027EB3F",
        "from_info": "技术支持",
        "to_id": "E7B5F1CCC304B82B411B55B4418DA449",
        "to_info": "",
        "message_id": "airflow",
        "strategy": 0,
        "content": "邯钢转债  3.222 9000*2 今天+0  出给 博时基金 发国信证券"
}

desired_result = {
    "res": {
        "from": [
            {
                "chat_with": "",
                "account_info": "",
                "bond_code": "",
                "bond_name": "邯钢转债",
                "bridge": [
                    "国信证券",
                    "博时基金",
                    "技术支持"
                ],
                "bridge_fee": "",
                "clearing_speed": "T+0",
                "counter_party": [
                    "博时基金",
                    "国信证券",
                    "技术支持"
                ],
                "credit_rate": "",
                "deal_code": "",
                "flat_price": "",
                "issuing_period": "",
                "notes": "",
                "origin_rate": "3.222",
                "rate": "3.222",
                "staff_code": "",
                "true_direction": "卖",
                "volume": "9000*2",
                "trade_type": "本方发对话",
                "yield_type": "",
                "our_staff_code": "",
                "other_staff_code": "",
                "full_price": "",
                "instruct_operator": "",
                "pass_number": "",
                "direct_counter": [
                    "国信证券",
                    "博时基金",
                    "技术支持"
                ],
                "real_counter": [
                    "博时基金",
                    "国信证券",
                    "技术支持"
                ]
            }
        ],
        "to": [
            {
                "chat_with": "",
                "account_info": "",
                "bond_code": "",
                "bond_name": "邯钢转债",
                "bridge": [
                    "国信证券",
                    "博时基金",
                    "技术支持"
                ],
                "bridge_fee": "",
                "clearing_speed": "T+0",
                "counter_party": [
                    "博时基金",
                    "国信证券",
                    "技术支持"
                ],
                "credit_rate": "",
                "deal_code": "",
                "flat_price": "",
                "issuing_period": "",
                "notes": "",
                "origin_rate": "3.222",
                "rate": "3.222",
                "staff_code": "",
                "true_direction": "卖",
                "volume": "9000*2",
                "trade_type": "本方发对话",
                "yield_type": "",
                "our_staff_code": "",
                "other_staff_code": "",
                "full_price": "",
                "instruct_operator": "",
                "pass_number": "",
                "direct_counter": [
                    "国信证券",
                    "博时基金",
                    "技术支持"
                ],
                "real_counter": [
                    "博时基金",
                    "国信证券",
                    "技术支持"
                ]
            }
        ],
        'status_code_from': 0,
        'status_code_to': 0,
    },
}


def check_result(real_result):
    real_result['res']['from'][0].pop('trade_date')
    real_result['res']['to'][0].pop('trade_date')
    return desired_result['res'] == real_result['res']


def token(s):
    return hashlib.md5(s.encode(encoding='utf-8')).hexdigest()


def run():
    str_date = datetime.datetime.now().strftime("%Y/%m/%d")
    data['token'] = token(data['content'] + str_date)
    for host in prod_host:
        result = requests.post(url.format(host), json=data).json()
        write_log(task_name, json.dumps(result, ensure_ascii=False))
        try:
            assert result['status'] == 0
            assert check_result(result)
        except AssertionError:
            to = ['rxy@qtrade.com.cn']
            cc = ['abcdefghijkl_mnopq@163.com']
            subject = '成交项目异常'
            html_content = '成交项目解析结果异常222'
            mime_charset = 'utf8'
            send_eamil(to, subject, html_content, retry=3, cc=cc, mime_charset=mime_charset)
            break

    #return result


if __name__ == '__main__':
    run()