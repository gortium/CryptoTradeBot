import requests
import time


class CoinfieldClient:
    with open('coinfield_token.txt') as f:
        token = f.readline()

    def GetStatus(self):
        request = "https://api.coinfield.com/v1/status"
        
        return self.send_request(request, retry=2)

    def GetTimestamp(self):
        request = "https://api.coinfield.com/v1/timestamp"
        
        return self.send_request(request, retry=2)

    def GetCurrencies(self):
        request = "https://api.coinfield.com/v1/currencies"
        
        return self.send_request(request, retry=2)

    def GetMarkets(self):
        request = "https://api.coinfield.com/v1/markets"
        
        return self.send_request(request, retry=2)

    def GetTickers(self, market=""):
        if market != '':
            request = "https://api.coinfield.com/v1/tickers" + "/" + market
        else:
            request = "https://api.coinfield.com/v1/tickers"
        
        return self.send_request(request, retry=2)

    def GetOrderbook(self, market, limit=None):
        if limit is not None:
            request = "https://api.coinfield.com/v1/orderbook/" + "/" + market + "?limit=" + str(limit)
        else:
            request = "https://api.coinfield.com/v1/orderbook/" + "/" + market
        
        return self.send_request(request, retry=2)

    def GetDepth(self, market, limit=None):
        if limit is not None:
            request = "https://api.coinfield.com/v1/depth/" + "/" + market + "?limit=" + str(limit)
        else:
            request = "https://api.coinfield.com/v1/depth/" + "/" + market
        
        return self.send_request(request, retry=2)

    def GetOhlc(self, market, limit=None, period=None, fromArg=None, to=None):
        request = "https://api.coinfield.com/v1/ohlc/" + market
        firstArg = True

        if limit != None:
            if firstArg:
                request += "?"
                firstArg = False
            else:
                request += "&"
            request += "limit=" + str(limit)
        if period != None:
            if firstArg:
                request += "?"
                firstArg = False
            else:
                request += "&"
            request += "period=" + str(period)
        if fromArg != None:
            if firstArg:
                request += "?"
                firstArg = False
            else:
                request += "&"
            request += "from=" + str(fromArg)
        if to != None:
            if firstArg:
                request += "?"
                firstArg = False
            else:
                request += "&"
            request += "to=" + str(to)

        return self.send_request(request, retry=2)

    def GetTrades(self, market, limit=None, timestamp=None, fromArg=None, to=None, order_by=None):
        request = "https://api.coinfield.com/v1/trades/" + market
        firstArg = True

        if limit is not None:
            if firstArg:
                request += "?"
                firstArg = False
            else:
                request += "&"
            request += "limit=" + str(limit)
        if timestamp is not None:
            if firstArg:
                request += "?"
                firstArg = False
            else:
                request += "&"
            request += "timestamp=" + str(timestamp)
        if fromArg is not None:
            if firstArg:
                request += "?"
                firstArg = False
            else:
                request += "&"
            request += "from=" + str(fromArg)
        if to is not None:
            if firstArg:
                request += "?"
                firstArg = False
            else:
                request += "&"
            request += "to=" + str(to)
        if order_by is not None:
            if firstArg:
                request += "?"
                firstArg = False
            else:
                request += "&"
            request += "order_by=" + str(order_by)

        return self.send_request(request, retry=2)

    def GetFees(self):
        request = "https://api.coinfield.com/v1/fees"

        return self.send_request(request, retry=2)

    def GetTradeHistory(self, market, limit=None, timestamp=None, fromArg=None, to=None, order_by=None):
        request = "https://api.coinfield.com/v1/trades/" + market
        firstArg = True

        if limit is not None:
            if firstArg:
                request += "?"
                firstArg = False
            else:
                request += "&"
            request += "limit=" + str(limit)
        if timestamp is not None:
            if firstArg:
                request += "?"
                firstArg = False
            else:
                request += "&"
            request += "timestamp=" + str(timestamp)
        if fromArg is not None:
            if firstArg:
                request += "?"
                firstArg = False
            else:
                request += "&"
            request += "from=" + str(fromArg)
        if to is not None:
            if firstArg:
                request += "?"
                firstArg = False
            else:
                request += "&"
            request += "to=" + str(to)
        if order_by is not None:
            if firstArg:
                request += "?"
                firstArg = False
            else:
                request += "&"
            request += "order_by=" + str(order_by)

        return self.send_request(request, retry=2)

    def send_request(self, request, retry=0):
        response = requests.get(request, headers = {"Authorization":"Bearer " + self.token}).json()
        if "status" in response:
            if response["status"] != 200:
                if retry > 0:
                    print("Server error: " + str(response["status"]))
                    time.sleep(1)
                    print("Retrying..")
                    response = self.send_request(request, retry-1)
                else:
                    print("SERVER ERROR. NO RETRY")
                    return None
        else:
            print("Request successful!")
        return response