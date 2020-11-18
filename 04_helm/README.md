# Helm
![](https://pandorafms.com/blog/wp-content/uploads/2020/08/helm-6.png)
> Helm is a package manager for Kubernetes that packages multiple Kubernetes resources into a single logical deployment unit called a Chart. Charts are easy to create, version, share, and publish.

In this section, we’ll cover installing Helm. Once installed, we’ll demonstrate how Helm can be used to deploy a simple python webserver, and a more sophisticated microservice.

## Advantages
- Achieve a simple (one command) and repeatable deployment
- Manage application dependency, using specific versions of other application and services
- Manage multiple deployment configurations: test, staging, production and others
- Execute post/pre deployment jobs during application deployment
- Update/rollback and test application deployments

## Install the Helm CLI

Before we can get started configuring Helm, we will need to first install the command line tools that you will interact with. To do this, run the following:  

``` 
curl -sSL https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash 
```  

We can verify the version

``` 
helm version --short  
```

Let’s configure our first Chart repository. Chart repositories are similar to APT or yum repositories that you might be familiar with on Linux, or Taps for Homebrew on macOS.  
Download the stable repository so we have something to start with:

``` 
helm repo add stable https://charts.helm.sh/stable 
```

```
helm search repo stable 
```

### Deploy nginx with helm

Helm uses a packaging format called Charts. A Chart is a collection of files and templates that describes Kubernetes resources.

```  
# first, add the default repository, then update
helm repo add stable https://charts.helm.sh/stable
helm repo update
helm search repo

```
You can see from the output that it dumped the list of all Charts we have added. In some cases that may be useful, but an even more useful search would involve a keyword argument. So next, we’ll search just for nginx:

``` 
helm search repo nginx 
```
In the last step, we saw that nginx offers many different products via the default Helm Chart repository, but the nginx standalone web server is not one of them.

```
helm repo add bitnami https://charts.bitnami.com/bitnami  
helm search repo bitnami
helm search repo bitnami/nginx
```

Installing the Bitnami standalone nginx web server Chart involves us using the helm install command. A Helm Chart can be installed multiple times inside a Kubernetes cluster. This is because each installation of a Chart can be customized to suit a different purpose. For this reason, you must supply a unique name for the installation, or ask Helm to generate a name for you.

Use the helm utility to install the bitnami/nginx chart and specify the name mywebserver for the Kubernetes deployment. Consult the helm install documentation or run the helm install --help command to figure out the syntax.

```
helm install mywebserver bitnami/nginx
kubectl get svc,po,deploy
```

To remove all the objects that the Helm Chart created, we can use Helm uninstall.

Before we uninstall our application, we can verify what we have running via the Helm list command:
```
helm list
helm uninstall mywebserver
kubectl get pods -l app.kubernetes.io/name=nginx
kubectl get service mywebserver-nginx -o wide
```

### Deploy example microservices using helm
Helm charts have a structure similar to:

/somedir
  /Chart.yaml  # a description of the chart  
  /values.yaml # defaults, may be overridden during install or upgrade  
  /charts/ # May contain subcharts  
  /templates/ # the template files themselves  
  
```
helm create hello-world-python
```

Now we customize defualt values with our values  
  
for test our template deployment we make
```
helm install --debug --dry-run workshop ~/environment/eksdemo
```
This command let us render template without installing the chart.  

Now we deploy our chart. 
```
helm install hello-world-python <pathtotemplate>
kubectl get svc,po,deploy
```

Now test the service, copy the external IP into browser
```
kubectl get svc
```

Update the demo application chart with a breaking change  
Open values.yaml and modify the image name under image to icesiops/hello-world-non-existing. This image does not exist, so this will break our deployment.

```
helm upgrade hello-world-python <pathtotemplate>
kubectl get pods
helm status hello-world-python
helm history hello-world-python
```

Rollback the failed upgrade
Then, rollback to the previous application revision (can rollback to any revision too):

```
helm rollback hello-world-python 1
helm status hello-world-python
kubectl get pods
helm uninstall hello-world-python
```






  

  






