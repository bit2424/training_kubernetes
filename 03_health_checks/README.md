#Health checks

By default, Kubernetes will restart a container if it crashes for any reason. It uses Liveness and Readiness probes which can be configured for running a robust application by identifyin the healthy containers to send traffic to and restarting the one when required.

[Liveness and Readiness probe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) probes are defined and test the same against different states of a pod.

- **Liveness probes:** are used in Kubernetes to know when a pod is alive or dead. A pod can be in a dead state for a variety of reasons; Kubernetes will kill and recreate the pod when a liveness probe does not pass

- **Readiness probes:** are used in Kubernetes to know when a pod is a ready to serve traffic. Only when the readiness probe passes will a pod receive traffic from the service; if a readiness probe fails traffic will not be sent to the pod.

## Liveness Probe

Inside liveness folder we will found a file .yml that contains:
```yml
apiVersion: v1
kind: Pod
metadata:
  name: liveness-app
spec:
  containers:
  - name: liveness
    image: brentley/ecsdemo-nodejs
    livenessProbe:
      httpGet:
        path: /health
        port: 3000
      initialDelaySeconds: 5
      periodSeconds: 5
```

We create the pod ``` kubectl apply -f liveness/liveness.yml ``` 

We get the pods. Notice the RESTARTS output ``` kubectl get pod liveness-app ```

Now we see the event history which will show is any probe failures or restarts

```  kubectl describe pod liveness-app  ```

Now is time to introduce a failure.

Run the next command to send a SISGUSR1 signal to the nodejs application.
```
kubectl exec -it liveness-app -- /bin/kill -s SIGUSR1 1
```

Describe the pod after waiting for 15-20 second and you will notice the kubelet actions of killing the container and restarting it.
  
Now get the pod again and notice the restart field.
```
kubectl get pod liveness-app
```

** Point:  ** How can we check the status of the containers health checks?

## Readiness probe

The readinessProbe definition explains how a linux command can be configured as healthcheck. We create an empty file /tmp/healthy to configure readiness probe and use the same to understand how kubelet helps to update a deployment with only healthy pods.

We will now create a deployment to test readiness probe:

```
kubectl apply -f readiness/readiness.yml
```

The above command creates a deployment with 3 replicas and readiness probe as described in the beginning.

```
kubectl get pods -l app=readiness-deployment
```

Let us also confirm that all the replicas are available to serve traffic when a service is pointed to this deployment.

```
kubectl describe deployment readiness-deployment | grep Replicas:
```

### Introduce a Failure
Pick one of the pods from above 3 and issue a command as below to delete the /tmp/healthy file which makes the readiness probe fail.

```
kubectl exec -it <YOUR-READINESS-POD-NAME> -- rm /tmp/healthy
kubectl get pods -l app=readiness-deployment
```
Traffic will not be routed to the first pod in the above deployment. The ready column confirms that the readiness probe for this pod did not pass and hence was marked as not ready.
We will now check for the replicas that are available to serve traffic when a service is pointed to this deployment.

```
kubectl describe deployment readiness-deployment | grep Replicas:
```

When the readiness probe for a pod fails, the endpoints controller removes the pod from list of endpoints of all services that match the pod.

** Challenge point: ** How would you restore the pod to Ready status?


### References
- https://www.eksworkshop.com/beginner/070_healthchecks/readinessprobe/
- https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/




