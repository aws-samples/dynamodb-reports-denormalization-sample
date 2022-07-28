<!-- /*
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: MIT-0
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this
 * software and associated documentation files (the "Software"), to deal in the Software
 * without restriction, including without limitation the rights to use, copy, modify,
 * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */ -->

# Sample Report Scenario using Amazon DynamoDB Workbench

The purpose of this repository is to demonstrate the impact design decisions have while working with Amazon DynamoDB tables.

It is very common for developers that come from a relational background (RDBMS) to try to replicate the same normalization concepts in Amazon DynamoDB tables, trying to obtain the scalability, cost efficiency and throughput that Amazon DynamoDB can provide, however, data normalization could lead to data models that are not efficient specially from the cost perspective.

## Disclaimer

All the data, code and access patterns from this application was generated for sample purposes, even if we have seen customers implement very similar strategies Customer should always load test their scenarios and confirm it satisfies their application requirements, in terms of cost, response time, scalability and security. 

Before any production release, customers should conduct a risk assessment and incorporate additional security controls as required based on data classification and use cases. It is customer responsibility to ensure their application code satisfies their own internal security postures and implement mechanisms to mitigate and prevent sensitive data exposure. 

## How can I visualize datamodels before creating Amazon DynamoDB tables

You can [download NoSQL Workbench for Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.settingup.html) which is a cross-platform client-side GUI application for modern database development and operations and is available for Windows, macOS, and Linux. NoSQL Workbench is a unified visual IDE tool that provides data modelling, data visualization, and query development features to help you design, create, query, and manage DynamoDB tables.

Visit the AWS documentation for more information about [NoSQL workbench for Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html).

### Sample files 

This repository contains NoSQL datamodels to help you understand the difference between a normalized and a denormalized data model, please visit the [`/workbench`](./workbench/) folder for sample data models and sample csv information.

## Data 

All the fake information in this repository that you can find in the [`/data`](./data/) folder, was generated using [Mockaroo](https://www.mockaroo.com/) but you can use any tool that works for your situation, with the free samples on Mockaroo you can generate very complex datasets that are very useful specially in data denormalization scenarios. 

## Application code

The files in the [`/app`](./app/) folder are intended to help you visualize the difference in performance and cost while working with denormalized data models. For more information please visit the [INFO](./documentation/INFO.MD) section. 

# Contributing

Thank you for your interest in contributing to our project. Whether it's a bug report, new feature, correction, or additional documentation, we greatly value feedback and contributions from our community. Please revisit the [CONTRIBUTING](./CONTRIBUTING.md) file. 

## License
This library is licensed under the MIT-0 License. See the [LICENSE](./LICENSE) file. 