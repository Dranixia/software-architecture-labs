# Lab 1: Micro-service basics

## Requirments:

```
pip install -r requirements.txt
```

## Usage:
To run the services (separately if needed):

```
python3 facade-service/facade_service.py
python3 logging-service/logging_service.py
python3 messages-service/messages_service.py
```

To send POST/GET requests using curl (or any other app of your preference):

```
curl -X POST [url] -d [message]:

curl -X POST http://localhost:8080/facade -d "Blablabla"
```
```
curl -X GET [url]

curl -X GET http://localhost:8080/facade
```

## Results:

See results in PDF file
