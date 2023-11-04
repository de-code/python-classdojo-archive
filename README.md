# Python Tapestry Archive

This is inspired by [dojo](https://github.com/espiegel/dojo), written in JavaScript.

Download all the resources from your child's [classdojo](https://classdojo.com) account.

## Requirements

* Python 3.9
* Pip
* Make

## Setup

```bash
make dev-venv
```

That will create a Python virtual environment and install dependencies.

## Configuration

Copy `env.example` to `.env` and fill in the details.

## Run

* Run `make run`

The resources will be downloaded to the `output` directory.
