#!python3

import csv
import os
from os import path
from argparse import ArgumentParser
from datetime import datetime


def main(filenames, due, outdir):
    if not path.isdir(outdir):
        os.makedirs(outdir)
    for fname in filenames:
        try:
            with open(fname, 'r', encoding='utf-8') as orig:
                with open(
                    path.join(outdir, f"LATEIFIED-{fname}"),
                    'w',
                    encoding='utf-8'
                ) as lateified:
                    header = next(csv.reader(orig))
                    orig.seek(0)
                    reader = csv.DictReader(orig)
                    writer = csv.DictWriter(lateified, fieldnames=header)

                    for row in reader:
                        date = datetime.strptime(
                            row['Timestamp'],
                            "%Y-%m-%d %H:%M:%S.%f%z"
                        )

                        if date > due:
                            days_late = due.day - date.day + 1

                            row['Total Points'] = str(
                                int(row['Total Points']) - (10 * days_late)
                            )

                        writer.writerow(row)

        except FileNotFoundError:
            print(f"{fname} not found. skipping...")


if __name__ == '__main__':
    parser = ArgumentParser(
        description="Late penalizer for ENGR-E111 at IU.",
        epilog="""Copyright (C) 2022 Drason Chow

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
    )

    parser.add_argument(
        'filenames',
        metavar='files',
        type=str,
        nargs='+',
        help="files to process"
    )

    parser.add_argument(
        "--due",
        "-u",
        help="Due date in in Year-Month-Day. E.g. 2022-02-22",
        type=str,
        required=True
    )

    parser.add_argument(
        "--dir",
        "-d",
        help="Output directory",
        type=str,
        default=".",
        required=False
    )

    args = parser.parse_args()
    main(
        args.filenames,
        datetime.strptime(f"{args.due}+00:00", "%Y-%m-%d%z"),
        args.dir
    )
