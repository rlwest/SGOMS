#################### SGOMS ###################


import sys
import os
sys.path.append(os.getcwd()+'/CCMsuite/')

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



# --------------- Motor Module ------------------


##In Python ACT-R motor actions are carried out by producitons in the motor module
##Consistent with ACT-R theory, this module has a finst which represents the state of
##the module. From a GOMS perspective the motor module executes operators






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






        
        

# --------------- Motor Methods Module ------------------

##the motor methods module contains GOMS methods. These are sets of operators that are
##frequently re-used (e.g., move hand to mouse, saccade to target icon, move cursor to
##target, double click)

##placing these in a sepperate production system represents a theoretical claim that these
##types of highly practiced, low level, quick sequences are executed by the motor system
##and not controled by the procedural system. In terms of ACT-R theory, sequences
##get learned in the procedural system through compilation. We are not contradicting
##that but are adding the idea that low level, quick sequences are taken over by the
##motor system once they are highly practiced.

##In fact, most experiments on sequence
##learning or low level dual tasking and most ACT-R models of these have the grain size
##for actions triggered by the procedural system set at the level of a goms method
##and not a goms operator. So doing it this way would add more low level detail but
##would not alter the result

##this issue needs to be decided empirically. For now we feel justified as it seems
##to be needed for to account for ongoing multi tasking such as driving or flying








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


##this module implements bottom up vision. essential for noticing unexpected things











    

# --------------- Emotion Module ------------------

class EmotionalModule(ccm.ProductionSystem):  
    production_time=0.043



##we argue that this module is essential for bottom up interuptions








# --------------- DM module ------------------




##this module implements bottom up memory
##e.g., when something in the environment reminds of something important
##needed for situated action models







 


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



########### create productions for choosing planning units #####################################
#########################################################################



        

##this one fires when nothing has been done yet
    def prep_wrap(b_context='finshed:nothing status:unoccupied'): # status:unoccupied triggers the selection of a planning unit
         b_plan_unit.set('planning_unit:prep_wrap cuelag:none cue:start unit_task:veggies state:begin') # which planning unit and where to start
         #b_unit_task.set('unit_task:veggies state:start') # ******** there is always a unit task that has just finished before another can start
         b_context.set('finished:nothing status:occupied') # update context status to occupied
         print 'prep the wrap planning unit is chosen'
##this one fires on the condition that any other planning unit has been completed
    def get_meat(b_context='finished:prep_wrap status:unoccupied'):
         b_plan_unit.set('planning_unit:meat cuelag:none cue:start unit_task:check_meat state:running')
         b_unit_task.set('unit_task:check_meat state:start')
         b_context.set('finished:prep_wrap status:occupied')
         print 'get the meat'

         


############ add planning units to declarative memory and set context buffer ###############
#########################################################################
    
    def init():                                             

        DM.add ('planning_unit:prep_wrap    cuelag:none          cue:start          unit_task:veggies')                     
        DM.add ('planning_unit:prep_wrap    cuelag:start         cue:veggies        unit_task:cheese')
        DM.add ('planning_unit:prep_wrap    cuelag:veggies       cue:cheese         unit_task:pickles')       
        DM.add ('planning_unit:prep_wrap    cuelag:cheese        cue:pickles        unit_task:spreads')
        DM.add ('planning_unit:prep_wrap    cuelag:pickles       cue:spreads        unit_task:sauce')
        DM.add ('planning_unit:prep_wrap    cuelag:spreads       cue:sauce          unit_task:finished')

        DM.add ('planning_unit:meat         cuelag:none          cue:start          unit_task:check_meat')                     
        DM.add ('planning_unit:meat         cuelag:start         cue:check_meat     unit_task:add_meat')
        DM.add ('planning_unit:meat         cuelag:check_meat    cue:add_meat       unit_task:finished')       


        b_context.set('finshed:nothing status:unoccupied')




########## cycle for unit task retrieval #############################################
#########################################################################

