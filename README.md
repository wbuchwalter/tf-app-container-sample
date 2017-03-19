# tensorflow-server
### Building the image
##### CPU:
`docker build -t ${USER}/tf-server .`

##### GPU:
`docker build -f Dockerfile.gpu -t ${USER}/tf-server-gpu .`

### Running the container
##### To train the model
`docker run -it -e STORAGE_ACCOUNT_NAME='' -e STORAGE_ACCOUNT_KEY='' ${USER}/tf-server --train`
(if using the GPU image, replace docker with nvidia-docker)
##### To serve predictions
`docker run -p <some localhost port>:80 -e STORAGE_ACCOUNT_NAME='' -e STORAGE_ACCOUNT_KEY='' ${USER}/tf-server`

Then make a GET request to `localhost:<port>/predict` to get the prediction

### Model save/restore
TF checkpoint files will be saved to an Azure storage account defined in `azure-blob-helper.py`.

## Deploying using Kubernetes on Azure Container Service (ACS)

### Getting Started
See [Microsoft Azure Container Service Engine - Kubernetes Multi-GPU support Walkthrough](https://github.com/ritazh/acs-engine/blob/enable-k8v1.6-multiplegpu/docs/kubernetes.gpu.md) on how to set up (multi) GPU Kubernetes clusters in ACS

Create a Standard storage account and then create a blob container called `checkpoints`

Edit STORAGE_ACCOUNT_NAME and STORAGE_ACCOUNT_KEY for k8s/server.yaml and k8s/trainer.yaml with your account name and keys (for GPU, use server-gpu.yaml and trainer-gpu.yaml)

### To train the model

`kubectl create -f trainer-gpu.yaml`

`export PODNAME=$(kubectl get pods -l app=tensorflow-server --kubeconfig=config.gpu -o jsonpath=tensorflow-server)`

`kubectl logs $PODNAME -f`

Wait for model to be saved to storage

Delete the trainer

`kubectl delete job tensorflow-trainer`

### To serve predictions

`kubectl create -f server-gpu.yaml`

`kubectl get svc -l run=tensorflow-server`

Wait for EXTERNAL-IP to be available and then make a GET request to `EXTERNAL-IP:<PORT>/predict` to get the prediction
