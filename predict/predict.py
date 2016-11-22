import tensorflow as tf
import numpy as np
import os
current_dir = os.path.dirname(__file__)

dataset = np.loadtxt(os.path.join(current_dir,"../collect/data/tweets.features.csv"),skiprows=1,delimiter=",")
x_len = len(dataset[0][:-1])
y_len = len(dataset[0]) - x_len	

x = tf.placeholder(tf.float32, shape=[None,x_len])
y = tf.placeholder(tf.float32, shape=[None,y_len])

#better initialization
w1 = tf.Variable(tf.zeros([]))
b1 = tf.Variable()


print(x_len,y_len)
#x = tf.placeholder(tf.float32, shape=[none,])