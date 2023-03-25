# Application Reviewer

This is a sample application that aims to use chatgpt to review job applications

## Getting Started

To get started, you'll need to have Docker and Poetry installed on your local machine. Here's how to install them:

### Installing Docker

Docker is a platform for building, shipping, and running applications in containers. You can download and install Docker by following the instructions on the official website: https://www.docker.com/products/docker-desktop

### Installing Poetry

Poetry is a dependency manager and build tool for Python. You can install Poetry by following the instructions on the official website: https://python-poetry.org/docs/#installation

## Running the Application

To run the application, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the root directory of the project.
3. Run `poetry install` to install the project dependencies.
4. Run `docker build -t my-app -f docker-containers/Dockerfile .` to build the Docker container.
5. Run `docker run -p 8000:8000 my-app` to start the container and expose the application on port 8000.

You should now be able to access the application by opening a web browser and navigating to `http://localhost:8000`. If you have your fastapi server up and running 
