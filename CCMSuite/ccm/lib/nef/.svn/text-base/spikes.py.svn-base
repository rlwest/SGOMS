import numpy
from ccm.lib.nef.activity import ActivityNode
from ccm.lib.nef.core import ArrayNode
from numpy import dot

class SpikeAccumulator:
    def __init__(self,dimensions,psc,decoder,weight):
        self.psc=psc
        self.data=numpy.zeros((dimensions,len(psc)))
        self.decoder=decoder
        self.weight=weight
        self.dimensions=dimensions
        self.basis=None
        self.alpha=None
        
    def add(self,spikes):
        if len(self.psc)>self.data.shape[1]:
            self.data=numpy.hstack((self.data,numpy.zeros((self.dimensions,len(self.psc)-self.data.shape[1]))))
        w=numpy.where(spikes>=0)
        if len(w)>0:
          for i in w[0]:
            dec=self.decoder[i,:]
            x=numpy.outer(self.psc,dec)
            if self.weight is not None:
                if hasattr(self.weight,'shape'):
                    x=numpy.dot(x,self.weight.T)
                else:
                    x*=self.weight
            self.data[:,:len(self.psc)]+=x.T
    def value(self):
        return self.data[:,0]
    def tick(self):
        self.data=self.data[:,1:]





class SpikingNode(ActivityNode):
    _set_current=None
    
    def configure_spikes(self,dt=0.001,pstc=0.02,current_noise=None):
        self.dt=dt
        self.pstc=pstc
        self.make_psc()
        self.voltage=numpy.zeros(self.neurons)
        self.spikes=numpy.zeros(self.neurons)
        self.refractory_time=numpy.zeros(self.neurons)
        self.Jm_prev=None
        self.mode='spike'
        self.current_noise=current_noise

    def make_psc(self,maximum_time=1.0,epsilon=0.01,n=0,area=1.0):
        if self.pstc<=self.dt:
            psc=numpy.array([1])
        else:
            t=numpy.arange(int(maximum_time/self.dt))*self.dt
            psc=t**n*numpy.exp(-t/self.pstc)

            # trim psc
            maxp=psc.max()
            pts=numpy.where(psc>maxp*epsilon)
            psc=psc[:pts[0][-1]]

        area2=numpy.sum(psc)*self.dt
        psc*=(area/area2)
        
        self.psc=psc

    def set(self,value,calc_output=True):
        ActivityNode.set(self,value,calc_output=False)
        if self.mode=='spike':
            c=self.array_to_current(self._set_array)+self.Jbias
            self._set_current=c


    def _calc_output(self):
        if self.mode!='spike': return ActivityNode._calc_output(self)
        if self._set_current is not None:
            curr=self._set_current
        elif self._input is not None:
            curr=self._input
        else:
            curr=numpy.zeros(self.neurons)
        if self.current_noise is not None:
            curr=self.add_current_noise(curr)
        self._output=self.calc_spikes(curr)
  
    def _clear_inputs(self):
        if self.mode!='spike': return ActivityNode._clear_inputs(self)
        if self._input is None: self._input=numpy.zeros(self.neurons)
        self._input[:]=self.Jbias

    def array(self):
        if self._array is None:
            if self.mode!='spike': return ActivityNode.array(self)
            self._array=self.activity_to_array(numpy.where(self._output>=0,1.0/self.dt,0))
        return self._array

    def _transmit_spike_direct(self,conn):
        if not hasattr(conn,'_spike_accumulator'):
            conn._spike_accumulator=SpikeAccumulator(conn.pop2.dimensions,self.psc,self.get_decoder(conn.func),conn.weight)
        conn._spike_accumulator.add(self._output)
        conn.pop2._input+=conn._spike_accumulator.value()
        conn._spike_accumulator.tick()

    def _transmit_spike_spike(self,conn):
        if not hasattr(conn,'_spike_accumulator'):
            conn._spike_accumulator=SpikeAccumulator(conn.pop2.dimensions,self.psc,self.get_decoder(conn.func),conn.weight)
        conn._spike_accumulator.add(self._output)
        conn.pop2._input+=dot(conn.pop2.basis,conn._spike_accumulator.value())*conn.pop2.alpha
        conn._spike_accumulator.tick()


    def _transmit_direct_spike(self,conn):
        conn.pop2._input+=conn.pop2.array_to_current(conn.apply_func_weight(self._output))
    

    def add_current_noise(self,curr):
        return curr
        noise=self.current_noise
        if noise>0:
            curr=numpy.random.normal(curr,noise)
            #curr=numpy.maximum(0,curr)            
        return curr


    """
    def apply_spikes(self,connect):
        spikes=connect.pop1.spikes
        decoder=connect.get_decoder().T
        psc=connect.pop1.psc
        weight=connect.weight
        
        if self.array_from_spikes is None:
            self.array_from_spikes=numpy.zeros(self.dimensions)
            self.array_from_spikes.shape=(self.dimensions,1)
            
        array=self.array_from_spikes
        if len(psc)>array.shape[1]:
            
            array=numpy.hstack((array,numpy.zeros((self.dimensions,len(psc)-array.shape[1]))))
            self.array_from_spikes=array

        for i in numpy.where(spikes>=0)[0]:
            if len(decoder[i].shape)==1:
                x=psc*decoder[i]
            else:
                x=numpy.outer(psc,decoder[i])
            if weight is not None:
                if connect.weight_is_matrix:
                    x=numpy.dot(weight,x)
                else:
                    x*=weight
            array[:len(psc)]+=x


    def calc_direct(self):
        if self.array_from_direct is None:
            self.array_from_direct=numpy.zeros(self.dimensions)
        self.array_from_direct[:]=0
        for conn in self.inputs:
            if not conn.pop1.use_spikes:
                if conn.pop1.use_activity and self.use_activity:
                    self.array_from_direct+=self.activity_to_array(conn.activity())
                else:
                    self.array_from_direct+=conn.array()
        

    def array(self,noise=None):
        if self.set_array is not None:
            return self.set_array
        if self.current_array is None:
            self.current_array=numpy.zeros(self.dimensions)        
        return self.current_array

    def recalc_array(self):
        if self.current_array is None:
            self.current_array=numpy.zeros(self.dimensions)
        else:
            self.current_array[:]=0
        if self.direct is not None:
            self.current_array+=self.direct
        if self.array_from_spikes is not None:
            self.current_array+=self.array_from_spikes[:,0]

    
    def tick(self):
        nodes=self.all_nodes()
        for node in nodes:
            node.calc_direct()
            if node.use_spikes:
                node.calc_spikes(node.array())
            if node.array_from_spikes is not None:
                node.array_from_spikes=node.array_from_spikes[:,1:]
        for node in nodes:
            node.direct=node.array_from_direct[:]
            node.recalc_array()
        for node in nodes:
            if node.use_spikes:
                for conn in node.outputs:
                    conn.pop2.apply_spikes(conn)
    """    
    
    def calc_spikes(self,current):
        Jm=current
        dt=self.dt
        #Jm=self.alpha.T*dot(self.basis,array)+self.Jbias.T
        if self.Jm_prev is None: self.Jm_prev=Jm
        R=1.0
        v=self.voltage

        # Euler's method
        dV=dt/self.t_rc*(self.Jm_prev*R-v)

        # Midpoint method
        #tt=dt/self.t_rc
        #dV=tt*(R*(Jm/2+self.Jm_prev*(0.5-tt))+v*(tt-1))

        #dV=dV[0]

        self.Jm_prev=Jm
        v+=dV
        v=numpy.maximum(v,0)


        # do accurate timing for when the refractory period ends
        self.refractory_time-=dt
        post_ref=1.0-self.refractory_time/dt  
        v=numpy.where(post_ref>=1,v,v*post_ref) # scale by amount of time outside of refractory period
        v=numpy.where(post_ref<=0,0,v)  # set to zero during refactory period
        
        self.spikes[:]=-1
        V_threshold=self.J_threshold*R
        for i in numpy.where(v>V_threshold):
            overshoot=(v[i]-V_threshold)/dV[i]
            spiketime=dt*(1.0-overshoot)
            self.refractory_time[i]=spiketime+self.t_ref
            self.spikes[i]=(1.0-overshoot)
            v[i]=0
        self.voltage=v
        
        return self.spikes    
