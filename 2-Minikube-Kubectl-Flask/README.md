# Exercise 2 – Deploy a Flask App on Minikube

## Objective

Deploy a Python Flask application on a local Kubernetes cluster using Minikube, Docker, `kubectl`, and Kubernetes YAML.

The exercise demonstrates how to:

- Create a Flask application.
- Containerize the Flask application using Docker.
- Build and load the Docker image into Minikube.
- Create a Kubernetes Deployment using YAML.
- Run the Flask application inside a Kubernetes Pod.
- Verify the Deployment and Pod status.
- Inspect the Deployment configuration.
- View application logs.
- Expose the Flask application using a Kubernetes NodePort Service.
- Access the Flask application through a browser.

---

## Environment

- OS: Windows 11 Home Single Language 26H2
- Minikube: v1.39.0
- Kubernetes: v1.37.0
- Container Runtime: Docker
- Docker Version: 29.2.1
- Kubernetes Driver: Docker
- Application: Python Flask
- Application Port: 15000
- Service Type: NodePort

---

## Project Structure

```text
02-Flask-Minikube/
│
├── README.md
├── app.py
├── Dockerfile
├── flask-deployment.yaml
├── .gitignore
│
└── screenshots/
    ├── 01-minikube-start-status.png
    ├── 02-kubernetes-deployment-service.png
    └── 03-flask-browser.png
```

---

# 1. Start Minikube

Minikube was used to create a local single-node Kubernetes cluster using Docker as the container driver.

### Command

```powershell
minikube start --driver=docker
```

Minikube successfully started the Kubernetes cluster and configured `kubectl` to use the Minikube cluster.

The cluster status was then checked using:

```powershell
minikube status
```

The Minikube host was successfully running.

### Screenshot

![Minikube Start and Status](2-Minikube-Kubectl-Flask\screenshots\01-minikube-start-status.png)

---

# 2. Create the Flask Application

A simple Flask application was created in `app.py`.

### `app.py`

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask on Kubernetes!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000)
```

The application listens on:

```text
0.0.0.0:15000
```

Using `0.0.0.0` allows the Flask application to accept connections from outside the container.

---

# 3. Create the Dockerfile

A Dockerfile was created to containerize the Flask application.

### `Dockerfile`

```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install flask

CMD ["python", "app.py"]
```

The Dockerfile performs the following steps:

1. Uses a Python 3.8 slim image.
2. Creates `/app` as the working directory.
3. Copies the Flask application into the container.
4. Installs Flask.
5. Starts the Flask application using `app.py`.

---

# 4. Build the Docker Image

The Flask application was built into a Docker image named:

```text
flask-app:latest
```

### Command

```powershell
docker build -t flask-app .
```

The image was then made available to the Minikube environment using:

```powershell
minikube image load flask-app:latest
```

The image was verified inside Minikube using:

```powershell
minikube image ls | Select-String flask-app
```

The output confirmed that the `flask-app` image was available:

```text
docker.io/library/flask-app:latest
```

---

# 5. Create the Kubernetes Deployment YAML

A Kubernetes Deployment configuration was created in:

```text
flask-deployment.yaml
```

The Deployment runs one replica of the Flask application.

### Deployment configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
        - name: flask-app
          image: flask-app:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 15000

---
apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
spec:
  selector:
    app: flask-app
  ports:
    - port: 15000
      targetPort: 15000
  type: NodePort
```

### Why `imagePullPolicy: Never`?

The Docker image was built locally and loaded into Minikube.

Therefore, Kubernetes was configured not to attempt to download the image from an external registry.

```yaml
imagePullPolicy: Never
```

This makes Kubernetes use the locally available:

```text
flask-app:latest
```

---

# 6. Deploy the Application

The Kubernetes YAML file was applied using `kubectl`.

### Command

```powershell
kubectl apply -f flask-deployment.yaml
```

The Deployment creates a Kubernetes Pod that runs the Flask container.

---

# 7. Check Deployment Status

The Deployment was verified using:

```powershell
kubectl get deployments
```

The Deployment successfully reached the following state:

```text
NAME        READY   UP-TO-DATE   AVAILABLE
flask-app   1/1     1            1
```

The `1/1` status indicates that the required replica is running and available.

---

# 8. Verify the Flask Pod

The Pods created by the Deployment were checked using:

```powershell
kubectl get pods -l app=flask-app
```

The Flask Pod successfully reached the `Running` state.

The Pod used in this exercise was:

```text
flask-app-59f7cdccb4-cps2v
```

The Pod showed:

```text
READY   STATUS
1/1     Running
```

This confirms that the Flask container was successfully created and is running inside Kubernetes.

---

# 9. Check Kubernetes Services

The available Kubernetes Services were checked using:

```powershell
kubectl get services
```

The Flask application was exposed using:

```text
flask-app-service
```

The Service used the `NodePort` type and mapped:

```text
15000:32042/TCP
```

The mapping is:

```text
Service Port 15000
       ↓
Target Port 15000
       ↓
Flask Container Port 15000
```

The existing `hello-k8s` NodePort Service from Exercise 1 was also present in the cluster.

