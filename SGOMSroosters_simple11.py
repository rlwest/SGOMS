
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













############ add planning units to declarative memory and set context buffer ###############
#########################################################################
    
    def init():                                             

        DM.add ('planning_unit:prep_wrap    cuelag:none          cue:start          unit_task:veggies      type:ordered')                     
        DM.add ('planning_unit:prep_wrap    cuelag:start         cue:veggies        unit_task:cheese       type:ordered')
        DM.add ('planning_unit:prep_wrap    cuelag:veggies       cue:cheese         unit_task:pickles      type:ordered')       
        DM.add ('planning_unit:prep_wrap    cuelag:cheese        cue:pickles        unit_task:spreads      type:ordered')
        DM.add ('planning_unit:prep_wrap    cuelag:pickles       cue:spreads        unit_task:sauce        type:ordered')
        DM.add ('planning_unit:prep_wrap    cuelag:spreads       cue:sauce          unit_task:finished     type:ordered')

        DM.add ('planning_unit:meat         type:unordered')                     
        #DM.add ('planning_unit:meat         cuelag:start         cue:check_meat     unit_task:add_meat     type:unordered')
        #DM.add ('planninzg_unit:meat         cuelag:check_meat    cue:add_meat       unit_task:finished     type:unordered')       


        b_context.set('finshed:nothing status:unoccupied')














########### create productions for choosing planning units #####################################
#########################################################################

##These productions fire when the agent has finished a planning unit
##and is unoccupied. These examples are very simple, using single productions
##to match to the context buffer. This type of decision would be very fast
##and automatic

        

##this one fires when nothing has been done yet
    def prep_wrap(b_context='finshed:nothing status:unoccupied'): # status:unoccupied triggers the selection of a planning unit
         b_plan_unit.set('planning_unit:prep_wrap cuelag:none cue:start unit_task:veggies state:running') # which planning unit and where to start
         b_unit_task.set('unit_task:veggies state:finished') # there is always a unit task that has just finished before another can start
         b_context.set('finished:nothing status:occupied') # update context status to occupied
         print 'prep the wrap'
## making meat into an unordered planning unit
    def get_meat(b_context='finished:prep_wrap status:unoccupied'):
         b_plan_unit.set('planning_unit:meat  state:running')
         b_unit_task.set('unit_task:check_meat state:finished')
         b_context.set('finished:prep_wrap status:occupied')
         print 'get the meat'

         


##need models of more complex thinking that would involve DM retrievals and logical
##inference and heuristics and further checking and discussion. According to SGOMS
##theory, the method for choosing the next planning unit will be task dependent and
##may be a source of significant individual differences

##need routines for dealing with planning units that have been interupted





########## cycle for ordered unit task retrieval #############################################
#########################################################################

##This cycle is fixed for all SGOMS models. It is not task dependent
   

    def request_next_unit_task(b_plan_unit='planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running',                   
                               b_unit_task='unit_task:?unit_task state:finished'):
        # plan_unit state:running means the planning unit has been set running
        # unit_task unit_taks:?unit_task makes sure unit task matches the unit task in the planning unit buffer (may not be necessary)
        # state:finished means the unit task is completed
        DM.request('planning_unit:?planning_unit cue:?unit_task unit_task:? cuelag:?cue')
        #request the next unit task using the previous one as the cue and the previous cue as the cue lag
        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:retrieve')
        # update the planning unit buffer and set status to retrieve    
        print 'finished unit task = ',unit_task
        
        
    def retrieve_next_unit_task(b_plan_unit='state:retrieve',
                                b_DM='planning_unit:?planning_unit cuelag:?cuelag cue:?cue!finished unit_task:?unit_task'):
        # retrieve next unit task in the planning unit
        # update the planning unit buffer to state:running
        # put the unit task in the unit task buffer with state:start

        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running')
        b_unit_task.set('unit_task:?unit_task state:start')
        print 'unit_task = ',unit_task

    def last_unit_task(b_plan_unit='planning_unit:?planning_unit',
                       b_unit_task='unit_task:finished'):
        # all planning units end with a unit task called finished
        b_unit_task.set('stop')
        b_context.set('finished:?planning_unit status:unoccupied')
        print 'finished planning unit=',planning_unit
        # this production updates the buffers and takes you out of the loop
        # a new planning unit must be chosen












################# unit tasks ######################################################
######################################################################
        

##the unit task models are expert system models for completing a distinct
##island of work. Unit tasks are assumed to have been created during learning
##and/or training and they represent islands of work that avoid overload, downtime
##and interuptions. According to rational analysis we expect few or no individual
##differences in unit tasks. In SGOMS, individual differences are assumed to occur
##when switching planning units and possibly, sometimes, within planning units
##an example of a difference within planning units would be the florida garbage men
##essentially, this would occur if someone has worked out a better way of doing
##the task but it has not been diseminated to other workers

##Unit tasks are not tied to specific planning units, they can
##be re-used. Likewise, methods in the motor module can be re-used
##by productions in any unit task. However, currently, productions in
##the procedural module cannot be re-used, that is, each unit task has
##its own productions and they are not shared. If a set of actions is re-occuring
##accross different unit tasks then the current view is that that set of actions
##should be a seperate unit task so that re-use can occur through the planning unit

##the simplest type of unit task is just a chain of productions with no decision points.
##In ACT-R these productions would be considered to be "complied." From ACT-R theory,
##compilation only occurs if a set of actions is frequently repeated in the same order.
##Also, the longer the sequence the harder it is to compile it so, in theory, we would
##expect to see more shorter sequences and fewer longer sequences done in this way. SGOMS
##has not yet been developed to the level of modeling the learning of a task so compiled
##sequences are coded in by the programmer with the goal of creating them where the
##theory suggests they should be



## veggies unit task - this is a strictly ordered task

# start the unit task
    def vegg_unit_task(b_unit_task='unit_task:veggies state:start'):
        print 'start the veggies unit task'
        b_unit_task.set('unit_task:veggies state:running')
        b_method.set('method:add target:lettuce state:start')
# do the unit task - in this case these productions call methods in a fixed order
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


        
## cheese unit task - this is a unit task that randomly chooses a method

# start the unit task
    def cheese_unit_task(b_unit_task='unit_task:cheese state:start'):
        print 'start the cheese unit task'
        b_unit_task.set('unit_task:cheese state:running')
        b_method.set('method:add target:feta state:start')
# do the unit task - in this case a method is chosen randomly
    def cheddercheese(b_unit_task='unit_task:cheese state:running',
                      b_method='method:add target:feta state:finished'):
        print 'chedder cheese method finished*************************************************'
        b_unit_task.set('unit_task:cheese state:finished')
    def fetacheese(b_unit_task='unit_task:cheese state:running',
                   b_method='method:add target:feta state:finished'):
        print 'feta cheese method finished **************************************************'
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
