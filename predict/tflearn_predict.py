import numpy as np
import tflearn
import os
import random
current_dir = os.path.dirname(__file__)

import tflearn.data_utils


def examples(model, n = 2, seed = None):
	dataset = open(os.path.join(current_dir,"../collect/data/tweets.processed.log"),"r").read().splitlines()
	dataset = [i.split(" ;; ") for i in dataset]
	if(seed == None):
		seed = random.randint(0,9999)
	random.seed(seed)
	for i,v in enumerate(dataset):
		dataset[i][1] = dataset[i][1].split(",")
		dataset[i][2] = [float(j) for j in dataset[i][2].split(",")]

	examples = [random.randint(0,len(dataset)) for _ in range(0,n)]
	print("==============================")
	for i in examples:
		print("Text: ", dataset[i])
		print(model.predict([data[i]]))
	print("Seed:",seed)


data,labels_a = tflearn.data_utils.load_csv(os.path.join(current_dir,"../collect/data/tweets.features.csv"),target_column=5,columns_to_ignore=[6],categorical_labels=False)
labels_b = tflearn.data_utils.load_csv(os.path.join(current_dir,"../collect/data/tweets.features.csv"),columns_to_ignore=[0,1,2,3,4,5], target_column=6,categorical_labels=False)[1]

print(data[0])

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

net = tflearn.input_data(shape=[None,5])
net = layer1 = tflearn.fully_connected(net, 5, name="layer1")
#net = tflearn.fully_connected(net, 10)
net = tflearn.fully_connected(net, 2, activation='softmax')
net = tflearn.regression(net,optimizer="SGD",learning_rate=0.9)#,loss="binary_crossentropy")

# Define model
model = tflearn.DNN(net)
# Start training (apply gradient descent algorithm)
model.fit(data, labels, n_epoch=5, batch_size=100, show_metric=True,validation_set=0.2)


examples(model,6)
print(model.predict([[0,1,0,0,1]]))
print(model.get_weights(layer1.W))