from random import choices
from string import ascii_lowercase

from locust import HttpUser, between, task


class CompleteStressTesting(HttpUser):
    wait_time = between(2, 5)

    def randomize_domain(self, length: int = 6):
        """ Generate a domain name with specified length """
        return f"{''.join(choices(ascii_lowercase, k=length))}.com"

    @task(1)
    def status_page(self):
        """ Requesting service status page """
        self.client.get('/')

    @task(1)
    def post_data(self):
        """ posting randomized data to the service (database used testing) """
        asset_post_payload = {
            "links": [
            ]
        }

        for i in range(3):
            asset_post_payload['links'].append(self.randomize_domain())

        self.client.post('/visited_links', json=asset_post_payload)

    @task(2)
    def get_data(self):
        """ getting data from the service (database used testing) """
        self.client.get('/visited_domains?from=0&to=9999999999999999')
