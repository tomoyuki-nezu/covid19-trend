# Author: Tomoyuki Nezu
# tomoyuki (at) genemagic.com

import sys
import argparse
import csv


def process(fp):
	reader = csv.DictReader(fp)
	total_count = 0
	prev_count = 0
	print(f'No,公表_年月日')

	for row in reader:
		date = f"{row['年']}-{row['月']}-{row['日']}"
		count = int(row['PCR検査陽性者'])

		if count != prev_count:
			delta_count = count - prev_count
			for i in range(delta_count):
				print(f'{total_count},{date}')
				total_count += 1

		prev_count = count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?')
    args = parser.parse_args()

    if args.filename is None:
        process(sys.stdin)
    else:
        with open(args.filename) as f:
            process(f)

if __name__ == "__main__":
    main()