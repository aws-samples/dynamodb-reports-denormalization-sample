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
 
 
operations.py

This file contains a set of helper functions, that will read, write, update elements
in the Amazon DynamoDB tables in this example. The aim of this file is to make cleaner
the other examples and remove the low level operations from the concept itself. 
    
"""
import json
from time import time
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
ddb_client = boto3.client("dynamodb")

reports_table = "report_data_exploration"
table = dynamodb.Table(reports_table)


def scan_table():
    """
    Scans a dynamodb table single threaded, no need to paginate on this example.
    This function it is intendely used to scan a particular DynamoDB Table with
    20 small items, in this specific example these items don't need pagination.

    Returns:
        _type_: _description_
    """
    try:
        start = time()
        response = ddb_client.scan(
            TableName=reports_table, ReturnConsumedCapacity="INDEXES"
        )
        end = time()
        print(f"Scan time: {end - start}")
        print(response["ConsumedCapacity"])
    except Exception as e:
        print("There was an exception while scanning the table: ")
        print(json.dumps(e, indent=4))
    else:
        return response["Items"]


def update_small_attribute(report):
    """
    Helper function that updates an small atrtribute from the table, updated_date.
    The report is the result of a table scan and this function
    will be used to write inside an iterator.

    Args:
        report (DDB JSON): DynamoDB Json that you can get as a result of a scan table
                            operation

    Returns:
        String: Consumed Capacity Units
    """
    try:
        date = datetime.now().isoformat()
        start = time()
        response = table.update_item(
            Key={"report_id": report["report_id"]["S"]},
            UpdateExpression="set updated_date = :r",
            ExpressionAttributeValues={
                ":r": date,
            },
            ReturnValues="UPDATED_NEW",
            ReturnConsumedCapacity="INDEXES",
        )
        end = time()
    except Exception as e:
        print("There was an exception in the update: ")
        print(json.dumps(e, indent=4))
    else:
        print(f"Update time: {end - start}")
        print(f"Consumed WCU:")
        print(response["ConsumedCapacity"])
        return response


def update_report_data(report, report_data):
    """
    Helper function that updates the items from the reports table
    The report data is the result of a table scan and this function
    will be used to write inside an iterator.

    Args:
        report (DDB JSON): DDB Item.
        report_data (string): BLOB encoded in UTF8 as string for simplicity

    Returns:
        String: Consumed Capacity Units
    """
    try:
        date = datetime.now().isoformat()
        start = time()
        response = table.update_item(
            Key={"report_id": report["report_id"]["S"]},
            UpdateExpression="set report_data = :r",
            ExpressionAttributeValues={
                ":r": report_data,
            },
            ReturnValues="UPDATED_NEW",
            ReturnConsumedCapacity="INDEXES",
        )
        end = time()
    except Exception as e:
        print("There was an exception in the update: ")
        print(json.dumps(e, indent=4))
    else:
        print(f"Update time: {end - start}")
        print(f"Consumed WCU:")
        print(response["ConsumedCapacity"])
        return response


def write_item(items, table_name=reports_table):
    """
    Helper function that writes a JSON array to DynamoDB, the json array needs to include the
    partition key and sort key for the table.

    Args:
        items (JSON Array): All the items that will be stored
        table_name (String, optional): Table that will be used. Defaults to reports_table.
    """
    try:
        table = dynamodb.Table(table_name)
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)
    except ClientError as e:
        print("Error writting to the DDB table.")
        print(e.response["Error"]["Message"])
    else:
        print("Success!")


def get_reports_by_user_id(pk, sk, table_name=reports_table):
    """
    Helper function that executes a query operation to the reusable GSI, on the UserID entity

    Args:
        pk (string): GSI1PK - This is based on the UserId entity, this function adds the UID# prefix
        sk (string): GSI1SK - Based on your entity,
                                - [STATUS]#[Date] - STATUS as COMPLETE, ASSIGNED, INPROGRESS, CREATED
                                - [COUNTRY]#[CITY]#[STATUS]#[Date]
        table_name (string, optional): Name of the DDB table. Defaults to "reports_table".

    Returns:
        {
            "capacity_units": (float), the total number of RCUs consumed,
            "response": (ddb-json), the reports returned by the query.
        }
    """
    try:
        start = time()
        resp = ddb_client.query(
            TableName=table_name,
            IndexName="query-index",
            KeyConditionExpression="GSI1PK = :pk AND begins_with ( GSI1SK , :sk )",
            ExpressionAttributeValues={
                ":pk": {"S": "UID#{}".format(pk)},
                ":sk": {"S": "{}".format(sk)},
            },
            ScanIndexForward=True,
            ReturnConsumedCapacity="TOTAL",
        )
        end = time()
    except Exception as e:
        print("There was an exception while getting the report: ")
        print(json.dumps(e, indent=4))
    else:
        print(
            "Get Reports by user_id - Operation time: {}, RCU: {}".format(
                end - start, resp["ConsumedCapacity"]["CapacityUnits"]
            )
        )
        return {
            "capacity_units": float(resp["ConsumedCapacity"]["CapacityUnits"]),
            "response": resp["Items"],
        }


def get_reports_by_org(pk, sk, table_name=reports_table):
    """
    Helper function that executes a query operation to the reusable GSI, on the Organization entity

    Args:
        pk (string): GSI1PK - This is based on the organization entity, this function adds the ORG# prefix
        sk (string): GSI1SK - Based on your entity,
                                - [STATUS]#[Date] - STATUS as COMPLETE, ASSIGNED, INPROGRESS, CREATED
                                - [COUNTRY]#[CITY]#[STATUS]#[Date]
        table_name (string, optional): Name of the DDB table. Defaults to "reports_table".

    Returns:
        {
            "capacity_units": (float), the total number of RCUs consumed,
            "response": (ddb-json), the reports returned by the query.
        }
    """
    try:
        start = time()
        resp = ddb_client.query(
            TableName=table_name,
            IndexName="query-index",
            KeyConditionExpression="GSI1PK = :pk AND begins_with ( GSI1SK , :sk )",
            ExpressionAttributeValues={
                ":pk": {"S": "ORG#{}".format(pk)},
                ":sk": {"S": "{}".format(sk)},
            },
            ScanIndexForward=True,
            ReturnConsumedCapacity="TOTAL",
        )
        end = time()
    except Exception as e:
        print("There was an exception while getting the report: ")
        print(json.dumps(e, indent=4))
    else:
        print(
            "Get Reports by organization - Operation time: {}, RCU: {}".format(
                end - start, resp["ConsumedCapacity"]["CapacityUnits"]
            )
        )
        return {
            "capacity_units": float(resp["ConsumedCapacity"]["CapacityUnits"]),
            "response": resp["Items"],
        }


def get_base_reports_by_user_id(pk, sk, table_name=reports_table):
    """
    Helper function that executes a query operation to the reports_table, using the
    user_id index.

    Args:
        pk (string): user_id, as specified in the base table.
        sk (string): date in ISO8601 format example 2022-06-03T18:01:18Z
        table_name (string, optional): Name of the DDB table. Defaults to "reports_table".

    Returns:
        {
            "capacity_units": (float), the total number of RCUs consumed,
            "response": (ddb-json), the reports returned by the query.
        }
    """
    try:
        start = time()
        resp = ddb_client.query(
            TableName=table_name,
            IndexName="user_id_index",
            KeyConditionExpression="user_id = :pk AND begins_with ( created_date , :sk )",
            ExpressionAttributeValues={
                ":pk": {"S": "{}".format(pk)},
                ":sk": {"S": "{}".format(sk)},
            },
            ScanIndexForward=True,
            ReturnConsumedCapacity="TOTAL",
        )
        end = time()
    except Exception as e:
        print("There was an exception while getting the report: ")
        print(json.dumps(e, indent=4))
    else:
        print(
            "Get Base Reports by user_id - Operation time: {}, RCU: {}".format(
                end - start, resp["ConsumedCapacity"]["CapacityUnits"]
            )
        )
        return {
            "capacity_units": float(resp["ConsumedCapacity"]["CapacityUnits"]),
            "response": resp["Items"],
        }


def get_base_reports_by_org(pk, sk, table_name=reports_table):
    """
    Helper function that executes a query operation to the reports_table. using the
    organization_index.

    Args:
        pk (string): organization, as specified in the base table.
        sk (string): date in ISO8601 format example 2022-06-03T18:01:18Z
        table_name (string, optional): Name of the DDB table. Defaults to "reports_table".

    Returns:
        {
            "capacity_units": (float), the total number of RCUs consumed,
            "response": (ddb-json), the reports returned by the query.
        }
    """
    try:
        start = time()
        resp = ddb_client.query(
            TableName=table_name,
            IndexName="organization_index",
            KeyConditionExpression="organization = :pk AND begins_with ( created_date , :sk )",
            ExpressionAttributeValues={
                ":pk": {"S": "{}".format(pk)},
                ":sk": {"S": "{}".format(sk)},
            },
            ScanIndexForward=True,
            ReturnConsumedCapacity="TOTAL",
        )
        end = time()
    except Exception as e:
        print("There was an exception while getting the report: ")
        print(json.dumps(e, indent=4))
    else:
        print(
            "Get Base Reports by organization - Operation time: {}, RCU: {}".format(
                end - start, resp["ConsumedCapacity"]["CapacityUnits"]
            )
        )
        return {
            "capacity_units": float(resp["ConsumedCapacity"]["CapacityUnits"]),
            "response": resp["Items"],
        }
