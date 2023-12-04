# Containerized App Exercise

See [instructions](./instructions.md) for details. This project is a containerized web application that uses YOLO (You Only Look Once) for object detection in images, with MongoDB as the backend for storage. The application consists of two main components: a web app client built with Flask, and a machine learning client for image processing.

## Prerequisites

- Docker
- Python 3.x
- Access to a terminal or command line interface

## Setting Up MongoDB

This project uses MongoDB as its database, running within a Docker container for ease of setup and portability.

### Install Docker

Ensure Docker and Docker Compose are installed on your machine. Instructions can be found on the [Docker website](https://www.docker.com/products/docker-desktop).

### Clone the Repository

Clone this repository to your local machine. This repository contains the Docker Compose file and necessary code for the web app client and the machine learning client.

### Start the Services Using Docker Compose

Navigate to the directory containing the `docker-compose.yaml` file and run the following command to start all services:

```bash
docker-compose up -d
```

This command will start the MongoDB database, the web app client, and the machine learning client in their respective containers.

### Machine Learning Client ![Machine Learning CI/CD](https://github.com/software-students-fall2023/4-containerized-app-exercise-teamdominator/actions/workflows/machinelearningCI-CD.yaml/badge.svg)


### Web App Client ![Web App CI/CD](https://github.com/software-students-fall2023/4-containerized-app-exercise-teamdominator/actions/workflows/webappCI-CD.yaml/badge.svg)

Open a web browser and go to `http://localhost:5001` to access the web application.

## Stopping the Services

To stop all services, run the following command in the directory containing the `docker-compose.yaml` file:

```bash
docker-compose down
```

## Troubleshooting

If you encounter any issues, check the following:

- Ensure that all Docker containers are up and running. Use `docker ps` to check the status.
- Check the Docker container logs for any error messages.
- Ensure that the ports specified in the `docker-compose.yaml` are not used by other services and are correctly mapped.
