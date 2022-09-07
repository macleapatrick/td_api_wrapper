from enumerations import StreamerServices as Stream
import pandas as pd
from datetime import datetime

class Consolidators(dict):
    """
    Dict data containor for all consolitdators
    """
    def __init__(self, service):
        self.service = service

    def stream_data(self, messages):
        """
        Takes list of messages from streamer.process() method
        """
        if messages:
            for message in messages:
                timestamp = message['timestamp']
                for data in message['content']:
                    key = data['key']
                
                    if key in self:
                        self[key].process_data(timestamp, data)
                    else:
                        self[key] = Consolidator(service=self.service)
                        self[key].process_data(timestamp, data)


class Consolidator:
    """
    Consolidator for 1 minute ohlc charts from live quote stream 
    """
    def __init__(self, service):
        self.service = service
        self.columns = ['TIMESTAMP','OPEN','HIGH','LOW','CLOSE','VOLUME']
        self.current = {kw : 0 for kw in self.columns}
        self.history = []

        self.minute = 0
        self.volumestart = 0

        if service == Stream.QUOTE.NAME:
            self._last_price_index = Stream.QUOTE.FIELDS.LAST_PRICE.value
            self._total_volume_key = Stream.QUOTE.FIELDS.TOTAL_VOLUME.value
        elif service == Stream.LEVELONE_FUTURES.NAME:
            self._last_price_index = Stream.LEVELONE_FUTURES.FIELDS.LAST_PRICE.value
            self._total_volume_key = Stream.LEVELONE_FUTURES.FIELDS.TOTAL_VOLUME.value
        else:
            pass
            # Add as needed

    def process_data(self, timestamp, data):
        if not self.minute:
            self.minute = self.round_timestamp(60)
        
        if (self.minute + 60000) < timestamp:
            self.minute += 60000
            self.history.append(self.current)
            print(self.current)
            self.clear()

        self.current['TIMESTAMP'] = int(self.minute / 1000)

        last_price = data.get(self._last_price_index)
        volume = data.get(self._total_volume_key)

        if last_price:
            if not self.current['OPEN']: 
                self.current['OPEN'] = last_price

            if not self.current['HIGH']:
                self.current['HIGH'] = last_price
            elif last_price > self.current['HIGH']:
                self.current['HIGH'] = last_price

            if not self.current['LOW']:
                self.current['LOW'] = last_price
            elif last_price < self.current['LOW']:
                self.current['LOW'] = last_price

            self.current['CLOSE'] = last_price

        if volume:
            if not self.volumestart:
                self.volumestart = volume
            else:
                self.current['VOLUME'] = volume - self.volumestart

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


