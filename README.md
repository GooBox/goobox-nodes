# goobox-nodes-api
![Generic badge](https://img.shields.io/badge/Status-Development-yellow.svg)

API for interacting with nodes.

## Getting started
To run _Goobox Nodes API_ you need previously to install the requirements and you can either use public docker image or build it from sources.

### Requirements
1. *Docker:* Install it following [official docs](https://docs.docker.com/engine/installation/).

### Use public image
You can use public docker image to run the service. E.g. run Storj nodes scraper, collect them and put together into a csv format file:

    docker run -p 80:80 goobox/goobox-nodes-api:latest start

### Build from sources
To build _Goobox Nodes API_ from sources you need to clone this project and build the image.

    git clone https://github.com/goobox/goobox-nodes-api.git & cd goobox-nodes-api
    python3.6 make build

Once build is completed you can run the scraper using ``start`` command from the entry point.

    python3.6 make run start

### Help
The entry point has a self-describing help that can be queried.

    python3.6 make run -h

Also, each command has its own help.

    python3.6 make run start -h
 
## License

[GNU GPL v3](https://github.com/GooBox/goobox-nodes-scraper/blob/master/LICENSE)
