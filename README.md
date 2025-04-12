# 🚢 Dockinitor

**Dockinitor** is a lightweight, container-based server monitoring system that automatically generates alerts and tickets when system thresholds are exceeded (CPU, RAM, disk, etc.).

> _“He watches your containers. Relentlessly.”_

---

## 🧠 Overview

Dockinitor is designed to simulate a multi-server infrastructure using Docker containers. Each container runs a monitoring agent that checks for resource usage and automatically creates a ticket when a threshold is passed.

### 🎯 Core Features
- 📈 Resource monitoring: CPU, RAM, disk usage  
- 🧾 Automatic ticket generation when thresholds are exceeded  
- ⚙️ Simple setup using Docker  
- 🛠️ Maintenance mode to disable alerts temporarily (coming soon)  
- 🌐 Web dashboard (planned)  

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/dockinitor.git && cd dockinitor
```

### 2. Build and run the containers
```bash
docker-compose up --build
```

---

## 📋 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🧑‍💻 Author

Made with ☕, 🐳, and a bit of system overload by **[Your Name]**
