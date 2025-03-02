from abc import ABC, abstractmethod
import re
import pandas as pd

class BaseDFBuilder(ABC):
    def __init__(self, data):
        self.data = data

    def return_list_of_keys(self):
        keys_that_should_become_df = []
        for key in self.data.keys():
            if type(self.data[key]) == dict:
                keys_that_should_become_df.append(key)
            elif type(self.data[key]) == list:
                if len(self.data[key]) > 0:
                    if type(self.data[key][0]) == dict:
                        keys_that_should_become_df.append(key)
        return keys_that_should_become_df

    def build_df(self) -> pd.DataFrame:
        raise NotImplemented

    def extract_id(url):
        match = re.search(r"/(\d+)/$", url)
        return int(match.group(1)) if match else None
