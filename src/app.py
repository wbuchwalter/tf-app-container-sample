import argparse
import sys
from flask import Flask
import tensorflow as tf
from model import Model
from server import Server
import server

tf.app.flags.DEFINE_boolean('train', False, '--train launch the app in training mode, ignore for serving')
FLAGS = tf.app.flags.FLAGS  

def main(_):
  model = Model()
  if FLAGS.train:
    model.train()
    model.save()
  else:
    model.restore()
    app = Flask(__name__)
    server = Server()
    server.set_model(model)
    app.add_url_rule('/', view_func=server.server_running)
    app.add_url_rule('/predict', view_func=server.predict)
    app.run(host= '0.0.0.0', port=80)
  
if __name__ == '__main__':
  tf.app.run()
