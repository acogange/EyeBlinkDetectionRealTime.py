import numpy as np

class CDense:
    def __init__(self,Weight,bias):
        self.Weight=Weight
        self.bias=bias

    def User_sigmoid(self,v):
        return 1 / (1 + np.exp(-v))

    def Predict(self,x):
        return self.Weight.dot(x)+self.bias

    def __call__(self, y):
        o=1/(1+np.exp(-y))

w=np.array([[1.2,2.3],[1.5,4.2]],dtype=np.float64)
b=np.array([[1.5],[-0.5]],dtype=np.float64)

dense1=CDense(w,b)
x=np.array([[1.4],[-1]],dtype=np.float64)
y1=dense1.Predict(x)
o1=dense1.User_sigmoid(y1)

y2=dense1.Predict(o1)
o2=dense1.User_sigmoid(y2)

print("y1=\n",y1)
print("o1=\n",o1)
print("y2=\n",y2)
print("y2=\n",o2)