# Goobox Nodes

![Generic badge](https://img.shields.io/badge/Project-Goobox-blue.svg)
![Generic badge](https://img.shields.io/badge/Author-José%20Antonio%20Perdiguero%20López-blue.svg)
![Generic badge](https://img.shields.io/badge/Status-Development-yellow.svg)

* **Project:** Goobox
* **Author:** José Antonio Perdiguero López
* **Status:** Development

## Introduction

_Goobox Nodes_ is a service part of Goobox ecosystem that manages the collection of data and metadata of storage nodes,
keep it updated and provides a reliable way to access it.

## API Description

### Online Documentation
API documentation can be accessed through `/docs/` or `/redoc/` endpoint, and it will show the full documentation that 
reflects the current status of the service, gathering every **resource** and its different **methods** as well as how 
to call the endpoint of these methods, including a descriptive list of **parameters**.

### Schema
The schema of the API can be generated following OpenAPI standard calling the `/schema/` endpoint:

```commandline
curl http://localhost:8000/schema/
```

## Contribute

### Requirements

 * [Python](https://www.python.org/downloads/).
 * [Docker](https://docs.docker.com/install/).
 * [Poetry](https://poetry.eustace.io/docs/#installation).

### Build

Clone repository 

```commandline
git clone https://github.com/goobox/goobox-nodes-api.git
```

Install development dependencies

```commandline
poetry install
```

Build service image

```commandline
poetry run python make build
```

### Run

Run the service stack

```commandline
poetry run python make up
```

And stop it when you finish

```commandline
poetry run python make down
```

### Help
The entry point has a self-describing help that can be queried.

```commandline
poetry run python make run -h
```

Also, each command has its own help.

```commandline
poetry run python make run start -h
```
 ### Code Quality
To check code quality:

```commandline
poetry run python make run lint
```

### Testing
To run tests manually:

```commandline
poetry run python make run test
```

## License

[GNU GPL v3](https://github.com/GooBox/goobox-nodes-api/blob/master/LICENSE)
