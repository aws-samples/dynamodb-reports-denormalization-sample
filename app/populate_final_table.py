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

populate_final_table.py
When you execute this file it will take the information in the base_report_data json file 
and insert it in the Amazon DynamoDB table, using a batch write item operation.

In this scenario each one of the rows read form the file need to be denormalized because we
will be using different sort keys to denormalize the data, for example:

report_id ( 1 ), location
report_id ( 1 ), organization
report_id ( 1 ), user_id

The for loop will read each line from the json file and then distribute among the different 
entities.
"""
import json
from operations import write_item

reports = []

with open("../data/final_model.json", "r") as file:
    for row in file:
        report = json.loads(row)
        # Report Data entity, we only store the report and some basic attributes
        reports.append(
            {
                "PK": report["report_id"],
                "SK": "report_data",
                "created_date": report["created_date"],
                "report_data": report["report_data"],
                "report_id": report["report_id"],
            }
        )
        # Report Location, we store a lot of informaiton about the report location and
        # Include a GSI1PK and GSI1SK to query based on the location.
        reports.append(
            {
                "PK": report["report_id"],
                "SK": "location",
                "report_id": report["report_id"],
                "status": report["status"],
                "city": report["city"],
                "country": report["country"],
                "created_date": report["created_date"],
                "organization": report["organization"],
                "GSI1PK": "LOC#" + report["organization"],
                "GSI1SK": report["location"]
                + "#"
                + report["status"]
                + "#"
                + report["created_date"],
            }
        )
        # Report Organization, we store a lot of informaiton about the report organization and
        # Include a GSI1PK and GSI1SK to query based on the organization.
        reports.append(
            {
                "PK": report["report_id"],
                "SK": "organization",
                "status": report["status"],
                "report_id": report["report_id"],
                "created_date": report["created_date"],
                "organization": report["organization"],
                "GSI1PK": "ORG#" + report["organization"],
                "GSI1SK": report["status"] + "#" + report["created_date"],
            }
        )
        # Report Requested by, we store a lot of informaiton about the user that requested the
        # report and Include a GSI1PK and GSI1SK to query based on this user.
        reports.append(
            {
                "PK": report["report_id"],
                "SK": "requested_by",
                "status": report["status"],
                "report_id": report["report_id"],
                "created_date": report["created_date"],
                "requested_by": report["requested_by"],
                "GSI1PK": "REQ#" + report["requested_by"],
                "GSI1SK": report["status"] + "#" + report["created_date"],
            }
        )
        # Report user_id, we store a lot of informaiton about the user working on the report and
        # Include a GSI1PK and GSI1SK to query based on this user.
        reports.append(
            {
                "PK": report["report_id"],
                "SK": "user_id",
                "status": report["status"],
                "report_id": report["report_id"],
                "created_date": report["created_date"],
                "user_id": report["user_id"],
                "GSI1PK": "UID#" + report["user_id"],
                "GSI1SK": report["status"] + "#" + report["created_date"],
            }
        )


write_item(reports, "reports_global")
