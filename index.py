# -*- coding: utf-8 -*-

import os
import json
import datetime
import boto3
import time


boto_client = boto3.client('athena')


def fetchall_athena(query_string, client):
    query_id = client.start_query_execution(
        QueryString=query_string,
        QueryExecutionContext={
            'Database': 'ec_tax_registry'
        },
        ResultConfiguration={
            'OutputLocation': 's3://aws-athena-query-results-758359885368-us-west-2'
        }
    )['QueryExecutionId']
    query_status = None
    while query_status == 'QUEUED' or query_status == 'RUNNING' or query_status is None:
        query_status = client.get_query_execution(QueryExecutionId=query_id)['QueryExecution']['Status']['State']
        if query_status == 'FAILED' or query_status == 'CANCELLED':
            raise Exception('Athena query with the string "{}" failed or was cancelled'.format(query_string))
        time.sleep(0.25)
    results_paginator = client.get_paginator('get_query_results')
    results_iter = results_paginator.paginate(
        QueryExecutionId=query_id,
        PaginationConfig={
            'PageSize': 1
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


def not_found(body):
    return {"statusCode": 404,
            "body": json.dumps(body),
            "headers": {"Content-Type": "application/json"}}


def ok(body):
    return {"statusCode": 200,
            "body": json.dumps(body),
            "headers": {"Content-Type": "application/json"}}


def address(location):
    return "%s %s %s" % (location[13], location[14], location[15])


def location_to_tax_location(location):
    return {"tax_code": location[11],
            "commercial_name": location[2],
            "address": address(location),
            "city": location[18],
            "province": location[17],
            "status": location[16],
            "opening_date": location[5],
            "last_update": location[6],
            "business_activity": location[21]}
    


def tax_locations(locations):
    locations = list(map(location_to_tax_location, locations))
    return locations


def tax_entity(locations):
    return {"tax_id": locations[0][0],
            "legal_name": locations[0][1],
            "status": locations[0][3],
            "requires_accounting": locations[0][9],
            "locations": tax_locations(locations)}


def handler(event, context):
    qs = event['queryStringParameters']
    tax_id = qs.get('t', None)
    debug = qs.get('debug', None)
    if tax_id:
        query = "SELECT * FROM ec_tax_registry WHERE numero_ruc = '%s'" % (tax_id)
        athena_data = fetchall_athena(query, boto_client)
        entity = tax_entity(athena_data)
        if debug:
            entity["debug"] = {"event": event}
        return ok(entity)
    else:
        return not_found({"message": "RUC no encontrado."})
