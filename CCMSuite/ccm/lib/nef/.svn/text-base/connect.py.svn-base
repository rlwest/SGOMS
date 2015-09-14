import numpy


array_class=numpy.array(0).__class__

class Connection:
    def __init__(self,pop1,pop2,func=None,weight=None):
        self.pop1=pop1
        pop1.outputs.append(self)
        self.pop2=pop2
        pop2.inputs.append(self)
        self.func=func
        self.weight=weight
        self.weight_is_matrix=hasattr(weight,'shape') and len(weight.shape)==2
        
        
    def type(self):
        return '%s_%s'%(self.pop1.mode,self.pop2.mode)


    def apply_weight(self,x):
        if self.weight is not None:
            if self.weight_is_matrix:
                x=numpy.dot(self.weight,x)
            else:
                x=x*self.weight
        return x
    
    def apply_func(self,x):
        if x is None: x=numpy.zeros(self.pop1.dimensions)
        if self.func is not None:
            v=self.pop1.array_to_value(x)
            v=self.func(v)
            if not isinstance(v,array_class):
                x=self.pop2.value_to_array(v)
            else:
                x=v
        return x
        
    def apply_func_weight(self,x):
        x=self.apply_func(x)
        x=self.apply_weight(x)
        return x









    """
    def value(self):
        return self.pop2.array_to_value(self.array())


    def convert(self,act):
        if self.dec is None: self.dec=self.pop1.get_decoder(func=self.func).T
        x=numpy.dot(self.dec,act)        
        if self.weight is not None:
            if self.weight_is_matrix:
                x=numpy.dot(self.weight,x)
            else:
                x*=self.weight
        return numpy.dot(self.pop2.basis,x)

    def get_decoder(self):
        if self.dec is None: self.dec=self.pop1.get_decoder(func=self.func).T
        return self.dec
        
        
    def activity(self,noise=None):
        if not self.pop1.use_activity:
            val=self.value()
            arr=self.pop2.value_to_array(val)
            return self.pop2.array_to_activity(arr)
        else:
            act=self.pop1.activity(noise=noise)
            act.shape=act.shape[0],1            
            J=self.pop2.alpha*self.convert(act)+self.pop2.Jbias
            J.shape=J.shape[0]
            J=self.pop2.nonlinearity(J)
            return J
        
    """        
    

        
def connect(x,y,func=None,weight=None):
    if func is not None and not callable(func):
        print func
        raise Exception('connection function is invalid')
    return Connection(x,y,func=func,weight=weight)
