from vcounter.server import app
from vcounter.lib.db import Redis as DataBase
from vcounter.helper import now_timestamp
from vcounter.helper import url_to_domain
from vcounter.lib.config import Config


config = Config()
db = DataBase(config.db_test_index)


def test_url_to_domain():
    """ Test URL to domain parsing """
    assert url_to_domain('http://example.com') == 'example.com'
    assert url_to_domain('https://example.com') == 'example.com'
    assert url_to_domain('https://example.com/?v=1') == 'example.com'
    assert url_to_domain('https://www.example.com/?v=1') == 'www.example.com'
    assert url_to_domain('https://www.www.example.com/?v=1') == 'www.www.example.com'
    assert url_to_domain('example.com') == 'example.com'


def test_config():
    """ Test configuration class """
    assert isinstance(config.db_get_key_string_by_name('test_key'), str)
    assert isinstance(config.debug, bool)
    assert isinstance(config.server_host, str)
    assert isinstance(config.server_port, int)
    assert isinstance(config.db_host, str)
    assert isinstance(config.db_port, int)
    assert isinstance(config.db_port, int)
    assert isinstance(config.db_index, int)
    assert isinstance(config.db_test_index, int)
    assert isinstance(config.db_key_prefix, str)
    assert isinstance(config.log_file_path, str)

    rotation_after, retention = config.log_rotation_settings
    assert isinstance(rotation_after, str)
    assert isinstance(retention, str)


class TestStatusPage:

    client = None

    def setup(self):
        app.testing = True
        self.client = app.test_client()

    def test(self):
        """ Simple test for service status page """
        response = self.client.get('/')
        response_body = response.get_json()

        assert response.status_code == 200
        assert 'status' in response_body
        assert response_body['status'] == 'ok'


class TestVisitsAdd:

    client = None
    asset_post_payload = {
        "links": [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
        ]
    }

    def setup(self):
        app.testing = True
        self.client = app.test_client()

    def test_correct_request(self):
        """ Test valid request to post visited links """
        response = self.client.post(f'/visited_links', json=self.asset_post_payload)
        response_body = response.get_json()

        assert response.status_code == 200
        assert 'status' in response_body
        assert response_body['status'] == 'ok'

        registered_domains = list(db.domain_filter(0, now_timestamp() + 600))
        for url in self.asset_post_payload['links']:
            domain_name = url_to_domain(url)
            assert domain_name in registered_domains

    def test_empty_data_request(self):
        """ Test request without POST data - should return 400 status code """
        response = self.client.post(f'/visited_links')
        response_body = response.get_json()

        assert response.status_code == 400
        assert 'message' in response_body

    def test_empty_links_list_request(self):
        """ Test correct request but with empty links list - should return 200 status code """
        response = self.client.post(f'/visited_links', json={'links': []})
        response_body = response.get_json()

        assert response.status_code == 200
        assert 'status' in response_body
        assert response_body['status'] == 'ok'

    def test_wrong_data_request(self):
        """ Test request with unexpected data - should return 400 status code """
        response = self.client.post(f'/visited_links', json={'some': 'wrong payload'})
        response_body = response.get_json()

        assert response.status_code == 400
        assert 'message' in response_body

    def teardown(self):
        """ Remove data from test database """
        db.flush_test_db()


class TestVisitsGet:

    client = None
    asset_domain_name = 'example.com'
    query_time_from = now_timestamp()
    query_time_to = query_time_from + 600

    def setup(self):
        app.testing = True
        self.client = app.test_client()

        db.domain_register(self.query_time_from, self.asset_domain_name)

    def test_correct_request(self):
        """ Test correct request for getting data from the service """
        response = self.client.get(f'/visited_domains?from={self.query_time_from}&to={self.query_time_to}')
        response_body = response.get_json()

        assert response.status_code == 200
        assert 'status' in response_body
        assert 'domains' in response_body
        assert response_body['status'] == 'ok'
        assert self.asset_domain_name in response_body['domains']

    def test_request_without_from_parameter(self):
        """ Test request with wrong parameters - 'from' parameter is not specified """
        response = self.client.get(f'/visited_domains?to={self.query_time_to}')
        response_body = response.get_json()

        assert response.status_code == 400
        assert 'message' in response_body

    def test_request_without_to_parameter(self):
        """ Test request with wrong parameters - 'to' parameter is not specified """
        response = self.client.get(f'/visited_domains?from={self.query_time_to}')
        response_body = response.get_json()

        assert response.status_code == 400
        assert 'message' in response_body

    def teardown(self):
        """ Remove data from test database """
        db.flush_test_db()
