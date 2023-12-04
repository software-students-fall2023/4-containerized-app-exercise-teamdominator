![Lint and formatting](https://github.com/software-students-fall2023/4-containerized-app-exercise-teamdominator/actions/workflows/lint.yml/badge.svg)
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

Reminder: We used the file "yolov3.weights" in our process of machine learning. However, the quota of our class repository is not enough. So here's the link for downloading the file:

https://drive.google.com/file/d/128QCeb4Ea-0TksH4Obpw6KpQrv8SdnU0/view?usp=sharing

After downloading the file, the user should put this file into the folder: "machine-learning-client/ML/yolov".

### Web App Client ![Web App CI/CD](https://github.com/software-students-fall2023/4-containerized-app-exercise-teamdominator/actions/workflows/webappCI-CD.yaml/badge.svg)

Open a web browser and go to `http://localhost:5001` to access the web application.

## Process of our application

When you visit the `http://localhost:5001`  successfully, you will see our web dashboard. The left part of the dashboard is a live camera. When you click on the "Capture Photo" button, the camera will capture the photo of yourself, which will be shown on the middle part of the dashboard. You can also choose to upload an image file by clicking the "Choose File" button in the middle. Then click on the "Process Image" button on the right side to see the visualized result!

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
