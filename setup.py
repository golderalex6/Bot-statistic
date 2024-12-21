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
            'symbol':'BTCUSDT'
            },
        'future_grid':{
            'symbol':'BTCUSDT'
            },
        'infinity_bot':{
            'symbol':'BTCUSDT'
            },
        'rebalancing_bot':{
            'symbol':'BTCUSDT'
            },
        'special_martingale':{
            'symbol':'BTCUSDT'
            },
        'dca_spot':{
            'symbol':'BTCUSDT'
            },
    }

for bot,metadata in metadatas.items():
    with open(os.path.join(Path(__file__).parent,'metadata',f"{bot}.json"),'a+') as f:
        json.dump(metadata,f,indent=4)
