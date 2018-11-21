# -*- coding: utf-8 -*-

import json
import datetime
from jinja2 import Environment, FileSystemLoader


file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)


def handler(event, context):
    template = env.get_template('home.html')
    page = template.render()
    data = {
        'output': 'Hello World',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    return {'statusCode': 200,
            'body': page,
            'headers': {'Content-Type': 'text/html'}}
