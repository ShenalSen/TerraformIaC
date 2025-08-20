# TerraformIaC - Flask App with MySQL Database

A Terraform Infrastructure as Code (IaC) project that deploys a complete web application stack using Docker containers. This project demonstrates how to use Terraform to orchestrate a multi-container application consisting of a Python Flask web application and a MySQL database.

## 🏗️ Architecture

This project creates the following infrastructure:

- **Docker Network**: An isolated network (`app-network`) for secure container communication
- **MySQL Database**: A MySQL 8.0 container with health checks and persistent data
- **Flask Web Application**: A Python Flask app containerized and connected to the database
- **Port Mapping**: Flask app accessible on `http://localhost:5000`

```
┌─────────────────────────────────────────┐
│              Docker Network             │
│              (app-network)              │
│                                         │
│  ┌─────────────┐    ┌─────────────────┐ │
│  │   MySQL     │    │   Flask App     │ │
│  │ Container   │◄───┤   Container     │ │
│  │ (mysql-db)  │    │ (flask-app)     │ │
│  │ Port: 3306  │    │ Port: 5000      │ │
│  └─────────────┘    └─────────────────┘ │
│                            │            │
└────────────────────────────┼────────────┘
                             │
                    ┌────────▼────────┐
                    │   Host System   │
                    │ localhost:5000  │
                    └─────────────────┘
```

## 📋 Prerequisites

Before running this project, ensure you have the following installed:

- **Terraform** (>= 1.0)
  ```bash
  # Install Terraform (example for Ubuntu/Debian)
  wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
  echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
  sudo apt update && sudo apt install terraform
  ```

- **Docker** or **Podman**
  ```bash
  # For Docker
  sudo apt install docker.io
  sudo systemctl start docker
  sudo usermod -aG docker $USER
  
  # For Podman (alternative)
  sudo apt install podman
  ```

- **Git** (for cloning the repository)

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/ShenalSen/TerraformIaC.git
   cd TerraformIaC
   ```

2. **Initialize Terraform**
   ```bash
   terraform init
   ```

3. **Review the execution plan**
   ```bash
   terraform plan
   ```

4. **Deploy the infrastructure**
   ```bash
   terraform apply
   ```
   
   Type `yes` when prompted to confirm the deployment.

5. **Access the application**
   
   Once deployed, you can access the Flask application at:
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
TerraformIaC/
├── main.tf                    # Main Terraform configuration
├── terraform.tfstate          # Terraform state file (auto-generated)
├── terraform.tfstate.backup   # State backup (auto-generated)
├── .terraform.lock.hcl        # Provider lock file
├── .terraform/                # Terraform working directory
└── FlaskApp/                  # Flask application source code
    ├── app.py                 # Main Flask application
    ├── Dockerfile             # Container definition for Flask app
    ├── requirements.txt       # Python dependencies
    ├── config/
    │   └── db_config.py      # Database configuration
    └── templates/
        ├── add.html          # Add item template
        └── show.html         # Show items template
```

## 🛠️ Components

### Terraform Configuration (`main.tf`)

- **Provider**: Uses the `kreuzwerker/docker` provider v3.0.1
- **Network**: Creates an isolated Docker network for container communication
- **MySQL Container**: 
  - Image: `mysql:8.0`
  - Database: `webapp`
  - Health checks with mysqladmin ping
- **Flask Container**: 
  - Built from `./FlaskApp/Dockerfile`
  - Exposes port 5000
  - Environment variables for database connection

### Flask Application (`FlaskApp/`)

A simple CRUD application for managing a list of items with the following features:

- **Routes**:
  - `/` - Welcome page
  - `/add` - Add new items to the list
  - `/show` - Display all items
  - `/delete/<id>` - Delete specific items

- **Database**: Uses MySQL with auto-created `items` table
- **Configuration**: Environment-based database connection

## 🔧 Usage

### Adding Items
1. Navigate to `http://localhost:5000/add`
2. Enter your item content
3. Click submit to add to the database

### Viewing Items
1. Navigate to `http://localhost:5000/show`
2. View all items in your list
3. Delete items using the delete links

### Database Connection
The Flask app automatically connects to the MySQL database using these environment variables:
- `DB_HOST=mysql-db`
- `DB_USER=root` 
- `DB_PASSWORD=password`
- `DB_DATABASE=webapp`

## 🧹 Cleanup

To destroy the infrastructure and remove all containers:

```bash
terraform destroy
```

Type `yes` when prompted to confirm the destruction.

## 🔍 Troubleshooting

### Common Issues

1. **Port 5000 already in use**
   ```bash
   # Check what's using port 5000
   sudo lsof -i :5000
   # Kill the process or change the port in main.tf
   ```

2. **Docker daemon not running**
   ```bash
   sudo systemctl start docker
   # Or for Podman
   sudo systemctl start podman
   ```

3. **Permission denied errors**
   ```bash
   # Add user to docker group
   sudo usermod -aG docker $USER
   # Log out and back in
   ```

4. **MySQL container not healthy**
   ```bash
   # Check container logs
   docker logs mysql-db
   # The Flask app waits for MySQL to be healthy before starting
   ```

### Debugging Commands

```bash
# View Terraform state
terraform show

# Check container status
docker ps

# View container logs
docker logs flask-app
docker logs mysql-db

# Inspect the network
docker network inspect app-network
```

## 🔄 Customization

### Changing Database Credentials
Modify the environment variables in `main.tf`:

```hcl
env = [
  "MYSQL_ROOT_PASSWORD=your_password",
  "MYSQL_DATABASE=your_database"
]
```

### Changing Application Port
Update the port mapping in `main.tf`:

```hcl
ports {
  internal = 5000
  external = 8080  # Change this to your desired port
}
```

### Adding Persistent Storage
Add a volume mount to the MySQL container:

```hcl
volumes {
  host_path      = "/path/to/mysql/data"
  container_path = "/var/lib/mysql"
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#🔍-troubleshooting) section
2. Review the [Issues](https://github.com/ShenalSen/TerraformIaC/issues) on GitHub
3. Create a new issue with detailed information about your problem

---

**Note**: This project is configured for Podman with the pipe path `npipe:////./pipe/podman-machine-default`. If you're using Docker, you may need to update the provider configuration in `main.tf`.