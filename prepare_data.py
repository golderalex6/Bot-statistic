from funtional import *

class prepare_date():
    def __init__(self):        
        self.paths=os.listdir(os.path.join(Path().cwd(),'data'))
        self.timeframes={'1m':1,'3m':3,'5m':5,'15m':15,'30m':30,'1h':60,'2h':120,'4h':240,'6h':360,'8h':480,'12h':720,'1d':1440}    
    def handle_ohlcv(self,arr):
        return [arr[0,0],arr[0,1],arr[0,2],arr[0,3],np.max(arr[:,4]),np.min(arr[:,5]),arr[-1,6],np.sum(arr[:,7])]
    def get_timeframe(self):        
        for pair in self.paths:
            for tf in self.timeframes.keys():
                if not os.path.exists(os.path.join(Path().cwd(),f"data/{pair}/{pair}_{tf}.csv")):
                    print(pair,tf)
                    df=pd.read_csv(os.path.join(Path().cwd(),f"data/{pair}/{pair}_1m.csv"))
                    wsize=self.timeframes[tf]
                    slide=sliding_window_view(df.values,(wsize,8)).squeeze()[::wsize]
                    get_timeframe=np.array(list(map(self.handle_ohlcv,slide)))
                    df=pd.DataFrame(get_timeframe,columns=['Date','Timestamp','Timeframe','Open','High','Low','Close','Volume'])
                    df.set_index('Date',inplace=True)
                    df.loc[:,'Timeframe']=tf
                    df.to_csv(os.path.join(Path().cwd(),f"data/{pair}/{pair}_{tf}.csv"))


prepare=prepare_date()
prepare.get_timeframe()

