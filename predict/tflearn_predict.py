import numpy as np
import tflearn
import os
current_dir = os.path.dirname(__file__)

import tflearn.data_utils

data,labels = tflearn.data_utils.load_csv(os.path.join(current_dir,"../collect/data/tweets.features.csv"),target_column=3,categorical_labels=False)

data = np.array(data, dtype=np.float32)
labels = np.reshape(labels,(len(labels),1))

net = tflearn.input_data(shape=[None,3])
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, 1, activation='linear')
net = tflearn.regression(net)

# Define model
model = tflearn.DNN(net)
# Start training (apply gradient descent algorithm)
model.fit(data, labels, n_epoch=10, batch_size=1, show_metric=True)
