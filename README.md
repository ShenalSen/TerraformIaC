# Flask List Application with Terraform Infrastructure

[![Terraform](https://img.shields.io/badge/Terraform-v1.0%2B-623ce4?logo=terraform)](https://terraform.io)
[![Docker](https://img.shields.io/badge/Docker-required-0db7ed?logo=docker)](https://docker.com)
[![Python](https://img.shields.io/badge/Python-3.13-3776ab?logo=python)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479a1?logo=mysql)](https://mysql.com)

A complete Infrastructure as Code (IaC) solution using Terraform to deploy a containerized Flask web application with MySQL database. This project demonstrates modern DevOps practices by automating the entire application stack deployment using declarative infrastructure management.

## 🏗️ Architecture

This project deploys a multi-container application stack consisting of:

```
┌─────────────────────────────────────────────────────────────┐
│                        Docker Host                          │
│                                                             │
│  ┌─────────────────┐           ┌──────────────────────────┐ │
│  │                 │           │                          │ │
│  │   Flask App     │◄─────────►│       MySQL 8.0          │ │
│  │   (Port 5000)   │           │   (Internal Network)     │ │
│  │                 │           │                          │ │
│  └─────────────────┘           └──────────────────────────┘ │
│           │                                                 │
│           │                                                 │
│  ┌─────────────────┐                                       │
│  │   app-network   │                                       │
│  │ (Docker Bridge) │                                       │
│  └─────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
          │
          │ Port 5000
          ▼
   ┌─────────────┐
   │   Localhost │
   │  Port 5000  │
   └─────────────┘
```

### Components

- **Flask Application**: A Python web application providing a simple list/todo interface
- **MySQL Database**: Persistent data storage with health checks
- **Docker Network**: Isolated network for container communication
- **Terraform**: Infrastructure as Code management

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Terraform** (v1.0 or later) - [Download here](https://terraform.io/downloads)
- **Docker** or **Podman** - [Docker Installation](https://docs.docker.com/get-docker/) | [Podman Installation](https://podman.io/getting-started/installation)
- **Git** - [Download here](https://git-scm.com/downloads)

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 2GB RAM available for containers
- **Disk Space**: At least 1GB free space
- **Network**: Internet connection for downloading images

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/ShenalSen/TerraformIaC.git
cd TerraformIaC
```

### 2. Configure Docker Provider (If using Podman)

If you're using Docker Desktop, the default configuration should work. For Podman users, update the provider configuration in `main.tf`:

```hcl
provider "docker" {
  host = "npipe:////./pipe/podman-machine-default"  # For Podman on Windows
  # host = "unix:///var/run/docker.sock"            # For Docker on Linux/macOS
}
```

### 3. Initialize Terraform

```bash
terraform init
```

### 4. Plan the Deployment

```bash
terraform plan
```

### 5. Deploy the Infrastructure

```bash
terraform apply
```

Type `yes` when prompted to confirm the deployment.

### 6. Access the Application

Once deployment is complete, the application will be available at:
- **Web Interface**: http://localhost:5000
- **Add Items**: http://localhost:5000/add
- **View Items**: http://localhost:5000/show

## 📖 Usage

### Application Features

The Flask application provides a simple list management interface:

1. **Home Page** (`/`): Welcome message
2. **Add Items** (`/add`): Form to add new items to your list
3. **View Items** (`/show`): Display all items with delete functionality
4. **Delete Items** (`/delete/<id>`): Remove specific items

### Managing the Infrastructure

```bash
# View current infrastructure state
terraform show

# View outputs (including app URL)
terraform output

# Update infrastructure after code changes
terraform plan
terraform apply

# Destroy all resources
terraform destroy
```

### Container Management

```bash
# View running containers
docker ps

# View application logs
docker logs flask-app

# View database logs
docker logs mysql-db

# Access the Flask container shell
docker exec -it flask-app /bin/bash

# Access the MySQL container
docker exec -it mysql-db mysql -u root -p
```

## ⚙️ Configuration

### Environment Variables

The application uses the following environment variables (automatically configured by Terraform):

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `DB_HOST` | `mysql-db` | MySQL container hostname |
| `DB_USER` | `root` | Database username |
| `DB_PASSWORD` | `password` | Database password |
| `DB_DATABASE` | `webapp` | Database name |

### Customization Options

You can customize the deployment by modifying `main.tf`:

#### Change MySQL Configuration
```hcl
resource "docker_container" "mysql_db" {
  env = [
    "MYSQL_ROOT_PASSWORD=your_secure_password",
    "MYSQL_DATABASE=your_database_name"
  ]
}
```

#### Change Application Port
```hcl
resource "docker_container" "flask_app" {
  ports {
    internal = 5000
    external = 8080  # Change to desired port
  }
}
```

#### Persistent Data Storage
Add volumes for data persistence:
```hcl
resource "docker_container" "mysql_db" {
  volumes {
    host_path      = "/path/to/mysql/data"
    container_path = "/var/lib/mysql"
  }
}
```

## 🛠️ Development

### Project Structure

```
TerraformIaC/
├── main.tf                 # Main Terraform configuration
├── README.md               # This file
├── FlaskApp/
│   ├── app.py              # Flask application main file
│   ├── Dockerfile          # Container build instructions
│   ├── requirements.txt    # Python dependencies
│   ├── config/
│   │   └── db_config.py    # Database configuration
│   └── templates/
│       ├── add.html        # Add item template
│       └── show.html       # Show items template
└── .terraform/             # Terraform state and providers
```

### Adding New Features

1. **Modify the Flask application** in `FlaskApp/app.py`
2. **Update templates** in `FlaskApp/templates/`
3. **Add dependencies** to `FlaskApp/requirements.txt`
4. **Rebuild and redeploy**:
   ```bash
   terraform apply
   ```

### Local Development

To develop the Flask application locally without Terraform:

```bash
cd FlaskApp
pip install -r requirements.txt
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=password
export DB_DATABASE=webapp
python app.py
```

## 🔧 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
Error: port 5000 is already in use
```
**Solution**: Change the external port in `main.tf` or stop the conflicting service.

#### Docker Connection Failed
```bash
Error: Cannot connect to Docker daemon
```
**Solutions**:
- Ensure Docker/Podman is running
- Verify the provider host configuration
- Check Docker socket permissions (Linux/macOS)

#### MySQL Connection Failed
```bash
Error: Can't connect to MySQL server
```
**Solutions**:
- Wait for MySQL health check to pass
- Check container logs: `docker logs mysql-db`
- Verify network connectivity between containers

#### Terraform State Issues
```bash
Error: state lock
```
**Solution**: 
```bash
terraform force-unlock <lock-id>
```

### Health Checks

The MySQL container includes health checks. Monitor status with:
```bash
docker inspect mysql-db | grep -A 10 "Health"
```

### Logs and Debugging

```bash
# View all container logs
docker logs flask-app --follow
docker logs mysql-db --follow

# Terraform debug mode
export TF_LOG=DEBUG
terraform apply
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test your changes**: `terraform plan && terraform apply`
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Code Standards

- Follow [Terraform best practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)
- Use meaningful resource names and comments
- Test infrastructure changes locally before submitting
- Update documentation for any configuration changes

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Terraform Docker Provider](https://registry.terraform.io/providers/kreuzwerker/docker/latest) by kreuzwerker
- [Flask Framework](https://flask.palletsprojects.com/) for the web application
- [MySQL](https://www.mysql.com/) for database services

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [Issues](https://github.com/ShenalSen/TerraformIaC/issues)
3. Create a new [Issue](https://github.com/ShenalSen/TerraformIaC/issues/new) with:
   - Your operating system and versions
   - Terraform and Docker versions
   - Complete error messages
   - Steps to reproduce the issue

---

Made with ❤️ using Terraform and Docker