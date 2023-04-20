from .base_classes import Merger


class KucoinMerger(Merger):
    def __init__(self, target: dict[str, dict], source: list[str]):
        super().__init__(target, source)

    def merge(self) -> list[dict]:
        for kucoin_trading_coin_name in self._source:
            if self._target.get(kucoin_trading_coin_name.lower().strip()) is not None:
                self._target[kucoin_trading_coin_name.lower().strip()]['is_trading_on_kucoin'] = 'KuCoin'

        return list(self._target.values())
