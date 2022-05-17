import logging
from time import sleep

import requests
from parsel import Selector

from build.gen.bakdata.corporate.v1.corporate_pb2 import StockCorporate, Status, StockEntry
from av_producer import AVProducer

log = logging.getLogger(__name__)

import requests

API_KEY = '2KAXFVFXLKF0TWUN'

# https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo
SUCC = 0
FAILS = 0


class AVExtractor:
    def __init__(self, symbol_list: list):
        self.symbol_list = symbol_list
        self.producer = AVProducer()

    def extract(self):
        for i, (symbol, company, company_long) in enumerate(self.symbol_list):
            try:
                log.info(f"Sending Request for: {symbol} and company: {company}")
                text = self.get_stock_json(symbol)
                if "Falsche Parameter" in text:
                    log.info("The end has reached")
                    break
                meta = text['Meta Data']
                stock_values = text['Weekly Time Series']

                stock_corporate = StockCorporate()
                # TODO: think about the id
                stock_corporate.id = f"{symbol}_{i}"
                stock_corporate.symbol = symbol
                stock_corporate.company_name = company
                stock_corporate.company_name_long = company_long
                stock_corporate.last_refreshed = meta['3. Last Refreshed']
                stock_corporate.time_zone = meta['4. Time Zone']
                for ix, stock_date in enumerate(stock_values):
                    stock_entry = stock_corporate.stocks.add()
                    stock_entry.id = f"{ix}"
                    stock_entry.date = stock_date
                    stock_entry.open = stock_values[stock_date]['1. open']
                    stock_entry.close = stock_values[stock_date]['4. close']
                    stock_entry.high = stock_values[stock_date]['2. high']
                    stock_entry.low = stock_values[stock_date]['3. low']
                    stock_entry.volume = stock_values[stock_date]['5. volume']

                self.producer.produce_to_topic(stock_corporate)
                log.debug(stock_corporate)
            except Exception as ex:
                log.error(f"Skipping {symbol} in company {company}")
                log.error(f"Cause: {ex}")
                continue

    def get_stock_json(self, symbol: str):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={API_KEY}'
        r = requests.get(url)
        return r.json()
