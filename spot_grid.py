from funtional import *

class spot_grid():
    def __init__(self,symbol,upper_limit,lower_limit,balance,amount,trade_style='arithmetic',start_date=None,end_date=None):
        self.symbol=symbol
        self.upper_limit=upper_limit
        self.lower_limit=lower_limit
        self.balance=balance
        self.amount=amount
        self.num_grids=int(balance/amount)

        if trade_style=='arithmetic':
            self.grid_levels=[lower_limit + i * (upper_limit - lower_limit) / self.num_grids for i in range(self.num_grids + 1)]
        elif trade_style=='geometric':
            self.percent=(upper_limit/lower_limit)**(1/self.num_grids)
            self.grid_levels=[round(lower_limit*self.percent**i,2) for i in range(self.num_grids+1)]
        
        self.buy_level=[]
        self.sell_level=[]
        self.coin_balance=[]
        self.fee=0
        self.current_level=None
        
        self.df = pd.read_csv(f'Data/{symbol}/{symbol}_3m.csv',index_col=0,parse_dates=True).loc[start_date:end_date]
        self.start_date=(start_date,self.df.index[0])[start_date==None]
        self.end_date=(end_date,self.df.index[-1])[end_date==None]
        self.price=self.df['Close']

        self.profit=[0]
        self.current_price = self.price.iloc[1]
        self.orders=[]
        self.start_price=self.price.iloc[0]
        
    def setup(self):
        for level in self.grid_levels:
            if self.start_price>=level:
                self.buy_level.append(level)
            else:
                self.sell_level.append(level)
                self.coin_balance.insert(0,self.amount/level)
                self.balance-=self.amount
        self.sell_level,self.current_level=self.sell_level[1:],self.sell_level[0]
        print(dt.datetime.strftime(dt.datetime.now(),'%Y/%m/%d %H:%M:%S')+f' Buy {sum(self.coin_balance)} BTC',f'start price :{self.start_price}')

    def trade(self):
        self.setup()
        for i in range(1,self.df.shape[0]):

            self.current_price=self.price.iloc[i]
            date=self.price.index[i]
        
            if self.current_price<self.lower_limit or self.current_price>self.upper_limit:
                self.profit.append(self.profit[-1])
                continue
            get=0
            if self.current_price>=self.sell_level[0]:
                
                sell_amount=self.coin_balance[-1]
                sell_price=self.sell_level[0]
                
                get=sell_amount*sell_price*0.998-self.amount
                self.fee+=sell_amount*sell_price*0.002
                
                self.buy_level.append(self.current_level)
                self.current_level=self.sell_level[0]
                self.orders.append([self.df.index[i],sell_price,-1])
                del self.coin_balance[-1],self.sell_level[0]
                
                print(f'Sell {sell_amount} BTC at {sell_price} get:{get} USDT,total BTC:{sum(self.coin_balance)}')
        
            elif self.current_price<self.buy_level[-1]:
                
                buy_price=self.buy_level[-1]
                buy=self.amount/buy_price
                
                self.coin_balance.append(buy)
                self.sell_level.insert(0,self.current_level)
                self.current_level=buy_price
                self.orders.append([self.df.index[i],buy_price,1])
                del self.buy_level[-1]
                
                print(f'BUY {buy} BTC at {buy_price},total BTC:{sum(self.coin_balance)}')
            self.profit.append(self.profit[-1]+get)
            # print(f"Price:{current_price},Level:{current_level},Upper:{sell_level[0]},Lower:{buy_level[-1]}")

        self.df['Profit']=self.profit
    def draw(self):
        fg=plt.figure(figsize=(15,9))
        ax1=fg.add_subplot(2,1,1)
        ax2=fg.add_subplot(2,1,2)
        for date,price,pos in self.orders:
            ax1.text(date,price,('S','B')[pos==1],color=('red','green')[pos==1],fontsize=15)
        ax1.set_ylabel('Price ($)')
        ax1.set_title(f'{self.symbol} {self.start_date}-{self.end_date}')
        
        self.df['Close'].plot(ax=ax1,color='black')
        self.df['Profit'].plot(ax=ax2)
        ax2.text(self.df.index[0],np.max(self.df['Profit'])*0.95,f'Total fee:-{round(self.fee,2)}',color='red')
        ax2.set_title('Profit over time')
        plt.tight_layout()
        plt.show()

if __name__=='__main__':
    symbol='BTCUSDT'
    upper_limit=80000
    lower_limit=5000
    balance=100000
    amount=1000
    trade_style='geometric'
    start_date='2023-01-01 00:00:00'
    end_date='2024-01-01 00:00:00'
    start_date,end_date=None,None
    spot=spot_grid(symbol,upper_limit,lower_limit,balance,amount,trade_style,start_date,end_date)
    spot.trade()
    spot.draw()

