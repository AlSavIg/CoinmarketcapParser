from typing import Union


class Writer:
    def __init__(self, data: list[dict]):
        self._data = data

    def save_to_file(self) -> str:
        pass


class Merger:
    def __init__(self, target: dict[str, dict], source: list[str]):
        self._target = target
        self._source = source

    def merge(self) -> list[dict]:
        pass


class Scraper:
    def scrape(self) -> Union[list[str] | dict[str, dict]]:
        pass
