# -*- coding: utf-8 -*-

import os
import json
import datetime
from pyathenajdbc import connect


def search_tax_id(tax_id):
    conn = connect(s3_staging_dir='s3://ecuador-tax-registry/',
                   schema_name='ec_tax_registry',
                   region_name='us-west-2')

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT numero_ruc, razon_social, estado_contribuyente, numero_establecimiento, estado_establecimiento FROM ec_tax_registry
            WHERE numero_ruc = %(param)s
            """, {'param': tax_id})
            print(cursor.fetchall())
    finally:
        conn.close()


def handler(event, context):
    entity = {"data": search_tax_id('0992712554001'),
              "event": event}
    return {"statusCode": 200,
            "body": json.dumps(entity),
            "headers": {"Content-Type": "application/json"}}
