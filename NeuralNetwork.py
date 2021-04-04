import numpy as np
import scipy.special
import random

# tweaks the weights based on the mutation rate
def mutate(val,rate):
    if random.gauss(0,0.1) < rate:
        #print(random.gauss(0,0.1))
        return val+random.gauss(0,0.1)
    else:
        return val
#neural network class definition
class neuralNetwork:

    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):

        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        # weight matrices, wih and who
        self.wih = [[np.random.uniform(-1,1) for i in range(self.inodes)] for j in range(self.hnodes)]
        self.who = [[np.random.uniform(-1,1) for i in range(self.hnodes)] for j in range(self.onodes)]
        #self.wih = np.random.normal(0.0, pow(self.inodes, -0.5), (self.hnodes, self.inodes))
        #self.who = np.random.normal(0.0, pow(self.hnodes, -0.5), (self.onodes, self.hnodes))

        # learning rate
        self.lr = learningrate

        # activation function : sigmoid function
        self.activation_function = lambda x: scipy.special.expit(x)
        # activation function : tanh function
        self.tan_activation_function = lambda x: np.tanh(x)

        pass

    # trains the neural network using backprop
    def train(self, inputs_list, targets_list):
        # convert inputs list to 2d array
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T

        # calculate signals into hidden layer
        hidden_inputs = np.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # calculate signals into final output layer
        final_inputs = np.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        # output layer error is the (target - actual)
        output_errors = targets - final_outputs
        # hidden layer error is the output_errors, split by weights, recombined at hidden nodes
        hidden_errors = np.dot(self.who.T, output_errors)

        # update the weights for the links between the hidden and output layers
        self.who += self.lr * np.dot((output_errors * final_outputs * (1.0 - final_outputs)),
                                        np.transpose(hidden_outputs))

        # update the weights for the links between the input and hidden layers
        self.wih += self.lr * np.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)),
                                        np.transpose(inputs))

        pass

    # predicts output using feedforward
    def predict(self, inputs_list):
        # convert inputs list to 2d array
        inputs = np.array(inputs_list, ndmin=2).T

        hidden_inputs = np.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)

        final_inputs = np.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)

        return final_outputs

    def copy(self):
        #print(self.who)
        return self

    # passes all the elements for mutation
    def map_mutate(self,rate):
        #print(1)
        #print("before",self.who)

        for i in range(len(self.wih)):
            for j in range(len(self.wih[i])):

                self.wih[i][j]=mutate(self.wih[i][j],rate)

        for i in range(len(self.who)):
            for j in range(len(self.who[i])):
                self.who[i][j] = mutate(self.who[i][j], rate)
        #print("after",self.who)
