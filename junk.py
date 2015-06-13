class A(object):
    def x(self):
        print 'A'

class B(A):
    def x(self):
        super(B,self).x()
        print "B"

b = B()
b.x()
        
