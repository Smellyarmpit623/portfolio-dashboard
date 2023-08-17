import streamlit as st
import time
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import threading
import time 


st.set_page_config(
    page_title="投资组合追踪",
    page_icon="😊",
    layout="wide",
    
)



def options_chain(symbol,expirationDate):

    tk = yf.Ticker(symbol)
    # Expiration dates
    exps = tk.options

    # Get options for each expiration
    options = pd.DataFrame()
    try:
        opt = tk.option_chain(expirationDate)
        opt = pd.DataFrame()._append(opt.calls)._append(opt.puts)
        options = options._append(opt, ignore_index=True)
        
    except:
        pass
    
    # Boolean column if the option is a CALL
    options['CALL'] = options['contractSymbol'].str[4:].apply(
        lambda x: "C" in x)
    
    options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)
    options['mark'] = (options['bid'] + options['ask']) / 2 # Calculate the midpoint of the bid-ask
    
    # Drop unnecessary and meaningless columns
    options = options.drop(columns = ['contractSize', 'currency', 'change', 'percentChange', 'lastTradeDate', 'lastPrice'])

    return options

class instrument:
    def __init__(self,ticker:str,qty:float,cost_price:float,chinese_name:str,option=False,option_ticker="",expirationDate="",direction="",strike=0):
        self.ticker=ticker
        self.strike=strike
        self.direction=direction
        self.chinese_name=chinese_name
        self.option_ticker=option_ticker
        self.option=option
        self.qty=qty
        self.cost_price=cost_price
        self.current_price=0.00
        self.market_value=self.qty*self.cost_price
        self.underlying_price=0
        self.expirationDate=expirationDate
        self.note=""
        if self.option:
            self.market_value*100   
        
        
    def update(self):
        if self.option:
            data=(options_chain(self.ticker,self.expirationDate))
            self.current_price=round((round(data[data["contractSymbol"]==self.option_ticker].iloc[-1]["ask"],3)+round(data[data["contractSymbol"]==self.option_ticker].iloc[-1]["bid"],3))/2,3)
            self.market_value=self.current_price*self.qty*100
            tk = yf.Ticker(self.ticker)
            data = tk.history()
            last_quote = data['Close'].iloc[-1]
            self.underlying_price=round(last_quote,3)
        else:
            tk = yf.Ticker(self.ticker)
            data = tk.history()
            last_quote = data['Close'].iloc[-1]
            self.current_price=round(last_quote,3)
            self.market_value=self.current_price*self.qty
            self.underlying_price=self.current_price


    def add_note(self,note:str):
        self.note=note
            
