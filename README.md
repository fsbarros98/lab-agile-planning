# lab-agile-planning
This repository contains the lab for agile planning

## Counter service

Run the service with Python 3:

```sh
python3 counter_service.py
```

The counter starts at 0 and is stored in memory, so it resets when the service
restarts. The service listens on `127.0.0.1:8000`.

```sh
curl -X POST http://127.0.0.1:8000/counter/increment
curl http://127.0.0.1:8000/counter
```

Both operations return JSON such as `{"counter": 1}`.

Run the tests with `python3 -m unittest`.
