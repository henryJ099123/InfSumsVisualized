import numpy as np

class Complex:

    def __init__(self, a=1, b=0, rect=True):
        a = float(a)
        b = float(b)
        if rect:
            self.real = a
            self.im = b
            self.r = np.sqrt(a*a + b*b)
            self.theta = np.atan2(b, a)
        else:
            self.r = a
            self.theta = b
            self.real = a * np.cos(b)
            self.im = a * np.sin(b)
    
    def setreal(self, a):
        self.real = a
        self.r = np.sqrt(a*a + self.im*self.im)
        self.theta = np.atan2(self.im, a)

    def setim(self, b):
        self.im = b
        self.r = np.sqrt(self.real**2 + b*b)
        self.theta = np.atan2(b, self.real)
    
    def setrad(self, r):
        self.r = r
        self.real = r * np.cos(self.theta)
        self.im = r * np.sin(self.theta)

    def settheta(self, theta):
        self.theta = theta
        self.real = self.r * np.cos(theta)
        self.im = self.r * np.sin(theta)
    
    def __neg__(self):
        return Complex(-self.real, -self.im)
    
    def __abs__(self):
        return Complex(abs(self.real), abs(self.im))

    def __add__(self, other):
        return Complex(self.real + other.real, self.im + other.im)

    def __sub__(self, other):
        return Complex(self.real - other.real, self.im - other.im)

    def __mul__(self, z):
        return Complex(self.real*z.real-self.im*z.im, self.im*z.real+self.real*z.im)
    
    def conj(self):
        self.setim(-self.im)
    
    def reciprocate(self):
        self.setreal(self.im / (self.r * self.r), self.im / (self.r * self.r))
    
    # returns the PRINCIPAL VALUE of the complex power
    def __pow__(self, z):
        nt = self.theta % (2*np.pi)
        if nt > np.pi:
            nt -= np.pi * 2
        self.settheta(nt)
        r = self.r**z.real* np.exp(-z.im*self.theta)
        theta = z.im*np.log(self.r)+z.real*self.theta
        return Complex(r, theta, False)
    
    def __div__(self, z):
        return self.reciprocate() * z

    def __str__(self):
        if self.im >= 0:
            im_string = f'+ {self.im:.4f}i'
        else:
            im_string = f'- {-self.im:.4f}i'
        return f"{self.real:.4f} {im_string}, {self.r:.4f}e^(i{self.theta:.4f})"
    