if __name__=="__main__" :
    t = st.empty()
    netvalue = st.empty()
    netvalue_note=st.empty()
    new=instrument(ticker="SOXL",qty=50,cost_price=3.161,chinese_name="三倍做多半导体",option=True,option_ticker="SOXL240119C00030000",expirationDate='2024-01-19',strike=30,direction="看涨期权")
    new1=instrument(ticker="SOXL",qty=120,cost_price=5,chinese_name="三倍做多半导体",option=True,option_ticker="SOXL250117C00040000",expirationDate='2025-01-17',strike=40,direction="看涨期权")
    new2=instrument(ticker="TNA",qty=15,cost_price=8.505,chinese_name="三倍做多罗素2000小盘股",option=True,option_ticker="TNA250117C00040000",expirationDate='2025-01-17',strike=40,direction="看涨期权")
    new3=instrument(ticker="JEPI",qty=180,cost_price=54.686,chinese_name="摩根大通股票收入 ETF",option=False)
    new4=instrument(ticker="JEPQ",qty=200,cost_price=47.755,chinese_name="摩根大通纳斯达克股票 ETF",option=False)
    new5=instrument(ticker="LABU",qty=200,cost_price=0.452,chinese_name="三倍做多生物科技",option=True,option_ticker="LABU240119C00010000",expirationDate='2024-01-19',strike=10,direction="看涨期权")
    new6=instrument(ticker="LABU",qty=40,cost_price=2.107,chinese_name="三倍做多生物科技",option=True,option_ticker="LABU250117C00007000",expirationDate='2025-01-17',strike=7,direction="看涨期权")
    new7=instrument(ticker="EZJ",qty=50,cost_price=1.46,chinese_name="MSCI 日本 ETF",option=True,option_ticker="EZJ240119C00041000",expirationDate='2024-01-19',strike=41,direction="看涨期权")
    new8=instrument(ticker="EWJ",qty=100,cost_price=0.809,chinese_name="IShare MSCI 日本 ETF",option=True,option_ticker="EWJ250117C00080000",expirationDate='2025-01-17',strike=80,direction="看涨期权")
    new9=instrument(ticker="HIBL",qty=11,cost_price=2.262,chinese_name="三倍做多 高Beta股",option=True,option_ticker="HIBL240216C00045000",expirationDate='2024-02-16',strike=45,direction="看涨期权")
    new10=instrument(ticker="TMF",qty=150,cost_price=1.479,chinese_name="三倍做多20年期美国国债收益率指数",option=True,option_ticker="TMF250117C00010000",expirationDate='2025-01-17',strike=10,direction="看涨期权")
    new11=instrument(ticker="PEY",qty=300,cost_price=19.675,chinese_name="Invesco 高收益股票股息 ETF",option=False)
    new12=instrument(ticker="PFE",qty=120,cost_price=36.199,chinese_name="辉瑞",option=False)
    new13=instrument(ticker="VZ",qty=100,cost_price=35.06,chinese_name="威瑞森",option=False)
    new14=instrument(ticker="IQ",qty=30,cost_price=1.177,chinese_name="爱奇艺",option=True,option_ticker="IQ240119C00005000",expirationDate='2024-01-19',strike=5,direction="看涨期权")
    new15=instrument(ticker="O",qty=50,cost_price=60.76,chinese_name="房地产收入公司",option=False)
    new16=instrument(ticker="MO",qty=50,cost_price=45.825,chinese_name="奥驰亚集团",option=False)
    new17=instrument(ticker="TNA",qty=30,cost_price=0.805,chinese_name="三倍做多罗素2000小盘股",option=True,option_ticker="TNA240119C00060000",expirationDate='2024-01-19',strike=60,direction="看涨期权")






    

    list1=[new,new1,new2,new3,new4,new5,new6,new7,new8,new9,new10,new11,new12,new13,new14,new15,new16,new17]

    while True:
        for i in list1:
            i.update()
        tickers,options,directions,experiationdates,chinese_names,qtys,cost_prices,current_prices,market_values,strikes,notes,pnl,theo,under,nlv=[],[],[],[],[],[],[],[],[],[],[],[],[],[],0.00
        for i in list1:
            tickers.append(i.ticker)
            options.append(i.option)
            directions.append(i.direction)
            experiationdates.append(i.expirationDate)
            chinese_names.append(i.chinese_name)
            qtys.append(i.qty)
            cost_prices.append(i.cost_price)
            current_prices.append(i.current_price)
            market_values.append(i.market_value)
            strikes.append(i.strike)
            notes.append(i.note)
            under.append(i.underlying_price)
            if i.option:
                pnl.append((i.current_price-i.cost_price)*i.qty*100)
            else:
                pnl.append((i.current_price-i.cost_price)*i.qty)
            nlv+=i.market_value
            
            
            
        table={"代码":tickers,"期权?":options,"期权方向":directions,"期权到期日":experiationdates,"行权价":strikes,"中文":chinese_names,"头寸数量":qtys,"平均持仓价格":cost_prices,"现价(期权价格为中间价)":current_prices,"标的资产价格":under,"市场价值":market_values,"未实现盈亏":pnl,"说明":notes}
        df=pd.DataFrame(data=table)
        t.dataframe(data=df)
        netvalue.text("Net liquidate value 净清算值: $"+str(round(nlv,3))+" 澳元: $"+str(round(nlv*1.4679,3)))
        netvalue_note.text("净清算值仅为理论值 具体值以最终值为准\n由于期权流通性问题期权现价用中间值计算 并非最新成交价")
        time.sleep(5)
