import matplotlib
import matplotlib.pyplot as plt
from numpy import loadtxt
# load array
data = loadtxt('data.csv', delimiter=',')

plt.plot(data)
plt.show()

