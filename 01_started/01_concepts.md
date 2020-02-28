Kubectl

Es el comando para hacer la gestión de nuestro Cluster de Kubernetes

Sintax: kubectl [command] [type] [name] [flags] 

Command: Operación a ejecutar
Type: Tipo de recurso a desplegar
name: nombre que le asignamos al recurso

Kubernetes Resources.

Kubernets OBjects son las entradas en el cluster, el cual van a ser almacenaas en ETCD. Representan el estao deseado del Cluster.

El objeto spec describe el estado deseado del objeto. Se escribe en YML (YAML)
Ejemplo:
```yml
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
