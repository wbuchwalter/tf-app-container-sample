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
