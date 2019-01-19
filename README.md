# Labrador

Labrador is a project aimed to do one thing, and one thing only: *retrieve data from a source*.

The project is composed of two packages:

- labrador - a library encapsulating the *retrieve-sink* logic;
- server - a REST server that uses the library.


## Build and install

Before installing, make sure you are in the correct environment and go to the project root directory (the one in which this README file is contained). The ideal is to create a virtual environment:

```bash
$ mkvirtualenv --python=$(which python3) <YOUR_ENVNAME>
```

After that, activate your environment and install the package.

```bash
$ workon <YOUR_ENVNAME>
$ python setup.py install
```


## Using

### labrador

Just import the modules, classes, functions and etc., as any normal Python package. Ex:

```bash
$ workon <YOUR_ENVNAME>
$ python
>>> import labrador
```

### server

```bash
$ workon <YOUR_ENVNAME>
$ export PRIVATE_KEY_PEM=<THE_PEM_PRIVATE_KEY_TO_DECRYPT_THE_CREDENTIALS>
$ python server/start.sh
```


## Testing

Both tests retrieve data from a BigQuery public dataset, JSONify it and saves in S3.

*For both **labrador** and **server** tests, notice that the credentials sent are encrypted*

### labrador

```bash
$ workon <YOUR_ENVNAME>
$ export PRIVATE_KEY_PEM=<THE_PEM_PRIVATE_KEY_TO_DECRYPT_THE_CREDENTIALS>
$ python test/test_labrador.py <CREDENTIALS_DIRPATH> <BUCKET_NAME>
```

### server

Turn the server up, as shown in the [using section](#server) and do:

```bash
$ workon <YOUR_ENVNAME>
$ python test/test_server.py <CREDENTIALS_DIRPATH> <BUCKET_NAME> <TEST_ID>
```
