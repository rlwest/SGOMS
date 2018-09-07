## The Faulty Warning Light Simulation


# this model shows the use of ordered and situated planning units
## an ordered planning unit is based on a stored plan to execute unit tasks in a specific order
## a situated planning unit is a set of unit tasks that fire based on the buffer conditions

# it also shows the planning unit interupt
## this occurs when an event renders a planning unit problematic
## then the current unit task is finished and the planning unit is ended
## interupt is the only way to get out of a situated planning unit
## it will also end an ordered planning unit
### ordered planning units also end when they are completed

# the task
## the agent must setup the task by doing unit task x first
## then unit task Y
## this is done wih an ordered planning unit
## after the setup the agent must randomly do unit task x or y continuosly
## this is done with a situated planning unit
## if the warning light goes off the agent must stop whatever planning unit they are in
## and restart by turing off the light and setting up the task again
## it is assumed that the light is faulty and the warnings are false

## to simplify the code, all actions are assumed to be done instantiously
## also to simplify the code, the model is set to be instantly aware of all enviornmental changes
## the waring light comes on randomly



import sys

sys.path.append('/Users/robertwest/CCMSuite')
#sys.path.append('C:/Users/Robert/Documents/Development/SGOMS/CCMSuite')
import ccm
from random import randrange, uniform
log = ccm.log()
# log=ccm.log(html=True)
from ccm.lib.actr import *




class MyEnvironment(ccm.Model):
    
    warning_light = ccm.Model(isa='warning_light', state='off')




class MotorModule(ccm.Model):
    
    def maybe_change_light(self):
        irand = randrange(0, 10) # adjust warning light probability here
        if irand < 1: 
           print ' light on ++++++++++++++++++++++++++++++++++++++++++++++++++++'
           print irand
           self.parent.parent.warning_light.state='on'         

    def turn_off_light(self):
        self.parent.parent.warning_light.state='off'
        print 'light off ------------------------------------------------------'


class MyDmModule(ccm.ProductionSystem):   # create production system
    production_time=0.040
    
    def Dream(EM='busy:False'):
        EM.request('dream:?dream')
        print "day dreaming"
##    def Dream_retrieve(b_EM='dream:?dream'): no need to retrieve, it gets put in the buffer
##        print "dreaming about"
##        print dream


class EmotionalModule(ccm.ProductionSystem):
    production_time = 0.043

    def warning_light(b_emotion='interupt:ok',warning_light='state:on'):
        print "warning light is on^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
        b_emotion.set('interupt:pu')

    def warning_thought(b_emotion='interupt:ok',b_EM='dream:cuba'):
        print "Cuba is communist!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        b_emotion.set('interupt:pu')



       
class Environment_Manager(ACTR): # this agent triggers the warning light

    b_focus = Buffer()
    motor = MotorModule()

    def init():
        b_focus.set('set_warning')

    def environment(b_focus='set_warning'):
        motor.maybe_change_light()




class MyAgent(ACTR): # this is the agent that does the task

    # module buffers
    b_DM = Buffer()
    b_EM = Buffer()
    
    b_motor = Buffer()
    b_focus = Buffer()

    # goal buffers
    b_context = Buffer()
    b_plan_unit = Buffer() 
    b_unit_task = Buffer()
    b_method = Buffer()
    b_operator = Buffer()
    b_emotion = Buffer()

    DM = Memory(b_DM)
    EM = Memory(b_EM)  

    motor = MotorModule(b_motor)
    Emotion = EmotionalModule(b_emotion)
    DM_productions = MyDmModule()



    def init():
        DM.add('planning_unit:XY         cuelag:none          cue:start          unit_task:X')
        DM.add('planning_unit:XY         cuelag:start         cue:X              unit_task:Y')
        DM.add('planning_unit:XY         cuelag:X             cue:Y              unit_task:finished')

        EM.add('dream:cuba')
        EM.add('dream:hawaii')
        EM.add('dream:fiji')
        EM.add('dream:japan')
##        EM.add('dream:bali')
##        EM.add('dream:hawaii2')
##        EM.add('dream:fiji2')
##        EM.add('dream:japan2')
##        EM.add('dream:bali2')
##        EM.add('dream:hawaii2a')
##        EM.add('dream:fiji2a')
##        EM.add('dream:japan2a')
##        EM.add('dream:bali2a')
        
        b_context.set('finshed:nothing status:unoccupied warning_light:off')
        b_emotion.set('interupt:ok')
        b_focus.set('none')



    
########################### begin the planning unit

# these productions are the highest level of SGOMS and fire off the context buffer
# the decision process can be as complex as needed
# the simplest way is to have a production for each planning unit (as in this case)
# the first unit task in the planning unit is directly triggered from here

    def run_sequenceXY(b_context='finshed:nothing status:unoccupied'):        
        b_unit_task.set('unit_task:X state:running pu_type:ordered')
        b_plan_unit.set('planning_unit:XY cuelag:none cue:start unit_task:X state:running')
        b_context.set('finished:nothing status:occupied')
        print 'ordered planning unit is chosen OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'

    def run_situatedXY(b_context='finshed:XY status:unoccupied'): 
        b_unit_task.set('unit_task:situated state:find_match pu_type:situated')
        b_plan_unit.set('planning_unit:XY state:running')
        b_context.set('finished:XY status:occupied') 
        print 'begin situated planning unit SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS'

    def false_alarm(b_context='finshed:?finished status:interupted', b_EM='dream:!cuba'):
        motor.turn_off_light() # change planning unit
        b_emotion.set('interupt:ok')
        b_unit_task.set('unit_task:X state:running pu_type:ordered')
        b_plan_unit.set('planning_unit:XY cuelag:none cue:start unit_task:X state:running')
        b_context.set('finished:nothing status:occupied')
        print 'ordered planning unit is chosen OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'

    def false_cuba(b_context='finshed:?finished status:interupted', b_EM='dream:cuba'):
        b_unit_task.set('unit_task:situated state:find_match pu_type:situated')
        b_plan_unit.set('planning_unit:XY state:running') # start situated planning unit
        b_context.set('finished:XY status:occupied')
        print 'cuba is OK, resume task'
        print 'begin situated planning unit SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS'

