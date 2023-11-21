# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.

## Prerequisites

- Docker
- Python

## Setting Up MongoDB

This project uses MongoDB as its database, running within a Docker container for ease of setup and portability.

### Install Docker

Ensure that Docker is installed on your machine. Instructions can be found on the [Docker website](https://www.docker.com/products/docker-desktop).

### Run MongoDB Container

Open a terminal and run the following command:

```bash
bashCopy code
docker run --name mongodb -d -p 27017:27017 mongo
```

This command will download and run the MongoDB image in a container.

### Verify Container is Running

Check if the MongoDB container is running using:

```bash
docker ps
```