---

# 10. Access the Flask Application

The Flask Service was accessed using Minikube.

### Command

```powershell
minikube service flask-app-service --url
```

Minikube generated the following local URL:

```text
http://127.0.0.1:52858
```

Because the Docker driver was being used on Windows, the terminal running the Minikube service command was kept open while accessing the application.

---

# 11. Flask Application in Browser

The generated Minikube URL was opened in the browser:

```text
http://127.0.0.1:52858
```

The following response was successfully displayed:

```text
Hello from Flask on Kubernetes!
```

This confirms that the request successfully travelled through the Kubernetes Service to the Flask application running inside the Pod.

### Screenshot

![Flask Application](2-Minikube-Kubectl-Flask\screenshots\03-flask-browser.png)

---

# 12. Kubernetes Deployment and Service Verification

The following commands were used to verify the complete deployment:

```powershell
minikube image ls | Select-String flask-app
```

```powershell
kubectl get deployments
```

```powershell
kubectl get pods
```

```powershell
kubectl get services
```

```powershell
minikube service flask-app-service --url
```

The outputs confirmed that:

- The Docker image was available in Minikube.
- The Flask Deployment was available.
- The Flask Pod was running.
- The Kubernetes Service was created.
- The Service was exposed through NodePort.
- Minikube generated a URL for accessing the application.

### Screenshot

![Kubernetes Deployment and Service](2-Minikube-Kubectl-Flask\screenshots\02-kubernetes-deployment-service.png)

---

# 13. View Deployment Details

Detailed information about the Deployment can be obtained using:

```powershell
kubectl describe deployment flask-app
```

This command provides information about:

- Deployment name
- Namespace
- Replica count
- Pod template
- Container image
- Container port
- Deployment strategy
- ReplicaSet
- Deployment events

The Deployment was successfully configured with:

```text
Replicas: 1
Image: flask-app:latest
Port: 15000/TCP
```

---

# 14. View Application Logs

The Flask application logs can be viewed using:

```powershell
kubectl logs <POD_NAME>
```

For example:

```powershell
kubectl logs flask-app-59f7cdccb4-cps2v
```

The logs confirm that Flask is running and listening on port `15000`.

Expected output includes:

```text
* Serving Flask app 'app'
* Debug mode: off
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:15000
```

---

# 15. Port and TargetPort

The Kubernetes Service configuration contains:

```yaml
ports:
  - port: 15000
    targetPort: 15000
```

### `port`

`port` represents the port exposed by the Kubernetes Service.

In this exercise:

```text
port: 15000
```

### `targetPort`

`targetPort` represents the port on which the application is listening inside the container.

In this exercise:

```text
targetPort: 15000
```

Therefore, the request flow is:

```text
Client
   ↓
NodePort Service
   ↓
Service Port: 15000
   ↓
Target Port: 15000
   ↓
Flask Container
   ↓
Flask Application
```

---

# 16. Kubernetes Architecture

The complete architecture for this exercise is:

```text
                        Browser
                           |
                           v
                  Minikube Service URL
                           |
                           v
                flask-app-service
                    NodePort
                           |
                           v
                  Service Port 15000
                           |
                           v
                 Target Port 15000
                           |
                           v
                Flask Kubernetes Pod
                           |
                           v
                  Flask Container
                           |
                           v
                    Flask :15000
```

The application flow is:

```text
Browser
   ↓
NodePort Service
   ↓
Flask Pod
   ↓
Flask Container
   ↓
Flask Application
```

---

# 17. What I Learned

Through this exercise, I learned how to deploy a Python application on Kubernetes using Docker, Minikube, `kubectl`, and YAML.

### Key concepts learned

- How to create a Flask application.
- How to containerize a Python application using Docker.
- How to build a Docker image using a Dockerfile.
- How to make a local Docker image available to Minikube.
- How Kubernetes Deployments manage application Pods.
- How to define a Deployment using YAML.
- How `replicas` controls the number of application instances.
- How labels and selectors connect Kubernetes resources.
- How `imagePullPolicy: Never` can be used with a locally available image.
- How to verify Deployments using `kubectl get deployments`.
- How to verify Pods using `kubectl get pods`.
- How to inspect Deployment details using `kubectl describe deployment`.
- How to view application logs using `kubectl logs`.
- How Kubernetes Services expose applications.
- The difference between `port` and `targetPort`.
- How NodePort Services provide access to applications running inside a Kubernetes cluster.
- How `minikube service --url` provides a URL for accessing a local Kubernetes Service.

---

# 18. Result

The Flask application was successfully containerized using Docker and deployed on a local Kubernetes cluster using Minikube.

The Kubernetes Deployment successfully created and managed the Flask Pod. The Pod reached the `Running` state, and the Flask application was confirmed to be running on port `15000`.

A NodePort Service was configured to expose the Flask application, and the application was successfully accessed through the Minikube-generated URL.

The final output displayed in the browser was:

```text
Hello from Flask on Kubernetes!
```

Therefore, the **Flask Application on Minikube exercise was successfully completed.**