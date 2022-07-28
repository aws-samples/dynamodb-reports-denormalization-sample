"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

set_report_size.py
Updates the report size on the original table to a realistic value.
"""
from time import time
from operations import update_small_attribute, scan_table, update_report_data

report_data = ""

with open("../data/big_blobs.txt", "r") as file:
    for row in file:
        report_data = row

reports = scan_table()

print("Updating attributes with small report size: ")
start = time()
for report in reports:
    print("Updating Report ", report["report_id"]["S"])
    update_small_attribute(report)
    print("")
end = time()

print(f"To perform an small update operation it took {end - start}")


print("Updating attributes with the real report size: ")
start = time()
for report in reports:
    print("Updating Report ", report["report_id"]["S"])
    update_report_data(report, report_data)
    print("")
end = time()

print(f"Updating report size to the right value {end - start}")
