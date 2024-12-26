import os
from pathlib import Path
import json

#create 'data' folder
if not os.path.exists(os.path.join(Path(__file__).parent,'data')):
    os.mkdir(os.path.join(Path(__file__).parent,'data'))

#create 'metadata' folder
if not os.path.exists(os.path.join(Path(__file__).parent,'metadata')):
    os.mkdir(os.path.join(Path(__file__).parent,'metadata'))

#create .json files for 'metadata' folder
metadatas={
        'spot_grid':{
            'symbol':'BTCUSDT',
            'initial_balance':10000
            },
        'future_grid':{
            'symbol':'BTCUSDT',
            'initial_balance':10000
            },
        'infinity_bot':{
            'symbol':'BTCUSDT',
            'initial_balance':10000
            },
        'rebalancing_bot':{
            'symbol':'BTCUSDT',
            'initial_balance':10000
            },
        'special_martingale':{
            'symbol':'BTCUSDT',
            'initial_balance':10000
            },
        'dca_spot':{
            'symbol':'BTCUSDT',
            'initial_balance':10000
            },
    }

for bot,metadata in metadatas.items():
    with open(os.path.join(Path(__file__).parent,'metadata',f"{bot}.json"),'a+') as f:
        json.dump(metadata,f,indent=4)
