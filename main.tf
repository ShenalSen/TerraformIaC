terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {
  host = "npipe:////./pipe/podman-machine-default"
}

# Setup an Isolated Docker network
resource "docker_network" "private_network" {
  name = "app-network"
}

# Create the MySQL Docker container
resource "docker_container" "mysql_db" {
  name  = "mysql-db"
  image = "mysql:8.0"

  networks_advanced {
    name = docker_network.private_network.name
  }

  env = [
    "MYSQL_ROOT_PASSWORD=password",
    "MYSQL_DATABASE=webapp"
  ]

  # Add a health check to ensure MySQL is ready to accept connections
  healthcheck {
    test     = ["CMD", "mysqladmin", "ping", "-h", "localhost"]
    timeout  = "20s"
    retries  = 10
    interval = "10s"
  }
}

# Create a Docker Image for the Python Flask Application
resource "docker_image" "flask_app_image" {
  name = "flask-list-app:latest"
  build {
    context = "./FlaskApp" # Path to the folder with the Dockerfile
  }
}

# Create a Docker container for the Python Flask App
resource "docker_container" "flask_app" {
  name  = "flask-app"
  image = docker_image.flask_app_image.name
  
  restart = "on-failure"

  networks_advanced {
    name = docker_network.private_network.name
  }

  # Port forward from the container's port 5000 to the host's port 5000
  ports {
    internal = 5000
    external = 5000
  }

  # Environment variables for connecting to MySQL
  env = [
    "DB_HOST=mysql-db",
    "DB_USER=root",
    "DB_PASSWORD=password",
    "DB_DATABASE=webapp"
  ]


  # Ensure MySQL container is healthy before starting Flask app
  depends_on = [
    docker_container.mysql_db
  ]
}

# Output the URL of the running Flask application
output "app_url" {
  value       = "http://localhost:${docker_container.flask_app.ports[0].external}"
  description = "The URL of the running Flask application"
}