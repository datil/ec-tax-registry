import json
import datetime
from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(
    loader=PackageLoader('ec-sri-registry', 'templates'),
    autoescape=select_autoescape(['html'])
)


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
