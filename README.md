# VCounter

There is microservice which created for counting website visits statistic.

It receives list of web URLs and returns uniq domain names with timestamp time-bounding.

#### Write stats

Send POST request to endpoint ```/visited_links```

Payload example:

```json
{
  "links": [
    "https://ya.ru",
    "https://ya.ru?q=123",
    "http://www.yandex.ru"
  ]
}
```

#### Get stats

Send GET request to endpoint ```/visited_domains?from=<integer timestamp>&to=<integer timestamp>```

Response example:

```json
{
  "domains":[
    "ya.ru",
    "yandex.ru"
  ]
}
```

### DEV

Requirements: 
1. Local Redis. You can run it from docker image using:
   * ```docker run -p 127.0.0.1:6379:6379 --name vcounter-redis -d redis```

#### Installation

1. install poetry
2. run ```poetry install```
3. copy YML config and configure it: ```cp conf/config.sample.yaml conf/config.local.yaml``` 
4. copy environment config and configure it: ```cp conf/.env.sample .env```

#### Debug

For debug run ```bin/run_server.py```

### Local Kubernetes cluster

Use instruction on page: [local k8s](/docs/deploy/deployment.md)

### Testing

Use instruction on page: [tests](/docs/testing/readme.md)


### About

1. Python 3
2. Flask [(lightweight WSGI web application framework)](https://flask.palletsprojects.com/)
3. Pytest [(test framework)](https://docs.pytest.org/)
4. Mypy [(static type checker)](https://mypy.readthedocs.io/en/stable/)
5. Locust [(an open source load testing tool)](https://locust.io/)
6. Redis [(data structure storage)](https://redis.io/)
7. Docker [(containerisation system)](https://www.docker.com)
8. Kubernetes [(container orchestration system)](https://kubernetes.io/)
9. Minikube [(your local k8s cluster)](https://minikube.sigs.k8s.io/docs/)
