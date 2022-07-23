Face Encoding API
=====================
Process a person's face and extract a vector of dimension 128.

System requirements
-------------------
- Python >= 3.6

Installation
------------
```bash
$ sudo mkdir /var/log/fksolutions  # creates fksolutions logging folder
$ sudo chown $USER:$USER /var/log/fksolutions  # give fksolutions logging folder group permissions
$ pip install -e .
```

Usage
-----
```bash
$ face-encoding  # run API
```
Read REST API documentation through ``/docs`` endpoint for API usage.