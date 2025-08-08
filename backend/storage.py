from pathlib import Path
import json

class CloudStorage: 
    storage_root = None
    # def __init__(self, storage_config="storageConfig.json"):
    #     with open(storage_config) as f:
    #         self.config = json.load(f)
    #         storage_root = Path(self.config["root"])
    @staticmethod
    def send_storage_root(storage_config="storageConfig.json"):
        with open(storage_config) as f:
            config = json.load(f)
            storage_root = Path(config["root"])
        return storage_root