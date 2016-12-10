import numpy as np
import tflearn
import os
current_dir = os.path.dirname(__file__)

import tflearn.data_utils

data,labels_a = tflearn.data_utils.load_csv(os.path.join(current_dir,"../collect/data/tweets.features.csv"),target_column=4,columns_to_ignore=[5],categorical_labels=False)
labels_b = tflearn.data_utils.load_csv(os.path.join(current_dir,"../collect/data/tweets.features.csv"),columns_to_ignore=[0,1,2,3,4], target_column=5,categorical_labels=False)[1]

print(data[3])

labels_a = np.array(labels_a, dtype=np.float32)
labels_b = np.array(labels_b, dtype=np.float32)
#used for binary labels, change the threshold to tweak
labels_a[:] = [int(i > 0.5) for i in labels_a]
labels_b[:] = [int(i > 0.5) for i in labels_b]

print(labels_a[0])
print(labels_b[0])
data = np.array(data, dtype=np.float32)
labels = np.column_stack((labels_a,labels_b))
#labels = np.reshape(labels,(len(labels),1))

net = tflearn.input_data(shape=[None,4])
net = tflearn.fully_connected(net, 5)
net = tflearn.fully_connected(net, 2, activation='softmax')
net = tflearn.regression(net,optimizer="SGD",learning_rate=0.9)#,loss="binary_crossentropy")

# Define model
model = tflearn.DNN(net)
# Start training (apply gradient descent algorithm)
model.fit(data, labels, n_epoch=1, batch_size=100, show_metric=True)

print(model.predict([data[3]]))
print(model.predict([[0,1,0,0]]))