######################### planning unit management loop
# these are generic productions for managing the execution of planning units

######## get next unit task and save a memory of the completed unit task

# the first unit task in a planning unit is triggered when the planning unit is chosen
# these porductions fire within planning units to get the next unit task
# to trigger the next unit task the unit_task state slot value is switched from 'end' to 'begin'
# this is also where the successful completion of the last unit task is saved to memory
## the memory save is often not needed in simple models and is not implemented here
### although, in theory, the memory save always happens so this step should always be included


# ordered planning units

## retrieve next unit task
    def request_next_unit_task(b_plan_unit='planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running',
                               b_unit_task='unit_task:?unit_task state:end pu_type:ordered',
                               b_emotion='interupt:ok'):
        DM.request('planning_unit:?planning_unit cue:?unit_task unit_task:? cuelag:?cue')
        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:retrieve')  # next unit task
        print 'finished unit task = ', unit_task
        # save completed unit task here
    def retrieved_next_unit_task(b_plan_unit='state:retrieve',
                                 b_DM='planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task!finished'):
        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running')
        b_unit_task.set('unit_task:?unit_task state:running pu_type:ordered')
        print 'next unit_task = ', unit_task
        print 'ordered'


# situated planning units

## allow the next unit task to fire
    def next_situated_unit_task(b_unit_task='unit_task:?unit_task state:end pu_type:situated',
                                b_emotion='interupt:ok'):
        b_unit_task.modify(state='find_match') 
        print 'next situated unit task'
        print 'situated'
        # save unit task here



########### end the planning unit and save a memory of it
        
# a planning unit can be thought of as a loop
# these are the exit conditions
# in these the planning unit should be saved
# although, to keep the code simple, this is not done here

## finished ordered planning unit
    def retrieved_last_unit_task(b_plan_unit='planning_unit:?planning_unit state:retrieve',
                                 b_unit_task='unit_task:?unit_task state:end pu_type:ordered',
                                 b_emotion='interupt:ok',
                                 b_DM='planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:finished'):
                                    # not, the memory retrieval indicates the plan is finished
        print 'stopped planning unit=',planning_unit
        print 'finished'
        b_unit_task.modify(state='stopped') 
        b_context.set('finshed:?planning_unit status:unoccupied')
        # save completed planning unit here



    def interupted_planning_unit(b_plan_unit='planning_unit:?planning_unit',
                                 b_unit_task='unit_task:?unit_task state:end pu_type:?pu_type',
                                 b_emotion='interupt:pu'):
        print 'stopped planning unit='
        print 'interupted IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII'
        b_unit_task.modify(state='stopped') 
        b_context.set('finshed:?planning_unit status:interupted')
        # save planning unit book mark here





####################################### unit tasks
# these are the unit task, they are specific to the task


# X unit task

## situated matching productions
### these productions match the unit task to situations for situated planning units
### there can be more than one allowing the unit task to be used in different situations
### an ordered planning unit will skip this step because the plan specifies the unit task
### in this model the details of the matching conditions are not specified
### so for situated planning units it is random whether unit task a or y is chosen

    def X_start_unit_task_situated(b_unit_task='unit_task:? state:find_match pu_type:situated'):
        b_unit_task.modify(unit_task='X', state='running')
        print 'starting unit task X situated'
        
## body of the unit task
### this is the actions of the unit task

    def X_part1(b_unit_task='unit_task:X state:running',
                b_focus='none'):
        b_focus.set('part1')
        print 'doing part 1 of unit task X'

    def X_part2(b_unit_task='unit_task:X state:running',
                b_focus='part1'):
        b_focus.set('none')
        b_unit_task.modify(state='end')  ## this line ends the unit task
        print 'doing part 2 of unit task X'


# Y unit task

## situated matching productions

    def Y_start_unit_task_situated(b_unit_task='state:find_match pu_type:situated'):
        b_unit_task.set('unit_task:Y state:running pu_type:situated')
        print 'start unit task Y'

## body of the unit task
        
    def Y_part1(b_unit_task='unit_task:Y state:running',
                b_focus='none'):
        b_focus.set('part1')
        print 'doing part 1 of unit task Y'

    def Y_part2(b_unit_task='unit_task:Y state:running',
                b_focus='part1'):
        b_focus.set('none')
        b_unit_task.modify(state='end')  ## this line ends the unit task
        print 'doing part 2 of unit task Y'
    






############## run model #############
        
jim = Environment_Manager()
tim = MyAgent()  # name the agent
subway = MyEnvironment()  # name the environment
subway.agent = tim  # put the agent in the environment
subway.agent = jim  # put the agent in the environment

ccm.log_everything(subway)  # print out what happens in the environment
subway.run()  # run the environment
ccm.finished()  # stop the environment
