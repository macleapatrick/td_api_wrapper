from sqlite3 import Timestamp
import pandas as pd
from datetime import datetime

class Consolidators(dict):
    """
    Dict data containor for all consolitdators
    """
    def __init__(self):
        pass

    def stream_data(self, messages):
        """
        Takes list of messages from streamer.process() method
        """
        for message in messages:
            if message.get('data'):
                message = message['data'][0]
                service = message['service']
                timestamp = message['timestamp']
                for data in message['content']:
                    key = data['key']
                
                    if key in self:
                        self[key].process_data(timestamp, data)
                    else:
                        self[key] = Consolidator()
                        self[key].process_data(timestamp, data)
            else:
                #Not a data message
                pass


class Consolidator:
    """
    Consolidator for 1 minute ohlc charts from live quote stream 
    """
    def __init__(self):
        self.columns = ['timestamp','open','high','low','close','volume']
        self.current = {kw : 0 for kw in self.columns}
        self.history = []

        self.minute = 0
        self.volumestart = 0

    def process_data(self, timestamp, data):
        if not self.minute:
            self.minute = self.round_timestamp(60)
        
        if (self.minute + 60000) < timestamp:
            self.minute += 60000
            self.history.append(self.current)
            print(self.current)
            self.clear()

        self.current['timestamp'] = self.minute

        last_price = data.get('3')
        volume = data.get('8')

        if last_price:
            if not self.current['open']: 
                self.current['open'] = last_price

            if not self.current['high']:
                self.current['high'] = last_price
            elif last_price > self.current['high']:
                self.current['high'] = last_price

            if not self.current['low']:
                self.current['low'] = last_price
            elif last_price < self.current['low']:
                self.current['low'] = last_price

            self.current['close'] = last_price

        if volume:
            if not self.volumestart:
                self.volumestart = volume
            else:
                self.current['volume'] = volume - self.volumestart

    def clear(self):
        self.current = {kw : 0 for kw in self.columns}
        self.volumestart = 0

    @staticmethod
    def round_timestamp(seconds):
        """
        round timestamp in ms down to nearest interval
        """
        inMs = seconds*1000
        return int(((datetime.now().timestamp() * 1000) // inMs) * inMs)


