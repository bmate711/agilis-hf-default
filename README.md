# Agilis HF
## Run the code

First create and activate your virtualenv - with the `venv` package on OSX or Linux, this will be:

```bash
python3 -m venv venv
source venv/bin/activate
```

With your virtualenv active, install the project locally:

```bash
pip install -e .
```

```bash
docker run -d  --name agilisHF  -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=mongoadmin -e MONGO_INITDB_ROOT_PASSWORD=secret mongo
```


```bash
export MONGO_URI="mongodb://mongoadmin:secret@localhost:27017/hf?authSource=admin"
```

And now you should be able to run the service like this:

```bash
FLASK_APP=agilisHF flask run
```

## Developing

Run the following to install the project (and dev dependencies) into your active virtualenv:

```bash
pip install -e .[dev]
```

You can run the tests with:

```bash
pytest
```
