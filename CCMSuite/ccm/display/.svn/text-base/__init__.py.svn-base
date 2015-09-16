engines=[
  'ccm.display.cairo.core.CairoDisplay',
  'ccm.display.tk.core.TkinterDisplay',
  'ccm.display.pygame.core.PygameDisplay',
]


def display(root,**args):
    d=None
    error=""

    for e in engines:
        module,obj=e.rsplit('.',1)
        try:
            m=__import__(module,globals(),locals(),[obj])
            d=getattr(m,obj)(root,**args)
            return d
        except ImportError,e:
            error+='\n'+str(e)
        
    print 'Error: could not create display: %s'%error
