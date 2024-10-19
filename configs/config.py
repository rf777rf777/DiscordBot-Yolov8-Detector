import json

class Config:
    def __init__(self):
        pass

    @staticmethod
    def get_config():
        """
        載入設定檔
        """
        with open('configs/config.json') as f:
            return json.load(f)