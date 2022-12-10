import json
import time
import requests
from ext_config import headers, data, post_url
from extended_user_agent import ExtendedUserAgent
import async_main
import asyncio
from async_main import exec_time_decorator, get_coefficient


def format_json_str(json_data):
    return str(json_data).replace("'", '"').replace('T', 't')


def get_coins_info():
    ua = ExtendedUserAgent()
    json_data = json.loads(data)
    headers.update({'user-agent': ua.random_fresh_ua})

    last_elem = int(requests.post(url=post_url,
                                  headers=headers,
                                  data=format_json_str(json_data)).json()['totalCount'])
    json_data.update({'range': [0, last_elem]})

    return requests.post(url=post_url,
                         headers=headers,
                         data=format_json_str(json_data)).json()


def scrap_info():
    return [
        {
            'name': item['d'][13].split('/')[0],
            # 'price': item['d'][6],
            # 'ath': item['d'][11],
            # 'atl': item['d'][12],
            # 'exchange_for_link': 'KUCOIN',
            # 'name_for_link': item['d'][2]
        } for item in get_coins_info()['data'] if item['d'][10] == 'KUCOIN'
    ]


def write_new_titles_to_excel(titles: tuple, ws):
    for pos, title in enumerate(titles, start=5):
        ws.cell(row=1, column=pos).value = title


def read_all_names_from_excel(ws, last_item_num):
    return {
        ws.cell(row=i, column=1).value.strip(): i for i in range(2, last_item_num + 2)
        if ws.cell(row=i, column=1).value is not None
    }


@exec_time_decorator
async def get_data() -> str:
    wb, ws, last_item_num, file_name = await async_main.get_data()

    kucoin_coins_data = scrap_info()
    new_titles = (
        'market',
    )
    write_new_titles_to_excel(new_titles, ws)

    all_names_from_excel = read_all_names_from_excel(ws, last_item_num)

    # link_body = 'https://www.tradingview.com/symbols'
    for coin in kucoin_coins_data:
        for key, val in all_names_from_excel.items():
            if key.lower() == coin['name'].lower().strip():
                # ws.cell(row=row_num, column=5).value = get_coefficient(
                #     coin['price'],
                #     coin['ath'],
                #     coin['atl']
                # )
                ws.cell(row=val, column=5).value = 'KuCoin'
                # link = f'{link_body}/{coin["name_for_link"]}/?exchange={coin["exchange_for_link"]}'
                # ws.cell(row=row_num, column=6).value = link

    wb.save(filename=file_name)
    return file_name


async def main():
    await get_data()


if __name__ == '__main__':
    asyncio.run(main())
