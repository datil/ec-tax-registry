# -*- coding: utf-8 -*-

import os
import json
import datetime


def handler(event, context):
    entity = {
        "tax_id": "0992712554001",
        "locations": []
    }
    return {"statusCode": 200,
            "body": json.dumps(entity),
            "headers": {"Content-Type": "application/json"}}
