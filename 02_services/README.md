# Services

> Service in Kubernetes is an abstraction layer for routing traffic to a logical set of pods. With service, we don't need to trace the IP address of each pod. Service usually uses label selector to select the pods that it needs to route to (in some cases service is created without selector in purpose). The service abstraction is powerful. It enables the decoupling and makes communication between micro-services possible. Currently Kubernetes service supports TCP and UDP.

### Service types

There are four types of services: ClusterIP, NodePort, LoadBalancer, and ExternalName.

![](https://i.ibb.co/SKWfKcn/services.png )

- ClusterIP: ClusterIP is the default service type. It exposes the service on a cluster-internal IP. Pods in
the cluster could reach the service via the IP address, environment variables, or DNS

```
kubectl create -f files/clusterip/RC.yml
kubectl create -f files/clusterip/RC2.yml
kubectl create -f files/clusterip/services.yml
```
We could see de full deatils about the service.
```
kubectl describe service nginx-service
kubectl get endpoints
```

Por defecto, k8s expondra 7 variables de entorno por cada servicio.
${SVCNAME}_SERVICE_HOST
${SVCNAME}_SERVICE_PORT
${SVCNAME}_PORT
${SVCNAME}_PORT_${PORT}_${PROTOCAL}
${SVCNAME}_PORT_${PORT}_${PROTOCAL}_PROTO
${SVCNAME}_PORT_${PORT}_${PROTOCAL}_PORT
${SVCNAME}_PORT_${PORT}_${PROTOCAL}_ADDR

![](https://i.ibb.co/prT0Crf/howtoworkservice.png)

Testeamos el funcionamiento del servicio a través de la variable de entorno.

```
kubectl create -f files/clusterip/pod.yml
```

Observamos el resultado de la creaación:

```
kubectl logs -f clusterip-chk
```

- NodePort: Kubernetes will allocate a port within a certain range on each node. Any traffic going to nodes on that port will be routed to the service port. Port number could be user-specified. If not specified, Kubernetes will randomly choose a port from range 30000 to 32767 without collision.

Corremos un servicio de tipo nodeport
```
kubectl create -f files/nodeport/service.yml
```

Podemos acceder via http://${NODE_IP}:80

- LoadBalancer:  
This type is only usable with cloud provider support, such as Google Cloud Platform By creating LoadBalancer service, Kubernetes will provision a load balancer by the Cloud
provider to the service.



