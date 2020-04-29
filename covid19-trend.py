# Author: Tomoyuki Nezu
# tomoyuki (at) genemagic.com

import sys
import argparse
import csv
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--source', type=str, default="https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv", help="CSV data url or file.")
	parser.add_argument('--fast', type=int, default=12, help="Fast length.")
	parser.add_argument('--slow', type=int, default=26, help="Slow length.")
	parser.add_argument('--signal', type=int, default=9, help="Signal length.")
	parser.add_argument('--ma1', type=int, default=5, help="MA1 length.")
	parser.add_argument('--ma2', type=int, default=25, help="MA2 length.")
	parser.add_argument('--ma3', type=int, default=75, help="MA3 length.")
	args = parser.parse_args()
	return args

def main():
	args = get_args()

	df = pd.read_csv(args.source)
	df['公表_年月日'] = pd.to_datetime(df['公表_年月日'], format="%Y-%m-%d")

	tmp_df = df[['公表_年月日']].copy()
	tmp_df['count'] = 1
	tmp_df.rename(columns={'公表_年月日': 'date'}, inplace=True)

	count_by_date_df = tmp_df.groupby(tmp_df['date']).count()
	count_by_date_df = count_by_date_df.asfreq(freq='D', fill_value=0)
	count_by_date_df.reset_index(inplace=True)

	macd_df = pd.DataFrame()
	macd_df['date'] = count_by_date_df['date']
	macd_df['close'] = count_by_date_df['count']
	macd_df['sma_1'] = count_by_date_df['count'].rolling(args.ma1).mean()
	macd_df['sma_2'] = count_by_date_df['count'].rolling(args.ma2).mean()
	macd_df['sma_3'] = count_by_date_df['count'].rolling(args.ma3).mean()
	macd_df['ema_fast'] = count_by_date_df['count'].ewm(span=args.fast).mean()
	macd_df['ema_slow'] = count_by_date_df['count'].ewm(span=args.slow).mean()
	macd_df['macd'] = macd_df['ema_fast'] - macd_df['ema_slow']
	macd_df['signal'] = macd_df['macd'].ewm(span=args.signal).mean()

	fig, (fig1, fig2) = plt.subplots(2, 1, gridspec_kw = {'height_ratios':[3, 1]})

	fig1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
	fig1.set_title("Moving Average")
	fig1.text(0.05, 0.90, f'MA1: {args.ma1}', transform=fig1.transAxes)
	fig1.text(0.05, 0.85, f'MA2: {args.ma2}', transform=fig1.transAxes)
	fig1.text(0.05, 0.80, f'MA3: {args.ma3}', transform=fig1.transAxes)
	fig1.bar(macd_df['date'], macd_df['close'], color="skyblue")
	fig1.plot(macd_df['date'], macd_df['sma_1'])
	fig1.plot(macd_df['date'], macd_df['sma_2'])
	fig1.plot(macd_df['date'], macd_df['sma_3'])

	fig2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
	fig2.set_title("MACD")
	fig2.text(0.05, 0.80, f'Fast: {args.fast}', transform=fig2.transAxes)
	fig2.text(0.05, 0.65, f'Slow: {args.slow}', transform=fig2.transAxes)
	fig2.text(0.05, 0.50, f'Signal: {args.signal}', transform=fig2.transAxes)
	fig2.plot(macd_df['date'], macd_df['macd'])
	fig2.plot(macd_df['date'], macd_df['signal'])
 
	fig.tight_layout()
	plt.show()

if __name__ == '__main__':
    main()
