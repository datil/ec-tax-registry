# -*- coding: utf-8 -*-

import os
import json
import datetime
import boto3
import time


def fetchall_athena(query_string, client):
    query_id = client.start_query_execution(
        QueryString=query_string,
        QueryExecutionContext={
            'Database': 'ec_tax_registry'
        },
        ResultConfiguration={
            'OutputLocation': 's3://ec-tax-registry-query-results'
        }
    )['QueryExecutionId']
    query_status = None
    while query_status == 'QUEUED' or query_status == 'RUNNING' or query_status is None:
        query_status = client.get_query_execution(QueryExecutionId=query_id)['QueryExecution']['Status']['State']
        if query_status == 'FAILED' or query_status == 'CANCELLED':
            raise Exception('Athena query with the string "{}" failed or was cancelled'.format(query_string))
        time.sleep(10)
    results_paginator = client.get_paginator('get_query_results')
    results_iter = results_paginator.paginate(
        QueryExecutionId=query_id,
        PaginationConfig={
            'PageSize': 1000
        }
    )
    results = []
    data_list = []
    for results_page in results_iter:
        for row in results_page['ResultSet']['Rows']:
            data_list.append(row['Data'])
    for datum in data_list[1:]:
        results.append([x['VarCharValue'] for x in datum])
    return [tuple(x) for x in results]


def handler(event, context):
    boto_client = boto3.client('athena')
    athena_data = fetchall_athena("SELECT * FROM ec_tax_registry WHERE numero_ruc = '0992712554001'", boto_client)
    entity = {"data": athena_data,
              "event": event}
    return {"statusCode": 200,
            "body": json.dumps(entity),
            "headers": {"Content-Type": "application/json"}}
