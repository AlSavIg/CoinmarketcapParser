import datetime
import openpyxl
import string

from .base_classes import Writer


class ExcelWriter(Writer):
    def __init__(self, data: list[dict]):
        super().__init__(data)
        self._wb = openpyxl.Workbook()
        self._ws = self._wb.active
        self._titles = None

    def _fill_titles(self, titles: tuple):
        row = 1
        for pos, title in enumerate(titles, start=1):
            self._ws.cell(row=row, column=pos).value = title

    def _write_data_to_excel_sheet(self):
        row = [
            key for key in self._data[0].keys()
        ]
        self._write_row(row)

        for coin in self._data:
            row = [
                coin.get('name'),
                coin.get('rank'),
                coin.get('coef_on_coinmarketcap'),
                coin.get('link'),
                coin.get('is_trading_on_kucoin'),
            ]
            self._write_row(row)

    def _write_row(self, row: list):
        self._ws.append(row)

    def _format_col_width(self):
        for letter in string.ascii_uppercase[:7]:
            self._ws.column_dimensions[letter].width = 30

    def save_to_file(self) -> str:
        file_name = f'{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}' \
                    f'_coinmarketcap.xlsx'

        last_item_num = len(self._data)

        self._write_data_to_excel_sheet()

        self._ws.auto_filter.ref = f'A1:E{last_item_num + 1}'
        self._ws.auto_filter.add_sort_condition(f'C2:C{last_item_num + 1}')
        self._format_col_width()

        self._wb.save(filename=file_name)

        return file_name
