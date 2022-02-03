import os
import yaml
import json
from copy import deepcopy

from config import PROJECT_ROOT


class FundScreenerConfig:
    def __init__(self):
        with open(os.path.join(PROJECT_ROOT, f"config/us.yml"), "r") as f:
            self._cfg = yaml.safe_load(f)

    def __getattr__(self, attr):
        return self.__dict__["_cfg"][attr]

    def __repr__(self):
        cfg = deepcopy(self._cfg)
        properties = [x for x in dir(self) if not x.startswith("_")]
        for pty in properties:
            cfg[pty] = getattr(self, pty)
        return json.dumps(cfg)
