from flask import Flask
from flask import request
from flask import jsonify

from vcounter.lib.db import Redis as DataBase
from vcounter.lib.config import Config
from vcounter.helper import now_timestamp
from vcounter.helper import url_to_domain
from vcounter.entities import InvalidUsage

app = Flask(__name__)
config = Config()
db = DataBase()


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    app.logger.error(f"status_code: {error.status_code}. Message: {error.message}")
    return response


@app.route('/', methods=['GET'])
def status_page():
    """ Status page. Shows how health of the service """
    app.logger.debug('Status page requested')
    content = {
        'status': 'ok'
    }

    if not db.status():
        content['status'] = 'error'
        content['db'] = 'error'

    return jsonify(content)


@app.route('/visited_links', methods=['POST'])
def visited_links():
    """
    Endpoint for posting visitation data. Correct data example:

    {
      "links": [
        "https://ya.ru",
        "https://ya.ru?q=123",
        "http://www.yandex.ru"
      ]
    }
    """
    app.logger.debug('Add visits page requested')
    content = {
        'status': 'ok'
    }

    timestamp = now_timestamp()
    data = request.get_json()

    if not data:
        raise InvalidUsage(message='Empty POST received')

    if 'links' not in data:
        raise InvalidUsage(message='Wrong request: no visited links specified in request')

    if not data['links']:
        return jsonify(content)

    for url in data['links']:
        domain = url_to_domain(url)
        db.domain_register(timestamp, domain)

    return jsonify(content)


@app.route('/visited_domains', methods=['GET'])
def visited_domains():
    """
    Endpoint for filtering data from database.

    Returns JSON:

    {
      "domains":[
        "ya.ru",
        "yandex.ru"
      ]
    }
    """
    app.logger.debug('Get visits page requested')
    content = {
        "domains": [],
        "status": "ok"
    }

    if 'from' not in request.args:
        raise InvalidUsage(message='No "from" parameter specified')
    else:
        from_timestamp = int(request.args.get('from'))

    if 'to' not in request.args:
        raise InvalidUsage(message='No "to" parameter specified')
    else:
        to_timestamp = int(request.args.get('to'))

    filtered_domains = set()
    for domain_name in db.domain_filter(from_timestamp, to_timestamp):
        filtered_domains.add(domain_name)

    if len(filtered_domains):
        content['domains'] = list(filtered_domains)

    return jsonify(content)
