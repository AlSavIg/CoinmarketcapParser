import json
import cfscrape

from .base_classes import Scraper
from .extended_user_agent import ExtendedUserAgent
from .config.tradingview_config import headers, data, url
from .utils import exec_time_decorator


class TradingviewScraper(Scraper):
    def __init__(self):
        self._session = None
        self._data = list()

    @staticmethod
    def _format_json_str(json_data):
        return str(json_data).replace("'", '"').replace('T', 't')

    def _make_request_to_tradingview(self):
        ua = ExtendedUserAgent()
        json_data = json.loads(data)
        headers.update({'user-agent': ua.random_fresh_ua})

        last_elem = int(self._session.post(url=url,
                                           headers=headers,
                                           data=self._format_json_str(json_data)).json()['totalCount'])
        json_data.update({'range': [0, last_elem]})

        return self._session.post(url=url,
                                  headers=headers,
                                  data=self._format_json_str(json_data)).json()

    @staticmethod
    def _parse_response(response_json: dict):
        # Returns more than I really need
        # return [
        #     {
        #         'name': item['d'][13].split('/')[0],
        #         # 'price': item['d'][6],
        #         # 'ath': item['d'][11],
        #         # 'atl': item['d'][12],
        #         # 'exchange_for_link': 'KUCOIN',
        #         # 'name_for_link': item['d'][2]
        #     } for item in response_json['_data'] if item['d'][10] == 'KUCOIN'
        # ]
        return [
            item['d'][13].split('/')[0]  # names
            for item in response_json['data'] if item['d'][10] == 'KUCOIN'
        ]

    @exec_time_decorator
    def _scrape_and_parse_kucoin_trading_names(self) -> list[str]:
        self._session = cfscrape.create_scraper()

        kucoin_market_coin_names = self._parse_response(
            self._make_request_to_tradingview()
        )

        return kucoin_market_coin_names

    def scrape(self) -> list[str]:
        return self._scrape_and_parse_kucoin_trading_names()
