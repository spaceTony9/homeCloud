from pathlib import Path
import json

class CloudStorage: 
    def __init__(self, storage_config="storageConfig.json"):
        with open(storage_config) as f:
            self.config = json.load(f)
            self.storage_root = Path(self.config["root"])