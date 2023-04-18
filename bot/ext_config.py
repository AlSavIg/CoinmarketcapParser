cookies = {
    'cookiePrivacyPreferenceBannerProduction': 'notApplicable',
    'cookiesSettings': '{"analytics":true,"advertising":true}',
    '_ga': 'GA1.2.1060717267.1664276657',
    '_gid': 'GA1.2.1656850805.1664276657',
    '_sp_ses.cf1a': '*',
    '_gat_gtag_UA_24278967_1': '1',
    '_sp_id.cf1a': 'b9b4f9d9-f5d4-4765-80e4-22b0264e8b63.1664276550.2.1664335578.1664279549.0e4bfcff-29ef-4913-b370'
                   '-4237d9819141',
}

headers = {
    'authority': 'scanner.tradingview.com',
    'accept': 'text/plain, */*; q=0.01',
    'accept-language': 'ru,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.tradingview.com',
    'referer': 'https://www.tradingview.com/',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Yandex";v="22"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/104.0.5112.114 Safari/537.36',
}

data = '{"filter":[{"left":"name","operation":"nempty"}],"options":{"active_symbols_only":true,"lang":"en"},' \
       '"markets":["crypto"],"symbols":{"query":{"types":[]},"tickers":[]},"columns":["base_currency_logoid",' \
       '"currency_logoid","name","close","change","change_abs","high","low","volume","Recommend.All","exchange",' \
       '"High.All","Low.All","description","type","subtype","update_mode","pricescale","minmov","fractional",' \
       '"minmove2"],"sort":{"sortBy":"name","sortOrder":"asc"},"range":[0,150]}'


post_url = 'https://scanner.tradingview.com/crypto/scan'
