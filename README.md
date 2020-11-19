# PyScripts
This repository contains all my single python script

### Parsing

- `CTFTime_to_csv.py`: this script simply convert the the ctf time events to csv file using the API

### Network

- `client-server.py`: this script contains two simple classes, Client and Server, which are builded to communicate between them. An example is shown below:

**SERVER**
```python 

if __name__ == "__main__":

    # Server Example
    server = Server()
    server.run()

    while True:
        server.listening()
        server.retrieve_data()
        data = {}
        data['msg'] = 'test_back'
        server.send_data(data)
```


**CLIENT**
```python 

if __name__ == "__main__":

    # Client Example
    client = Client()

    while True:
        data = 'test'
        client.run(data)
```