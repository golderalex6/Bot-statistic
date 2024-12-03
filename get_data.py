from funtional import *

class crypto_data():
    def __init__(self,pairs,start_date,end_date,interval='1m',thread=20):
        self.pairs=pairs
        self.thread=thread
        self.start_date=start_date
        self.end_date=end_date
        self.interval=interval
        self.container=[]

    def split(self,a, n):
        k, m = divmod(len(a), n)
        return [a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n)]
    
    def date_processing(self):
        date=pd.date_range(self.start_date,self.end_date,freq='D').to_pydatetime()
        date=self.split(date,self.thread)
        for i in date:i[-1]+=dt.timedelta(1)
        date=list(map(lambda x:[x[0],x[-1]],date))
        return date

    def get_history_bars(self,pair, start_date,end_date):

        start_date=int(start_date.timestamp()*1000)
        end_date=int(end_date.timestamp()*1000)

        url = f"https://data-api.binance.vision/api/v3/klines?symbol={pair}&interval={self.interval}&startTime={start_date}&endTime={end_date}&limit=1000"
        df=pd.DataFrame(requests.get(url).json())
        if (len(df.index)==0):
            return None

        df=df.iloc[:, 0:6]
        df.columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
        df['Date'] = [dt.datetime.strftime(dt.datetime.fromtimestamp(x/1000.0),'%Y/%m/%d %H:%M:%S') for x in df['Timestamp']]
        df['Open']=df['Open'].astype(float)
        df['High']=df['High'].astype(float)
        df['Low']=df['Low'].astype(float)
        df['Close']=df['Close'].astype(float)
        df['Volume']=df['Volume'].astype(float)
        df['Timestamp']=df['Timestamp']/1000
        df['Timeframe']=self.interval
        df=df[['Date','Timestamp','Timeframe','Open','High','Low','Close','Volume']]

        return df
    def get_binance_kline_price(self,pair,start_time,end_time):
        df_list = []
        last_datetime =start_time

        while True:
            new_df = self.get_history_bars(pair,last_datetime,end_time)
            if new_df is None:
                break
            df_list.append(new_df)
            last_datetime = dt.datetime.fromtimestamp(max(new_df['Timestamp'])) + dt.timedelta(0, 1)
            # print(last_datetime)
        df = pd.concat(df_list)
        self.container.append(df)

    def get_symbol_data(self,pair):
        th_list=[]
        date=self.date_processing()

        for i in range(self.thread):
            m=threading.Thread(target=self.get_binance_kline_price,args=(pair,date[i][0],date[i][1]))
            m.start()
            th_list.append(m)
        for th in th_list:th.join()
        data=pd.concat(self.container)
        data.drop_duplicates(inplace=True)
        data.sort_values(['Timestamp'],inplace=True)
        self.container=[]
        return data

    def filling(self,df):
        df=df.set_index('Date')
        df.index=pd.to_datetime(df.index)
        df=df.asfreq('1min',method='bfill')
        # df.reset_index(inplace=True)
        return df
    
    def get_data(self):
        if not os.path.exists(os.path.join(Path().cwd(),f'data')):
            os.mkdir(os.path.join(Path().cwd(),f'data'))
        for pair in self.pairs:
            print(pair)
            raw_data=self.get_symbol_data(pair)
            data=self.filling(raw_data)
            if not os.path.exists(os.path.join(Path().cwd(),f'data/{pair}')):
                os.mkdir(os.path.join(Path().cwd(),f'data/{pair}'))
            data.to_csv(os.path.join(Path().cwd(),f'data/{pair}/{pair}_1m.csv'))

if __name__=='__main__':
    start_date='2017/11/15 00:00:00' #FROM
    end_date= dt.datetime.strftime(dt.datetime.now(),'%Y/%m/%d %H:%M:%S') # NOW
    pairs=['BTCUSDT','ETHUSDT','BNBUSDT'] # PAIR LIST
    crypto=crypto_data(pairs=pairs,start_date=start_date,end_date=end_date)
    crypto.get_data()

