from ..parser.base_classes import *


class ParserInterface:
    def __init__(self):
        self._token = None
        self._chat_id = None

    async def get_filename(self):
        coinmarket_scrape = CoinmarketcapScraper()
        self._push_tqdm_telegram_data_to_scraper(coinmarket_scrape)

        tradingview_scrape = TradingviewScraper()

        kucoin_merge = KucoinMerger(
            target=await coinmarket_scrape.scrape(),
            source=tradingview_scrape.scrape()
        )

        excel_write = ExcelWriter(
            data=kucoin_merge.merge()
        )

        return excel_write.save_to_file()

    def set_telegram_data(self, token: str, chat_id: str):
        self._token = token
        self._chat_id = chat_id

    def _push_tqdm_telegram_data_to_scraper(self, coinmarket_scrape: CoinmarketcapScraper):
        coinmarket_scrape.set_telegram_data(_token=self._token, _chat_id=self._chat_id)
