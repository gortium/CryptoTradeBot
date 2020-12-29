import coinfieldClient as cfc
import json
import csv
import pandas as pd
import numpy as np
import pprint
import time
import os

CF_DATA_LIMIT = 10000
COINFIELDSTART = 1522896600


class DataManager:
    cfClient = cfc.CoinfieldClient()
    
    def format_raw_data(self, df):
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].apply(pd.to_numeric)
        df.set_index('Datetime', inplace=True)
        df = df.tz_localize(None)
        df.drop_duplicates(inplace=True)
        df.sort_index(inplace=True)
        
        return df
    
    def load_raw_data_from_file(self, fullPath):
        file_df = pd.read_csv(fullPath, index_col=None, header=0)
        file_df = self.format_raw_data(file_df)
        
        return file_df

    def update_raw_data(self, source, market, period):
        main_df = pd.DataFrame()
        start = COINFIELDSTART
        MAX_FETCH_PERIOD = period*60*CF_DATA_LIMIT  # period is in minute. *60 to get s.
        stop = start + MAX_FETCH_PERIOD + 1     # +1 for inclusivity
        path = "raw_data/"  # + str(source) + "/" + str(market) + "/" + str(period) + "/"

        fileName = str(source) + "-" + str(market) + "-" + str(period) + ".csv"
        fullPath = path + fileName

        if os.path.exists(fullPath):
            print('\nFile already exists. Loading data from CSV')
            file_df = self.load_raw_data_from_file(fullPath)
            print("From: " + str(file_df.head(1).index[0]))
            print("To: " + str(file_df.tail(1).index[0]))
            start = int((file_df.tail(1).index.astype(np.int64)/10**9)[0]) + period*60
            stop = start + MAX_FETCH_PERIOD + 1  # +1 for inclusivity
            all_df = [file_df]
        else:
            all_df = []

        all_fetched_df = []
        while stop < time.time() + MAX_FETCH_PERIOD:

            print('\nFetching data..')
            print("From: " + str(pd.to_datetime(start, unit='s')))
            print("To: " + str(pd.to_datetime(stop, unit='s')))
            
            data = self.cfClient.GetOhlc(str(market), limit=CF_DATA_LIMIT, period=period, fromArg=start, to=stop)
            if data is None:
                print("UNABLE TO COMPLETE UPDATE FOR: " + str(market))
                return None
            
            fetched_df = pd.DataFrame(data["ohlc"], columns=['ts', 'o', 'h', 'l', 'c', 'v'])
            fetched_df.columns = ('Datetime', 'Open', 'High', 'Low', 'Close', 'Volume')

            fetched_df = self.format_raw_data(fetched_df)
            
            all_fetched_df.append(fetched_df)

            start += MAX_FETCH_PERIOD
            stop += MAX_FETCH_PERIOD

            time.sleep(1)

        all_df += all_fetched_df
        main_df = pd.concat(all_df)
        main_df.drop_duplicates(inplace=True)
        main_df.sort_index(inplace=True)
        print(main_df.head())
        
        print("\nWriting to csv !!")
        if not os.path.exists(path):
            os.makedirs(path)
        main_df.to_csv(fullPath)
        
        return main_df

    def add_feature_log_return(self, df):
        if "return" in df:
            df["log_return"] = np.log(1+ df["return"])
            return df
        else:
            return None
    
    def add_feature_return(self, df): 
        df["return"] = df.Close.pct_change()
        return df
    
    def get_training_and_testing_data(self, n, m, data: list):
        
        # To numpy array
        x_list = np.array(data)
        y_list = np.array([[x[0]] for x in data])
             
        # Split training/test     
        split = int(len(data) * 0.8)
        x_train_splitted = x_list[:split]
        x_test_splitted = x_list[split: len(x_list)]
        y_train_splitted = y_list[:split]
        y_test_splitted = y_list[split: len(y_list)]
        
        # TODO OPTIMIZE ME PLEASE> THIS IS AWFUL !! 
        x_train = []
        x_test = []
        y_train = []
        y_test = []
        
        # TODO OPTIMIZE ME PLEASE> THIS IS AWFUL !! 
        for i in range(n, len(x_train_splitted) - m):
            x_train.append(x_train_splitted[i-n : i, : x_train_splitted.shape[1]])
            y_train.append(y_train_splitted[i : i+m, : x_train_splitted.shape[1]])
        for i in range(n, len(x_test_splitted) - m):
            x_test.append(x_test_splitted[i-n : i, : x_test_splitted.shape[1]])
            y_test.append(y_test_splitted[i : i+m, : x_test_splitted.shape[1]])
            
        # TODO OPTIMIZE ME PLEASE> THIS IS AWFUL !! 
        x_train, x_test, y_train, y_test = (np.array(x_train), np.array(x_test), np.array(y_train), np.array(y_test))
            
        x_train.reshape((x_train.shape[0], x_train.shape[1], x_train.shape[2]))
        y_train.reshape((y_train.shape[0], y_train.shape[1]))
        x_test.reshape((x_test.shape[0], x_test.shape[1], x_test.shape[2]))
        y_test.reshape((y_test.shape[0], y_test.shape[1]))
        
        return x_train, y_train, x_test, y_test
\
    
def main():
    dataManager = DataManager()
    marketList = {"btccad", "ethcad", "xrpcad", "ltccad", "btcusd", "ethusd", "xrpusd", "ltcusd", "btceur", "etheur",
                  "xrpeur", "ltceur", "xrpjpy", "xrpgbp", "xrpaed", "ethxrp", "btcxrp", "dashxrp", "ltcxrp", "zecxrp",
                  "btgxrp", "bchxrp", "zrxxrp", "gntxrp", "repxrp", "omgxrp", "saltxrp", "batxrp", "zilxrp",
                  "xlmusd", "xlmcad", "xlmeur", "xlmxrp", "dgbxrp", "cvcxrp", "loomxrp", "xrpusdc", "btcusdc"}
    for market in marketList:
        print("\n\n*****  " + str(market) + "  *****")
        dataManager.update_raw_data("coinfield", str(market), 5)


if __name__ == '__main__':
    main()
