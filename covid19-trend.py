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
	parser.add_argument('--source', type=str, help="CSV data url or file.")
	parser.add_argument('--fast', type=int, default=12, help="Fast length.")
	parser.add_argument('--slow', type=int, default=26, help="Slow length.")
	parser.add_argument('--signal', type=int, default=9, help="Signal length.")
	parser.add_argument('--ma1', type=int, default=5, help="MA1 length.")
	parser.add_argument('--ma2', type=int, default=25, help="MA2 length.")
	parser.add_argument('--ma3', type=int, default=75, help="MA3 length.")
	parser.add_argument('--bbp', type=int, default=20, help="BB period.")
	parser.add_argument('--title', type=str, default="COVID19 Trend analysis.", help="Graph title.")
	args = parser.parse_args()
	return args

def process(args):
	if args.source is None:
		df = pd.read_csv(sys.stdin)
	else:
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

	bb_df = pd.DataFrame()
	bb_data = count_by_date_df['count'].values.tolist()
	bb_df['date'] = count_by_date_df['date']
	bb_df['close'] = count_by_date_df['count']
	bb_df['mean'] = bb_df['close'].rolling(window=args.bbp).mean()
	bb_df['std'] = bb_df['close'].rolling(window=args.bbp).std()
	bb_df['bb_up1'] = bb_df['mean'] + bb_df['std']
	bb_df['bb_up2'] = bb_df['mean'] + bb_df['std']*2
	bb_df['bb_low1'] = bb_df['mean'] - bb_df['std']
	bb_df['bb_low2'] = bb_df['mean'] - bb_df['std']*2

	fig, (fig1, fig2) = plt.subplots(2, 1, gridspec_kw = {'height_ratios':[3, 1]})

	fig1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
	fig1.set_title("Moving Average and Bollinger Bands")
	fig1.text(0.05, 0.90, f'Title: {args.title}', transform=fig1.transAxes)
	fig1.text(0.05, 0.80, f'MA1: {args.ma1}', transform=fig1.transAxes)
	fig1.text(0.05, 0.75, f'MA2: {args.ma2}', transform=fig1.transAxes)
	fig1.text(0.05, 0.70, f'MA3: {args.ma3}', transform=fig1.transAxes)
	fig1.bar(macd_df['date'], macd_df['close'], color="skyblue")
	fig1.plot(macd_df['date'], macd_df['sma_1'])
	fig1.plot(macd_df['date'], macd_df['sma_2'])
	fig1.plot(macd_df['date'], macd_df['sma_3'])

	fig1.text(0.05, 0.65, f'BBP: {args.bbp}', transform=fig1.transAxes)
	fig1.plot(bb_df['date'], bb_df['mean'], color="red", alpha=0.3)
	fig1.plot(bb_df['date'], bb_df['bb_up1'], color="red", alpha=0.3)
	fig1.plot(bb_df['date'], bb_df['bb_low1'], color="red", alpha=0.3)
	fig1.plot(bb_df['date'], bb_df['bb_up2'], color="red", alpha=0.3)
	fig1.plot(bb_df['date'], bb_df['bb_low2'], color="red", alpha=0.3)
	fig1.fill_between(bb_df['date'], bb_df['bb_up1'], bb_df['bb_low1'], color="pink", alpha=0.3)
	fig1.fill_between(bb_df['date'], bb_df['bb_up2'], bb_df['bb_low2'], color="pink", alpha=0.3)

	fig2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
	fig2.set_title("MACD")
	fig2.text(0.05, 0.80, f'Fast: {args.fast}', transform=fig2.transAxes)
	fig2.text(0.05, 0.65, f'Slow: {args.slow}', transform=fig2.transAxes)
	fig2.text(0.05, 0.50, f'Signal: {args.signal}', transform=fig2.transAxes)
	fig2.plot(macd_df['date'], macd_df['macd'])
	fig2.plot(macd_df['date'], macd_df['signal'])
 
	fig.tight_layout()
	plt.show()

def main():
	args = get_args()
	process(args)

if __name__ == '__main__':
    main()
