### Kubectl

Es el comando para hacer la gestión de nuestro Cluster de Kubernetes

Sintax: ```  kubectl [command] [type] [name] [flags]  ``` 

Command: Operación a ejecutar  
Type: Tipo de recurso a desplegar  
name: nombre que le asignamos al recurso  

## Kubernetes Resources.
 
Kubernets Objects son las entradas en el cluster, el cual van a ser almacenaas en ETCD. Representan el estado deseado del Cluster.

El objeto spec describe el estado deseado del objeto. Se escribe en YML (YAML)
Ejemplo:
```  yml
apiVersion: Kubernetes API version 
kind: object type
metadata:
  spec metadata, i.e. namespace, name, labels and annotations
spec:
  the spec of Kubernetes object  
  ```
### Namespaces
Los NS nos permiten el aislamiento de los objetos dentro del cluster. Objetos entre diferentes NS son invisibles entre ellos.
Por defecto los objetos serán localizados en el NS del contexto actual.

Kubernetes tiene 3 ns por defecto: default, kube-system, kube-public

NS son muy importantes para la gestión de recursos y roles.

Ejemplo de como crear un objeto de tipo NS:

```yml
apiVersion: v1
kind: Namespace
metadata:
  name: project1
```
Corremos el comando para crear el NS
```
microk8s.kubectl create -f example-ns.yml
```
Validamos la creación del NS
```
microk8s.kubectl get ns
```

Corramos 2 contenedores dentro de nuestro NS
```
microk8s.kubectl run nginx --image=nginx:1.12.0 --replicas=2 --port=80 --namespace=project1
```

Listamos los pods de nuestro cluster
```
microk8s.kubectl get pods
```
¿Porqué no aparecen los pods desplegados?

### Label and Selector

Los label son un conjunto de valores key/pair que adjuntan un objeto. Están diseñados para proporcionar información significativa e identificable sobre los objetos.
Los usos comunes son indicar el nombre del micro-servicio, el nivel, el ambiente y la versión del software.

Sintax:
```
labels:
  $key1: $value1
  $key2: $value2
```

## PODS

Pequeña unidad de despliegue en KUbernetes. Puede contener uno o más contenedores. Contenedores en el mismo pods, corren en el mismo NS, context, comparten la misma red y volumes.
Más info: kubectl explain pods

Ejemplo:

```yml
apiVersion: v1
kind: Pod
metadata:
  name: example
spec:
  containers:
  - name: web
    image: nginx
  - name: centos
    image: centos
    command: ["/bin/sh", "-c", "while : ;do curl http://localhost:80/; sleep 10; done"]
```

Corremos el pod.
```
microk8s.kubectl create -f example-pod.yml
```
Revisamos y esperamos por la creación del pod.
```
kubectl get pods
```

Podemos validar la comunicación entre los dos pods revisando los logs del contenedor "Centos"
```
kubectl logs example centos
```

### ReplicaSet
Un pod no sobrevive por si mismo, cuando muere un pods por alguna u otra causa, este no se restaura y es ahí donde entra a jugar ReplicaSet.
ReplicaSet asegura que el número de replicas de pods configuradas, se mantengan en el cluster.

Ejemplo: Crearemos un ReplicaSet con 2 replicas deseadas.

```yml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      project: icesi-devops
    matchExpressions:
      - {key: version, operator: In, values: ["0.1", "0.2"]}
  template:
    metadata:
      name: nginx
      labels:
        project: icesi-devops
        service: web
        version: "0.1"
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
```
Corremos la RS y validamos el estado
```
kubectl create -f example-rs.yml
kubectl get rs
```
¿Cuantos pods tenemos?

Intentemos crear otro pod con la mismas etiquetas que en la RS.

```yml
apiVersion: v1
kind: Pod
metadata:
  name: our-nginx
  labels:
   project: icesi-devops
   service: web
   version: "0.1"
spec:
  containers:
  - name: nginx
    image: nginx
    ports:
    - containerPort: 80
```

¿Qué pasó con el nuevo pod?

Para escalar la replica
```
kubectl edit rs nginx
```

Para borrar recursos:
```
 kubectl delete <resource> <resource_name>
 kubectl delete -f <configuration_file>
```

### Deployments

Permite desplegar pods, desplegar actualizaciones, hacer rollback de pods y ReplicaSets. Definimos las actualizaciones de nuestro software de manera declarativa.

Ejemplo:

Hacemos un deployment de un nginx server
```
microk8s.kubectl run nginx --image=nginx:latest --replicas=2 --port=80
```
Validamos el deployment
```
microk8s.kubectl get deployments
```

Cómo podemos observar, la relación entre Deployment, ReplicaSet y pods es que el Deployment gestiona las ReplicaSet y Pods.
![alt text](https://static.packt-cdn.com/products/9781788997027/graphics/8bc2c7ec-a1de-4eb5-b188-6c05d7e80e26.png "")

Si nosotros matamos un pod, inmediatamente se programará un nuevo despliegue para cumplir con el estado deseado.

También podemos definir un objeto de tipo Deployment a través de un archivo yml.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  labels:
   app: nginx
spec:
  replicas: 2
  selector:
    matchLabels:
         app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
     containers:
     - name: nginx
       image: nginx:latest
       ports:
        - containerPort: 80

---

apiVersion: v1
kind: Service
metadata:
 name: nginx
 labels:
  app: nginx
spec:
 selector:
  app: nginx
 ports:
  - protocol: TCP
    port: 80
    targetPort: 80
    name: http
```

podemos ver el servicio y el deployment.
```
kubectl get services
kubectl get deployments
```
Podemos ejecutar "rolling updates" , para ello debemos tener en cuenta 3 parámetros.
minReadySeconds : valueDefault 0
maxSurge: valueDefault 25%
maxUnavailable: 25%

Ejemplo:
Agregar en el spec, del objeto deployment.
```yml
minReadySeconds: 3
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 1
```
Desplegamos nuevamente 
```
microk8s.kubectl replace -f deployment-example.yml
```
Hacemos una actualización de imagen, para ver el "Rolling update"
```
kubectl set image deployment nginx nginx=nginx:1.13.1
```
Podemos ver como se ha actualizado la imagen del contenedor 
```
kubectl get rs
kubectl describe rs <name>
```
### Services

Capa de abstracción para enrutamiento de tráfico a un conjunto logico de pods. Con los servicios no necesitamos apuntar a la dirección IP de un pod.

![alt txt]( )




