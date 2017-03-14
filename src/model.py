import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import azure_blob_helper
import os 

save_dir="/tmp/ckp/"

class Model:
  x = tf.placeholder(tf.float32, [None, 784])
  W = tf.Variable(tf.zeros([784, 10]))
  b = tf.Variable(tf.zeros([10]))
  y = tf.matmul(x, W) + b
  sess = tf.InteractiveSession()
  

  def train(self):
    # Import training data
    mnist = input_data.read_data_sets('/app/MNIST_data/', one_hot=True)

    # Define loss and optimizer
    y_ = tf.placeholder(tf.float32, [None, 10])

    cross_entropy = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=self.y))
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy) 

    tf.global_variables_initializer().run()

    # Train
    for _ in range(1000):
      batch_xs, batch_ys = mnist.train.next_batch(100)
      self.sess.run(train_step, feed_dict={self.x: batch_xs, y_: batch_ys})

    # Test trained model
    correct_prediction = tf.equal(tf.argmax(self.y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    print(self.sess.run(accuracy, feed_dict={self.x: mnist.test.images,
                                        y_: mnist.test.labels}))

  def predict(self, x):
    feed_dict = {self.x: x}
    prediction = self.sess.run(tf.nn.softmax(self.y), feed_dict)
    return prediction
  
  def save(self, toblob = True):  
    if os.path.isdir(save_dir) == False:
      os.makedirs(save_dir)
    saver = tf.train.Saver()
    save_path = saver.save(self.sess, os.path.join(save_dir, "model"))
    print("Model saved in file: %s" % save_path)
    if toblob:
      azure_blob_helper.upload_checkpoint_files(save_dir)
      print("Model saved to blob")
  
  def restore(self, fromblob = True):
    if os.path.isdir(save_dir) == False:
      os.makedirs(save_dir)
    if fromblob:
      azure_blob_helper.download_checkpoint_files(save_dir)
    saver = tf.train.Saver()
    #saver = tf.train.import_meta_graph(os.path.join(save_dir, "model.meta"))
    saver.restore(self.sess, os.path.join(save_dir, "model"))
    print("Model restored from: %s" % os.path.join(save_dir, "model"))