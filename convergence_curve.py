import matplotlib
import matplotlib.pyplot as plt
from numpy import loadtxt
# load array
data = loadtxt('data.csv', delimiter=',')

plt.plot(data)
plt.xlabel("Number of Generations")
plt.ylabel("Max Score in each generation")
plt.title("Learning Curve")
plt.show()

