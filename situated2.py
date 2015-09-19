# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 13:53:07 2015

@author: Korey
"""
#################### SGOMS ###################

import sys
sys.path.append('/Users/robertwest/CCMSuite')

import ccm      
log=ccm.log()

#log=ccm.log(html=True) 

from ccm.lib.actr import *



# --------------- Environment ------------------

class MyEnvironment(ccm.Model):
    
    
    chicken=ccm.Model(isa='chicken',location='grill',state='cooked',salience=0.2)
    pita=ccm.Model(isa='pita',location='bins2',status='in_bag',salience=0.2)
    
    cheese=ccm.Model(isa='cheese',location='in_bins1',salience=0.2)
    feta=ccm.Model(isa='feta',location='in_bins1',salience=0.2)
    cucumber=ccm.Model(isa='cucumber',location='in_bins1',salience=0.2)
    green_pepper=ccm.Model(isa='green_pepper',location='in_bins1',salience=0.2)
    mushroom=ccm.Model(isa='mushroom',location='in_bins1',salience=0.2)
    lettuce=ccm.Model(isa='lettuce',location='in_bins1',salience=0.2)
    tomato=ccm.Model(isa='tomato',location='in_bins1',salience=0.2)

    green_olives=ccm.Model(isa='green_olives',location='in_bins2',salience=0.2)
    black_olives=ccm.Model(isa='black_olives',location='in_bins2',salience=0.2)
    hot_peppers=ccm.Model(isa='hot_peppers',location='in_bins2',salience=0.2)
    onion=ccm.Model(isa='onion',location='in_bins2',salience=0.2)
    
    humus=ccm.Model(isa='humus',location='in_bins2',salience=0.2)
    tzatziki=ccm.Model(isa='tzatziki',location='in_bins2',salience=0.2)

    hot_sauce=ccm.Model(isa='hot_sauce',location='in_bins2',salience=0.2)
    
    worker=ccm.Model(isa='worker',location='at_counter',salience=0.2)
    spider=ccm.Model(isa='spider',location='on_counter',feature1='yellow_stripe',salience=0.99)

    motor_finst=ccm.Model(isa='motor_finst',state='re_set')



class MotorModule(ccm.Model):     ### defines actions on the environment
        
    def change_location(self, env_object, slot_value):
        yield 2                   
        x = eval('self.parent.parent.' + env_object)
        x.location= slot_value
        print env_object
        print slot_value
        self.parent.parent.motor_finst.state='finished'
        
    def motor_finst_reset(self):             
        self.parent.parent.motor_finst.state='re_set'



class MethodModule(ccm.ProductionSystem):  # creates an extra production system for the motor system
    production_time=0.04


    # adding method


    def do_add(b_method='method:add target:?target state:start'): # target is the chunk to be altered
        motor.change_location(target,"in_wrap")
        b_method.set('method:add target:?target state:running')
        print 'target=',target
     
    def done_add(b_method='method:add target:?target state:running',
                 motor_finst='state:finished'):
        b_method.set('method:add target:?target state:finished')
        motor.motor_finst_reset()
        print 'finished=',target
        

    # checking method


    def do_check(b_method='method:check target:?target state:start'): # target is the chunk to be checked
        b_method.set('method:check target:?target state:running')
        print 'target=',target
     
    def result1_check(b_method='method:check target:?target state:running',
                      chicken='state:cooked'):
        b_method.set('method:check target:?target state:finished')
        print 'finished=',target

    def result2_check(b_method='method:check target:?target state:running',
                      chicken='state:raw'):
        b_method.set('method:check target:?target state:finished')
        print 'finished=',target



# --------------- Vision Module ------------------

class VisionModule(ccm.ProductionSystem):  
    production_time=0.045


#
# --------------- Emotion Module ------------------

class EmotionalModule(ccm.ProductionSystem):  
    production_time=0.043



# --------------- Agent ------------------

class MyAgent(ACTR):


########### create agent architecture ################################################
#############################################################

    # module buffers
    b_system=Buffer()                            # create system buffers
    b_DM=Buffer()   
    b_motor=Buffer
    b_visual=Buffer()
    b_image=Buffer()
    b_focus=Buffer()

    # goal buffers
    b_context=Buffer()
    b_plan_unit=Buffer()                         # create buffers to represent the goal module
    b_unit_task=Buffer()
    b_method=Buffer()
    b_operator=Buffer()
    b_emotion=Buffer()

    # associative memory
    DM=Memory(b_DM)                              # create the DM memory module

    # perceptual motor module
    vision_module=SOSVision(b_visual,delay=0)    # create the vision module
    motor=MotorModule(b_motor)                   # put motor production module into the agent

    # auxillary production modules
    Methods=MethodModule(b_method)               # put methods production module into the agent    
    Eproduction=EmotionalModule(b_emotion)       # put the Emotion production module into the agent
    p_vision=VisionModule(b_visual)    

############ add planning units to declarative memory and set context buffer ###############
#########################################################################
    
    def init():                                             

        DM.add ('planning_unit:prep_wrap    cuelag:none          cue:start          unit_task:X')
        DM.add ('planning_unit:prep_wrap    cuelag:start         cue:X        unit_task:cheese')
        DM.add ('planning_unit:prep_wrap    cuelag:veggies       cue:cheese         unit_task:pickles')       
        DM.add ('planning_unit:prep_wrap    cuelag:cheese        cue:pickles        unit_task:spreads')
        DM.add ('planning_unit:prep_wrap    cuelag:pickles       cue:spreads        unit_task:sauce')
        DM.add ('planning_unit:prep_wrap    cuelag:spreads       cue:sauce          unit_task:finished')

        DM.add ('planning_unit:meat         cuelag:none          cue:start          unit_task:check_meat')                     
        DM.add ('planning_unit:meat         cuelag:start         cue:check_meat     unit_task:add_meat')
        DM.add ('planning_unit:meat         cuelag:check_meat    cue:add_meat       unit_task:finished')       


        b_context.set('finshed:nothing status:unoccupied')




########### create productions for choosing planning units #####################################
#########################################################################



        

##this one fires when nothing has been done yet
    def prep_wrap(b_context='finshed:nothing status:unoccupied'): # status:unoccupied triggers the selection of a planning unit
         b_plan_unit.set('planning_unit:prep_wrap cuelag:none cue:start unit_task:X state:begin_sequence') # which planning unit and where to start
         b_context.set('finished:nothing status:occupied') # update context status to occupied
         print 'prep the wrap planning unit is chosen'
##this one fires on the condition that any other planning unit has been completed
    def get_meat(b_context='finished:prep_wrap status:unoccupied'):
         b_plan_unit.set('planning_unit:meat cuelag:none cue:start unit_task:check_meat state:running')
         b_unit_task.set('unit_task:check_meat state:start')
         b_context.set('finished:prep_wrap status:occupied')
         print 'get the meat'

         




########## unit task set up #############################################
#########################################################################


## these set up whether it will be an ordered or a situated planning unit
         

    def setup_situated_planning_unit(b_plan_unit='planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:begin_situated'): 
        b_unit_task.set('state:start type:unordered')
        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running') # next unit task     
        print 'begin unorderdered planning with unit task = ',unit_task
        
    def setup_ordered_planning_unit(b_plan_unit='planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:begin_sequence'): 
        b_unit_task.set('unit_task:?unit_task state:start type:ordered')
        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running') # next unit task     
        print 'begin orderdered planning with unit task = ',unit_task

## these manage the sequence

    def request_next_unit_task(b_plan_unit='planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running',                   
                               b_unit_task='unit_task:?unit_task state:finished type:ordered'): 
        DM.request('planning_unit:?planning_unit cue:?unit_task unit_task:? cuelag:?cue')                 
        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:retrieve') # next unit task     
        print 'finished unit task = ',unit_task
        
    def retrieve_next_unit_task(b_plan_unit='state:retrieve',
                                b_DM='planning_unit:?planning_unit cuelag:?cuelag cue:?cue!finished unit_task:?unit_task'): 
        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running')
        b_unit_task.set('unit_task:?unit_task state:start type:ordered')
        print 'unit_task = ',unit_task

    def last_unit_task(b_plan_unit='planning_unit:?planning_unit',
                       b_unit_task='unit_task:finished state:start type:ordered'):
        print 'finished planning unit=',planning_unit
        b_unit_task.set('stop')
        b_context.set('finished:?planning_unit status:unoccupied')




################# unit tasks ######################################################
######################################################################
        


## veggies unit task


    def OR_unit_task_unordered(b_unit_task='state:start type:unordered'):
        b_unit_task.set('unit_task:X state:begin type:unordered')
       # b_focus.set('start')
        print 'start unit task X unordered'

    def OR_unit_task_ordered(b_unit_task='unit_task:X state:start type:ordered'):
        b_unit_task.set('unit_task:X state:begin type:ordered')
       # b_focus.set('start')
        print 'start unit task X ordered'

    def start_unit_task(b_unit_task='unit_task:X state:begin type:?type'):
        b_unit_task.set('unit_task:X state:running type:?type')
        b_method.set('method:add target:tomato state:start')
        b_focus.set('')
        print 'start unit task'

    def tomato(b_unit_task='unit_task:X state:running type:?type',
               b_method='method:add target:tomato state:finished'):
        print 'tomato method finished'
        b_method.set('method:add target:cucumber state:start')
    def cucumber(b_unit_task='unit_task:X state:running type:?type',
                 b_method='method:add target:cucumber state:finished'):
        print 'cucumber method finished'
        b_method.set('method:add target:green_pepper state:start')
    def green_pepper(b_unit_task='unit_task:X state:running type:?type',
                     b_method='method:add target:green_pepper state:finished'):
        b_unit_task.set('unit_task:X state:end type:?type')
        print 'green_pepper method finished'

    def finished_ordered(b_unit_task='unit_task:X state:end type:ordered'):
        print 'finished unit task - ordered'
        b_unit_task.set('unit_task:X state:finished type:ordered')

    def finished_unordered(b_unit_task='unit_task:X state:end type:unordered'):
        print 'finished unit task - unordered'
        b_unit_task.set('unit_task:X state:finished type:unordered')



## cheese unit task

    def cheese_unit_task(b_unit_task='unit_task:cheese state:start type:ordered'):
        print 'start the cheese unit task'
        b_unit_task.set('unit_task:cheese state:running')
        b_method.set('method:add target:feta state:start')    
    def cheese_unit_task2(b_unit_task='unit_task:cheese state:start type:unordered'):
        print 'start the cheese unit task'
        b_unit_task.set('unit_task:cheese state:running')
        b_method.set('method:add target:feta state:start') 
    def cheese(b_unit_task='unit_task:cheese state:running',
               b_method='method:add target:feta state:finished'):
        print 'cheese method finished'
        b_unit_task.set('unit_task:cheese state:finished type:ordered')

## pickles unit task

    def pickles_unit_task(b_unit_task='unit_task:pickles state:start type:ordered'):
        print 'start the pickles unit task'
        b_unit_task.set('unit_task:pickles state:running')
        b_method.set('method:add target:green_olives state:start')  
    def green_olives(b_unit_task='unit_task:pickles state:running',
                     b_method='method:add target:green_olives state:finished'):
        print 'green_olives method finished'
        b_method.set('method:add target:black_olives state:start')       
    def black_olives(b_unit_task='unit_task:pickles state:running',
               b_method='method:add target:black_olives state:finished'):
        print 'black_olives method finished'
        b_method.set('method:add target:onion state:start')
    def onion(b_unit_task='unit_task:pickles state:running',
                 b_method='method:add target:onion state:finished'):
        print 'onion method finished'
        b_unit_task.set('unit_task:pickles state:finished type:ordered')

## spreads

    def humus_unit_task(b_unit_task='unit_task:spreads state:start type:ordered'):
        print 'start the spreads unit task'
        b_unit_task.set('unit_task:spreads state:running')
        b_method.set('method:add target:humus state:start')  
    def humus_end(b_unit_task='unit_task:spreads state:running',
                    b_method='method:add target:humus state:finished'):
        print "spreads finished"
        b_unit_task.set('unit_task:spreads state:finished type:ordered')

## sauce

    def sauce_unit_task(b_unit_task='unit_task:sauce state:start type:ordered'):
        print 'start the sauce unit task'
        b_unit_task.set('unit_task:sauce state:running')
        b_method.set('method:add target:hot_sauce state:start')  
    def sauce_end(b_unit_task='unit_task:sauce state:running',
                    b_method='method:add target:hot_sauce state:finished'):
        print "sauce finished"
        b_unit_task.set('unit_task:sauce state:finished type:ordered')
        
## check_meat

    def check_meat_unit_task(b_unit_task='unit_task:check_meat state:start'):
        print 'start the check_meat unit task'
        b_unit_task.set('unit_task:check_meat state:running')
        b_method.set('method:check target:chicken state:start')       
    def check_meat(b_unit_task='unit_task:check_meat state:running',
                   b_method='method:check target:chicken state:finished'):
        print 'chicken is checked'
        b_unit_task.set('unit_task:check_meat state:finished')

## add_meat

    def add_meat_unit_task(b_unit_task='unit_task:add_meat state:start'):
        print 'start the add_meat unit task'
        b_unit_task.set('unit_task:add_meat state:running')
        b_method.set('method:add target:chicken state:start')   
    def add_meat(b_unit_task='unit_task:add_meat state:running',
                 b_method='method:add target:chicken state:finished'):
        print 'chicken is added'
        b_unit_task.set('unit_task:add_meat state:finished')
        



############## run model ##########################################
####################################################
          
tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run()                               # run the environment
ccm.finished()                             # stop the environment
