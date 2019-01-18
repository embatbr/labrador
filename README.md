# Labrador


## Packages


### labrador

Library containing all the logic.


### server

TOFIX


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


## Running

The library receives the credentials encrypted. To decrypt them, a private key is needed. The system will load the environment variable **PRIVATE_KEY_PEM** (or break in case it is no defined).

### Testing

The following execution retrieves data from a BigQuery public source and stores in a S3 bucket:

```bash
$ PRIVATE_KEY_PEM=<YOUR_PRIVATE_KEY> python test/test_labrador.py <CREDENTIALS_FILEPATH> <BUCKET_NAME>
```
