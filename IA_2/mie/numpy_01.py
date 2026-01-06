import numpy as np

a = np.array([1,2,3])
print(a*3)
print(a+3)

b = np.arange(0,8,2)
c = np.linspace(0,8,10)

print(b)
print(c)

x = np.random.rand()
print(x)

x2 = np.random.rand(3)
print(x2)

x3 = np.random.randint(1, 7, 2)
print(x3)

x4 =  np.random.uniform(10, 20)   
print(x4)