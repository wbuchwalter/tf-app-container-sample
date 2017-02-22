import numpy as np
import json

class Server:
  model = None

  def set_model(self, model):
    self.model = model

  def server_running(self):
    return 'Server is running.'

  def predict(self):
    x = np.random.rand(1,784)
    prediction = self.model.predict(x)   
    return json.dumps(prediction.tolist(), separators=(',',':'))
    
