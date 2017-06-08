#!/usr/bin/env python
import sys
import os.path
sys.path.append(os.path.dirname(__file__) + "/../python-bittrex/bittrex")
from bittrex import Bittrex
from datetime import datetime


class Market(object):
    """
    Used to provide analysis of a market on Bittrex.
    """

    def __init__(self, name, bittrex=None):
        """
        :param name: String literal for the market (e.g. BTC-LTC)
        :type name: str
        :param bittrex: Instance of Bittrex, potentially with API_KEY and SECRET
        :type bittrex: Bittrex
        """
        self.name = name
        if bittrex:
            self.bittrex = bittrex
        else:
            self.bittrex = Bittrex(None, None)

    @property
    def summary(self):
        response = self.bittrex.get_market_summary(self.name)
        if response['success']:
            return response['result']
        raise Exception(
            "Could not retrieve data from Bittrex: {:s}".format(response['message'])
        )

    @property
    def history(self):
        response = self.bittrex.get_market_history(self.name)
        if response['success']:
            return response['result']
        raise Exception(
            "Could not retrieve data from Bittrex: {:s}".format(response['message'])
        )

    @property
    def orderbook(self):
        response = self.bittrex.get_orderbook(self.name)
        if response['success']:
            return response['result']
        raise Exception(
            "Could not retrieve data from Bittrex: {:s}".format(response['message'])
        )

    @property
    def ticker(self):
        response = self.bittrex.get_ticker(self.name)
        if response['success']:
            return response['result']
        raise Exception(
            "Could not retrieve data from Bittrex: {:s}".format(response['message'])
        )

    def get_price_trend(self):
        """
        Used to obtain a series of datetime-price tuples representing a market's price trend
        :return: list of tuples
        """
        price_trend = []
        for entry in self.history:
            price_trend.append(
                (datetime.strptime(entry['TimeStamp'].split(".")[0], "%Y-%m-%dT%H:%M:%S"),
                    entry["Price"])
            )
        return price_trend

    def __str__(self):
        return "{:s}\t{:s}".format(self.name, str(self.ticker))
