# covid19-trend

MA, MACD is calculated using the number of active persons per day.
It is based on the data format provided by Tokyo Metropolitan Government.


# Recommendation

  Python 3.6 or later, pandas, matplotlib (pyplot, dates).
  Developed in the Anaconda environment.


# How to use

From the command line run:

```
python covid19_trend.py --source https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv --fast 12 --slow 26 --signal 9 --ma1 7 --ma2 14 --ma3 30
```

The arguments are as follows:

  --source
​	Specify the source file. You can specify the URL such as the CSV endpoint provided by Tokyo, or the CSV you have.
    130001_tokyo_covid19_patients.csv is the data as of 4/29 21:00 JST.

  --fast
    short period (int, default: 12)

  --slow
    longer period (int, default: 26)

  --signal
    signal (int, default: 9)

  --ma1
    moving average (int, default: 5)

  --ma2
    moving average (int, default: 25)

  --ma3
    moving average (int, default: 75)