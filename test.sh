curl -X POST\
   -H 'Content-Type: application/json'\
   -H 'Host: 127.0.0.1:8000'\
   -H 'cache-control: no-cache'\
   -d '{ "num": 148 }'\
    http://localhost:8000/inc/
