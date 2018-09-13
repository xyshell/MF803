'''
    data check: return(Stock)
    data source: Yahoo Finance...(p21) iVolatility, Bloomberg...(p22) 

    reading data:
        pd.read_csv / pd.read_html --> dataframe
        f = open(fname, 'r'):

    cleaning data:
        missing data: bootstrap, regression
        option data: no arbitrage

    database:
        keys: primary key, foreign key
        SQL: select insert update delete(select first)

    SQL:
        select ticker, price
        from Equity_prices
        where quote_date = 'today'
        order by mkt_value DESC / order by 3 DESC

        select from a join b on a.ticker = b.ticker

        select sum(shares) as shrs from pos group by ticker having shrs > 0 

        select from a join (sub-query) on ...

        select from where ticker in (sub-query)

        select ticker, case when ... (just if-else clause)

    Python connections on database:
        import pypyodbc (p55)

'''


