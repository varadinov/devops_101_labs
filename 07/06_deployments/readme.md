# Deployment with Service
Objective: Use a Deployment to manage a ReplicaSet with versioned upgrades.

# Steps
* Create a Deployment to manage pods and Service
```bash
kubectl apply -f .
```

* Review deployment
```bash
kubectl describe deployment nginx-deployment
```
**Note:** If you review carefully the description of the deployment, you will find that it relays on ReplicaSets. 

* List replicasets
```bash
kubectl get replicasets
```
You will find a replica set with random suffix (e.g. -8bfc588). It is managed by the deployment object.

* Get nginx response header "Server"
```bash
curl -s --head localhost:30000 | grep Server:
```
You will see value nginx/1.21.5

* Use rolling updates to ensure zero downtime during updates
If you want to update the application version, you only need to update the Deployment's Pod template.  
We will update the nginx image version to 1.21.6. You can update the deployment.yaml file and change the image: nginx:1.21.5 to image: nginx:1.21.6

You can edit menually the file with text editor or use this command:
```bash 
sed -i 's/nginx:1.21.5/nginx:1.21.6/g' deployment.yaml
```

```bash
kubectl apply -f deployment.yaml
```

* Check rollout status
```bash
kubectl rollout status deployment/nginx-deployment
```

You should see output like this
```
Waiting for deployment "nginx-deployment" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "nginx-deployment" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "nginx-deployment" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "nginx-deployment" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "nginx-deployment" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "nginx-deployment" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "nginx-deployment" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "nginx-deployment" rollout to finish: 1 old replicas are pending termination...
deployment "nginx-deployment" successfully rolled out
```


* Get nginx response header "Server"
```bash
curl -s --head localhost:30000 | grep Server:
```
You will see value nginx/1.21.6


* Cleanup
```bash
kubectl delete -f .
```