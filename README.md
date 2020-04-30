# covid19-trend

MA, MACD, and Bollinger Bands (1σ and 2σ) is calculated using the number of active persons per day.
It is based on the data format provided by Tokyo Metropolitan Government.


# Recommendation

  Python 3.6 or later, pandas, matplotlib (pyplot, dates).
  Developed in the Anaconda environment.


# How to use

From the command line run:

```
python covid19_trend.py --source https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv --fast 12 --slow 26 --signal 9 --ma1 7 --ma2 14 --ma3 30 --title "Tokyo active trend."
```

It also supports standard input:

```
curl https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv | python covid19_trend.py --fast 12 --slow 26 --signal 9 --ma1 7 --ma2 14 --ma3 30 --title "Tokyo active trend."
```

The arguments are as follows:

  --source
​	Specify the source file. You can specify the URL such as the CSV endpoint provided by Tokyo, or the CSV you have.
    130001_tokyo_covid19_patients.csv is the data as of 4/29 21:00 JST.

  --fast
    MACD short period (int, default: 12)

  --slow
    MACD longer period (int, default: 26)

  --signal
    MACD signal (int, default: 9)

  --ma1
    Moving Average (int, default: 5)

  --ma2
    Moving Average (int, default: 25)

  --ma3
    Moving Average (int, default: 75)

  --bbp
  	Bollinger Bands period (int, default: 20)

  --title
    Title to display on the graph (str, default: COVID19 Trend analysis.)


# toyokeizai-convert.py

 This is a script that converts CSV data provided by Toyokeizai to Tokyo Metropolitan Government format. Read data from standard input and output to standard output.

 ```
curl https://raw.githubusercontent.com/kaz-ogiwara/covid19/master/data/summary.csv | python toyokeizai-convert.py > output.csv
 ```

 Also can connect to covid19_trend.py with a pipe.

 ```
curl https://raw.githubusercontent.com/kaz-ogiwara/covid19/master/data/summary.csv | python toyokeizai-convert.py | python covid19-trend.py --fast 12 --slow 26 --signal 9 --ma1 7 --ma2 14 --ma3 30 --bbp 20 --title "Japan active trend."
 ```