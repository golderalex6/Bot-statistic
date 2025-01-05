from abc import ABC,abstractmethod
import numpy as np

#kind = 'usd'

class Order:

    def __init__(self,amount,leverage,position):

        self._order_id = None

        self._leverage = leverage
        self._position = position

        self._margin = amount/leverage
        self._liquidity_price = None
        self._open_price = np.nan
        self._close_price = np.nan

        self._pnl = None
        self._roi = None

        self._status = 0 #{0 : "Placing",1 : "Opening",2 : "Closed" }

    def place(self,price) -> None:
        self._liquidity_price = price*(1-self._position/self._leverage)
        self._status = 1
        self._open_price = price
        self._pnl = 0
        self._roi = 0

    def close(self,price) -> None:

        self._status = 2
        self._close_price = price
        self._pnl = self._position*(price-self._open_price)
        self._roi = self._position*(price-self._open_price)/self._open_price

    @abstractmethod
    def _open_condition(self) -> bool:
        pass

    def update(self) -> None:
        pass

    @abstractmethod
    def update(self,price) -> None:
        pass

    def get_metadata(self):
        return {
                'leverage':self._leverage,
                'position':self._position,
                'margin':self._margin,
                'liquidity_price':self._liquidity_price,
                'open_price':self._open_price,
                'close_price':self._close_price,
                'pnl':self._pnl,
                'roi':self._roi,
                'status':self._status
            }

class Limit(Order):

    def __init__(self,amount:float,leverage:int,price:float,position:int) -> None:
        super().__init__(amount,leverage,position)
        self._limit_price = price

    def update(self,price:float):
        if self._position*price <= self._position*self._limit_price and self._status == 0:
            self.place(price)
            self._status = 1

        if self._status == 1:

            self._pnl = self._position*(price-self._open_price)
            self._roi = self._position*(price-self._open_price)/self._open_price



class Market(Order):
    def __init__(self,amount:float,leverage:int,position:int) -> None:
        super().__init__(amount,leverage,position)

    def update(self,price:float):
        if self._status == 0:
            self.place(price)
            self._status = 1

        if self._status == 1:

            self._pnl = self._position*(price-self._open_price)
            self._roi = self._position*(price-self._open_price)/self._open_price

class TraillingStop(Order):
    def __init__(self):
        pass

    def update(self,price:float):
        if self._position == 'long':
            pass
        elif self._position == 'short':
            pass


class Spot:

    def __init__(self) -> None:
        self._container = []

    def place(self,order:Order):
        self._container.append(order)

    def update(self,price):
        for order in self._container:
            order.update(price)

    def close(self,order_id:str):
        pass

    def info(self,order_id:str):
        pass

    def history(self):
        pass


if __name__ == '__main__':
    prices = [10,8,7,5,4,6,8,11]
    order = Limit(100,1,4.5,-1)
    for price in prices:
        order.update(price)
        print(price,order.get_metadata())