##This cycle is fixed for all SGOMS models. It is not task dependent

    def request_first_unit_task(b_plan_unit='planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:begin'): 
        b_unit_task.set('unit_task:?unit_task state:start')
        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running') # next unit task     

        print 'begin with unit task = ',unit_task

    def request_next_unit_task(b_plan_unit='planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running',                   
                               b_unit_task='unit_task:?unit_task state:finished'): 
        DM.request('planning_unit:?planning_unit cue:?unit_task unit_task:? cuelag:?cue')                 
        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:retrieve') # next unit task     
        print 'finished unit task = ',unit_task
        
    def retrieve_next_unit_task(b_plan_unit='state:retrieve',
                                b_DM='planning_unit:?planning_unit cuelag:?cuelag cue:?cue!finished unit_task:?unit_task'): 
        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running')
        b_unit_task.set('unit_task:?unit_task state:start')
        print 'unit_task = ',unit_task

    def last_unit_task(b_plan_unit='planning_unit:?planning_unit',
                       b_unit_task='unit_task:finished state:start'):
        print 'finished planning unit=',planning_unit
        b_unit_task.set('stop')
        b_context.set('finished:?planning_unit status:unoccupied')




################# unit tasks ######################################################
######################################################################
        


## veggies unit task

    def vegg_unit_task(b_unit_task='unit_task:veggies state:start'):
        print 'start the veggies unit task'
        b_unit_task.set('unit_task:veggies state:running')
        b_method.set('method:add target:lettuce state:start')  
    def lettuce(b_unit_task='unit_task:veggies state:running',
                b_method='method:add target:lettuce state:finished'):
        print 'lettuce method finished'
        b_method.set('method:add target:tomato state:start')        
    def tomato(b_unit_task='unit_task:veggies state:running',
               b_method='method:add target:tomato state:finished'):
        print 'tomato method finished'
        b_method.set('method:add target:cucumber state:start')
    def cucumber(b_unit_task='unit_task:veggies state:running',
                 b_method='method:add target:cucumber state:finished'):
        print 'cucumber method finished'
        b_method.set('method:add target:green_pepper state:start')
    def green_pepper(b_unit_task='unit_task:veggies state:running',
                     b_method='method:add target:green_pepper state:finished'):
        print 'green_pepper method finished'
        b_method.set('method:add target:mushroom state:start')
    def mushroom(b_unit_task='unit_task:veggies state:running',
                 b_method='method:add target:mushroom state:finished'):
        print 'mushroom method finished'
        b_unit_task.set('unit_task:veggies state:finished')   
        
## cheese unit task

    def cheese_unit_task(b_unit_task='unit_task:cheese state:start'):
        print 'start the cheese unit task'
        b_unit_task.set('unit_task:cheese state:running')
        b_method.set('method:add target:feta state:start')       
    def cheese(b_unit_task='unit_task:cheese state:running',
               b_method='method:add target:feta state:finished'):
        print 'cheese method finished'
        b_unit_task.set('unit_task:cheese state:finished')

## pickles unit task

    def pickles_unit_task(b_unit_task='unit_task:pickles state:start'):
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
        b_unit_task.set('unit_task:pickles state:finished')

## spreads

    def humus_unit_task(b_unit_task='unit_task:spreads state:start'):
        print 'start the spreads unit task'
        b_unit_task.set('unit_task:spreads state:running')
        b_method.set('method:add target:humus state:start')  
    def humus_end(b_unit_task='unit_task:spreads state:running',
                    b_method='method:add target:humus state:finished'):
        print "spreads finished"
        b_unit_task.set('unit_task:spreads state:finished')

## sauce

    def sauce_unit_task(b_unit_task='unit_task:sauce state:start'):
        print 'start the sauce unit task'
        b_unit_task.set('unit_task:sauce state:running')
        b_method.set('method:add target:hot_sauce state:start')  
    def sauce_end(b_unit_task='unit_task:sauce state:running',
                    b_method='method:add target:hot_sauce state:finished'):
        print "sauce finished"
        b_unit_task.set('unit_task:sauce state:finished')
        
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
