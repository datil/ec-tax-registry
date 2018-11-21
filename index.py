# -*- coding: utf-8 -*-

import os
import json
import datetime
from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader(os.path.abspath("templates/" + os.path.dirname(__file__))))


def handler(event, context):
    template = env.get_template("home.html")
    page = template.render()
    return {"statusCode": 200,
            "body": page,
            "headers": {"Content-Type": "text/html"}}
