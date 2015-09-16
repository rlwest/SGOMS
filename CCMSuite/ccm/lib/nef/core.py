import numpy
import ccm

from ccm.lib.nef.connect import connect

class ArrayNode:    
    _set_array=None
    _value=None
    _array=None
    _input=None
    _output=None
        
    def __init__(self,dimensions,min=-1,max=1,noise=0.01):
        self.inputs=[]
        self.outputs=[]
        self.dimensions=dimensions
        self.min=min
        self.max=max
        self.array_noise=noise
        
        self.mode='direct'
        
        
    def set(self,value,calc_output=True):
        array=numpy.array(self.value_to_array(value))
        if len(array.shape)>1: array.shape=array.shape[0]
        assert len(array)==self.dimensions
        self._set_array=array
        if calc_output: self._calc_output()
        self._array=None
        self._value=None

    def array(self):
        if self._array is None:
            if self._output is None: self._output=numpy.zeros(self.dimensions)
            self._array=self._output
        return self._array
    def value(self):
        if self._value is None:
            self._value=self.array_to_value(self.array())
        return self._value



    def _calc_output(self):
        if self._output is None: self._output=numpy.zeros(self.dimensions)
        else: self._output[:]=0
        if self._set_array is not None:
            self._output+=self._set_array
        elif self._input is not None:
            self._output+=self._input
        if self.array_noise>0:
            self._output+=numpy.random.randn(self.dimensions)*self.array_noise

    def _clear_inputs(self):
        if self._input is None: self._input=numpy.zeros(self.dimensions)
        else: self._input[:]=0
    
    def _transmit_direct_direct(self,conn):
        conn.pop2._input+=conn.apply_func_weight(self._output)
        
    def tick(self):
        nodes=self.all_nodes()
        for n in nodes:
            n._clear_inputs()
        for n in nodes:
            for conn in n.outputs:
                f=getattr(n,'_transmit_%s'%conn.type())
                f(conn)
        for n in nodes:
            n._calc_output()
            n._value=None
            n._array=None


    def connect(self,other,func=None,weight=None):
        connect(self,other,func=func,weight=weight)
    
    def all_nodes(self,list=None):
        if list is None: list=[]
        list.append(self)
        for c in self.inputs:
            if c.pop1 not in list:
                c.pop1.all_nodes(list)
        for c in self.outputs:
            if c.pop2 not in list:
                c.pop2.all_nodes(list)
        return list
                


