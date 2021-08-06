### Testing

Just run pytest in poetry environment:

1. ```poetry init```
2. ```pytest```

Or run ```bin/run_tests.sh``` (make it executable first)

### Stress testing

Run locust script and watch testing dashboard:

1. ```poetry init```
2. ```pytest```
3. ```locust -f tests/stress.py```
4. ```go to  http://0.0.0.0:8089```
5. Configure test: set number of users, user spawn rate and service main url

Or run ```bin/run_stress_test.sh``` (make it executable first)
