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

simulate_operations_base.py
Retrieves from a list of given users and organizations a set of reports during 60 seconds

Every second there is a query to the get_report_by_user and every 10 seconds you obtain the reports
for a given organization with some random status. After each query the RCU consumption is printed.

This file calls the base table created in the example which is the original data model.
"""
from random import SystemRandom
from time import sleep

from operations import get_base_reports_by_org, get_base_reports_by_user_id

user_list = [
    "npedder0",
    "baddie1",
    "cwarin2",
    "cwestover4",
    "gboddington4",
    "jbates3",
    "gmerioth3",
    "ftamsett5",
    "ebrunicke5",
    "dkemitt6",
    "pbaldoni6",
    "sughelli7",
    "dduckhouse7",
    "cbrigge8",
    "aderdes8",
]

org_list = ["alfa", "beta", "gamma", "delta", "epsilon", "zeta"]

DATE = "2022-06-05"
status_list = ["ASSIGNED", "INPROGRESS", "CREATED"]

if __name__ == "__main__":
    counter = 0
    while counter <= 60:
        get_base_reports_by_user_id(SystemRandom.choice(user_list), DATE)
        if counter % 10 == 0:
            get_base_reports_by_org(SystemRandom.choice(org_list), DATE)
        sleep(1)
        counter += 1
