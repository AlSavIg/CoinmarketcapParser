import asyncio
import random
import time
from decimal import Decimal
from aiocfscrape import CloudflareScraper
import json
from bs4 import BeautifulSoup
from tqdm.contrib.telegram import tqdm
import logging

from .config.coinmarket_config import url, headers, params
from .base_classes import Scraper
from .utils import async_exec_time_decorator
from .extended_user_agent import ExtendedUserAgent


class CoinmarketcapScraper(Scraper):
    class CoinmarketcapLowPricesPageScraper:
        def __init__(self):
            self._session = None

        @staticmethod
        def _parse_response(page: BeautifulSoup) -> dict[str, Decimal]:
            try:
                def _get_low_price_from_tr(tr: BeautifulSoup):
                    return tr.find("td").find_all("div")[0].text.replace("$", "").replace(",", "").replace(" /", "")

                low_price_table_rows = page.find(
                    "div", {"class": "sc-aef7b723-0 dDQUel hide"}
                ).find_all("table")[1].find_all("tr")

                return {
                    "week": Decimal(_get_low_price_from_tr(low_price_table_rows[0])),
                    "month": Decimal(_get_low_price_from_tr(low_price_table_rows[1])),
                    "quarter": Decimal(_get_low_price_from_tr(low_price_table_rows[2])),
                    "year": Decimal(_get_low_price_from_tr(low_price_table_rows[3])),
                }
            except Exception as e:
                return {
                    "week": Decimal(-1000),
                    "month": Decimal(-1000),
                    "quarter": Decimal(-1000),
                    "year": Decimal(-1000),
                }

        async def _get_min_from_requested_page(self, link, to_fill_dict: dict) -> dict[str, Decimal]:
            ua = ExtendedUserAgent()

            headers.update(user_agent=ua.random_fresh_ua)
            response = await self._session.get(link, headers=headers)

            for _ in range(2):
                if response.status != 200:
                    sleep_time = 60
                    logging.warning(f"Response code: {response.status} on page {link}\n"
                                    f"Sleep thread for {sleep_time} seconds and trying again [{_}]")
                    time.sleep(sleep_time + random.random())  # Stops the thread

                    headers.update(user_agent=ua.random_fresh_ua)
                    response = await self._session.get(link, headers=headers)
                else:
                    logging.info(f"Response code: {response.status} on page {link}")
                    break

            to_fill_dict.update(
                self._parse_response(
                    BeautifulSoup(await response.text(), "lxml")
                )
            )

            return to_fill_dict

        async def fill_dict_with_low_prices(self, link: str, to_fill_prices_dict: dict) -> dict[str, Decimal]:
            async with CloudflareScraper() as session:
                self._session = session
                return await self._get_min_from_requested_page(link, to_fill_prices_dict)

    def __init__(self):
        self._session = None
        self._tqdm = None
        self._data = dict()
        self._token = None
        self._chat_id = None

        logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                            format="%(asctime)s %(levelname)s %(message)s")

    @staticmethod
    def _calc_coef(price: str, rank: str, intervals_low: dict[str, Decimal]):
        # Negative result means exception on the parse step
        return round(
            (
                    sum(intervals_low.values()) / Decimal(price) + 1 / Decimal(rank)
            ),
            4)

    @staticmethod
    def _filter_by_trading_volume(day_trading_volume) -> bool:
        border = 100_000
        return day_trading_volume >= border

    # async def _calc_min_of_requested_chart(self, id_) -> dict:
    #     # chart_params = {
    #     #     'id': None,
    #     #     'range': None,
    #     # }
    #     # local_data = dict()
    #     # for key in self._time_shortcuts.keys():
    #     #     for _ in range(3):
    #     #         chart_params.update(id=id_, range=self._time_shortcuts[key])
    #     #
    #     #         response = await self._session.get(
    #     #             url='https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart',
    #     #             headers=headers,
    #     #             params=chart_params
    #     #         )
    #     #         ua = ExtendedUserAgent()
    #     #         headers.update({'user-agent': ua.random_fresh_ua})
    #     #         try:
    #     #             points = json.loads(await response.text()).get('data').get('points')
    #     #             print(f"[INFO] Got data with next key: [{key}]")
    #     #             local_data[key] = min(
    #     #                 (Decimal(points[i].get("c")[0]) for i in range(len(points)))
    #     #             )
    #     #             await asyncio.sleep(random.random() * 5)
    #     #             break
    #     #         except json.decoder.JSONDecodeError:
    #     #             print(f"[ERROR] Json decode error on the key: [{key}]")
    #     #             await asyncio.sleep(random.random() * 5)
    #     # return local_data
    #     pass

    async def _make_requests_and_fill_data_list(self, start: int):
        ua = ExtendedUserAgent()
        headers.update(user_agent=ua.random_fresh_ua)
        params_copy = params.copy()
        params_copy.update(start=start)

        sleep_time = 11 + random.random() * 10

        response = await self._session.get(
            url=url,
            headers=headers,
            params=params_copy
        )
        json_ = json.loads(await response.text())['data']['cryptoCurrencyList']

        page_low_prices_scraper = self.CoinmarketcapLowPricesPageScraper()

        main_url = 'https://coinmarketcap.com/currencies/'
        for item in json_:
            try:
                name = item['name']
                price = item['quotes'][2]['price']  # USD
                rank = item['cmcRank']
                link = main_url + item['slug'] + '/'
                # id_ = item['id']  # Needs only for the request to charts
                day_trading_volume = item['quotes'][2]['volume24h']  # Needs only to filter _data
                _time_shortcuts = {
                    "day": Decimal(item['low24h']),  # USD all
                    "week": None,
                    "month": None,
                    "quarter": None,
                    "year": None,
                }

                self._tqdm.update(1)

                if self._filter_by_trading_volume(day_trading_volume):
                    await page_low_prices_scraper.fill_dict_with_low_prices(
                        link=link,
                        to_fill_prices_dict=_time_shortcuts
                    )

                    await asyncio.sleep(sleep_time)

                    coefficient = self._calc_coef(
                        price=price,
                        rank=rank,
                        intervals_low=_time_shortcuts
                    )

                    self._data[name.lower().strip()] = {
                        "name": name,
                        'rank': rank,
                        'coef_on_coinmarketcap': coefficient,
                        'link': link,
                        'is_trading_on_kucoin': '',
                    }
            except KeyError:
                self._tqdm.update(1)

        await asyncio.sleep(sleep_time)

    async def _get_last_coin_num_from_api(self):
        response = await self._session.get(
            url=url,
            headers=headers,
            params=params)
        return int(json.loads(await response.text())['data']['totalCount'])

    @async_exec_time_decorator
    async def _scrape_and_parse_coinmarket_cryptocurrency_listing(self):
        async with CloudflareScraper() as session:
            self._session = session
            last_item_num = await self._get_last_coin_num_from_api()
            self._tqdm = tqdm(
                total=last_item_num,
                token=self._token,
                chat_id=self._chat_id,
                dynamic_ncols=True,
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} "
                           "[Прошло: {elapsed} Осталось: {remaining}]",
            )

            step = int(params['limit'])

            tasks = [
                asyncio.create_task(self._make_requests_and_fill_data_list(i)) for i in range(1, last_item_num, step)
            ]

            await asyncio.gather(*tasks)

    def set_telegram_data(self, _token, _chat_id):
        self._token = _token
        self._chat_id = _chat_id

    async def scrape(self) -> dict[str, dict]:
        await self._scrape_and_parse_coinmarket_cryptocurrency_listing()
        self._tqdm.close()
        return self._data
