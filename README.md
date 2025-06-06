SRE Monitor
A simple Python-based monitoring service that checks the availability and response time of two URLs and exposes Prometheus-compatible metrics via an HTTP server.


# 1. Prerequisites.

- openSUSE SLES 15 SP6
- Docker
- Minikube (with Docker driver)
- Helm
- Git
- curl, wget, tree
  

### Install Docker:
sudo zypper install docker
sudo systemctl enable --now docker

## Create work user and give correct permissions:
useradd -m -G docker -s /bin/bash ivan
sudo usermod -aG docker ivan

## Install kubectl:
curl -LO "https://dl.k8s.io/release/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

## Install Helm:
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

## Install Minikube:
wget https://storage.googleapis.com/minikube/releases/latest/minikube-latest.x86_64.rpm
rpm -ivh --nosignature minikube-latest.x86_64.rpm

## Switch to work user:
su - ivan

# 2. Clone the Repository.

git clone https://github.com/vank1chaa/sre-monitor.git
cd sre-monitor

# 3. Start Minikube and Use Docker Env:
minikube start --driver=docker
eval $(minikube docker-env)

# 4. Build the Docker Image (inside Minikube's Docker):
docker build -t sre-monitor:latest .

# 5. Deploy to Kubernetes via Helm:
helm upgrade --install sre-monitor ./charts/sre-monitor

# 6. Port Forward the Service:
kubectl port-forward svc/sre-monitor 8000:8000

# 7. Check from VM or browser:
curl http://localhost:8000
