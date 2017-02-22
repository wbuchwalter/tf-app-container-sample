from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
import os
import sys

def get_blob_service():
  return BlockBlobService(account_name='wibuch', account_key='PACubDwiOYvTPW1zVseSeTmSe1Q5IAhapoAc5g4Wy1nxLdlAFFMOptaxFYMuUlxL9QR6cuR0bN3sp8DdkxvukA==')

def upload_checkpoint_files(dir_path):
  delete_existing_blobs()
  blob_service = get_blob_service()
  files = os.listdir(dir_path)
  for file in files:
    blob_service.create_blob_from_path('checkpoints', file, os.path.join(dir_path, file))

def download_checkpoint_files(dir_path):
  blob_service = get_blob_service()  
  generator = blob_service.list_blobs('checkpoints')
  for blob in generator:
    blob_service.get_blob_to_path('checkpoints', blob.name, os.path.join(dir_path, blob.name))

def delete_existing_blobs():
  blob_service = get_blob_service()  
  generator = blob_service.list_blobs('checkpoints')
  for blob in generator:
    blob_service.delete_blob('checkpoints', blob.name)

