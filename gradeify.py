#!python3

import csv
import os
from typing import Dict
from argparse import ArgumentParser
from datetime import datetime
from os import path


def main(filenames, due, outdir):
    if not path.isdir(outdir):
        os.makedirs(outdir)
    for fname in filenames:
        try:
            header = None
            grade_dct: Dict[str, Dict[str, str]] = {}

            with open(fname, 'r', encoding='utf-8') as orig:
                header = next(csv.reader(orig))
                orig.seek(0)
                reader = csv.DictReader(orig)

                for row in reader:
                    date = datetime.strptime(
                        row['Timestamp'],
                        "%Y-%m-%dT%H:%M:%S.%f%z"
                    )

                    uname = row['Username 1']

                    if uname not in grade_dct:
                        if date > due:
                            days_late = date.day - due.day + 1
                            points = max(
                                0,
                                int(row['Total']) - (10 * days_late)
                            )

                            row['Total'] = str(points)

                        grade_dct[uname] = row
                    else:
                        if date > due:
                            days_late = date.day - due.day + 1
                            points = max(
                                0,
                                int(row['Total']) - (10 * days_late)
                            )

                            if points > int(grade_dct[uname]['Total']):
                                row['Total'] = str(
                                    int(row['Total']) - (10 * days_late)
                                )

                                row['Total'] = str(points)
                                grade_dct[uname] = row

            with open(
                path.join(outdir, f"GRADED-{fname}"),
                'w',
                encoding='utf-8'
            ) as graded:
                writer = csv.DictWriter(graded, fieldnames=header)
                writer.writeheader()
                for row in grade_dct.values():
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
