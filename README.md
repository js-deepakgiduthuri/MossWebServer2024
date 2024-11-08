# Redox MossWebServer

Redox MossWebServer is a web-based management tool for handling modem and network configurations, enabling easy access to and configuration of SIM-APN pairs, LAN settings, and system state information.

---

## Features

1. **Add and Remove SIM-APN Pairs**  
   Dynamically manage SIM-APN pairs in a dictionary, allowing users to add and remove pairs as needed.

2. **Display Ethernet Configuration**  
   In the **LAN Section**, the application reads and displays the Ethernet configuration, providing a clear overview of LAN settings.

3. **Display System State Information**  
   In the **State Section**, the application reads from `/etc/config/config.json` and displays system state details.

---

## Getting Started

Follow these instructions to set up and run Redox MossWebServer on your system.

### Docker Image Names

The Docker images required for the web server are specified below:

- **Web Application Image**: `web_application12`
- **Shell Script Modifier Image**: `modify_shell_script6`

For the most recent image versions and configurations, refer to the `docker-compose.yml` file included in this repository.

### Prerequisites

- **Docker**: Ensure Docker is installed on your system.
- **Docker Compose**: Required to manage multiple containers with the provided `docker-compose.yml` file.

