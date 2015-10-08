__author__ = 'Robert'
import sys

#sys.path.append('/Users/robertwest/CCMSuite')

sys.path.append('C:/Users/Robert/Documents/Development/SGOMS/CCMSuite')


import ccm

log = ccm.log()

# log=ccm.log(html=True)

from ccm.lib.actr import *


# --------------- Environment ------------------

class MyEnvironment(ccm.Model):
    chicken = ccm.Model(isa='chicken', location='grill', state='cooked', salience=0.2)
    pita = ccm.Model(isa='pita', location='bins2', status='in_bag', salience=0.2)

    cheese = ccm.Model(isa='cheese', location='in_bins1', salience=0.2)
    feta = ccm.Model(isa='feta', location='in_bins1', salience=0.2)
    cucumber = ccm.Model(isa='cucumber', location='in_bins1', salience=0.2)
    green_pepper = ccm.Model(isa='green_pepper', location='in_bins1', salience=0.2)
    mushroom = ccm.Model(isa='mushroom', location='in_bins1', salience=0.2)
    lettuce = ccm.Model(isa='lettuce', location='in_bins1', salience=0.2)
    tomato = ccm.Model(isa='tomato', location='in_bins1', salience=0.2)

    green_olives = ccm.Model(isa='green_olives', location='in_bins2', salience=0.2)
    black_olives = ccm.Model(isa='black_olives', location='in_bins2', salience=0.2)
    hot_peppers = ccm.Model(isa='hot_peppers', location='in_bins2', salience=0.2)
    onion = ccm.Model(isa='onion', location='in_bins2', salience=0.2)

    humus = ccm.Model(isa='humus', location='in_bins2', salience=0.2)
    tzatziki = ccm.Model(isa='tzatziki', location='in_bins2', salience=0.2)

    hot_sauce = ccm.Model(isa='hot_sauce', location='in_bins2', salience=0.2)

    worker = ccm.Model(isa='worker', location='at_counter', salience=0.2)
    spider = ccm.Model(isa='spider', location='on_counter', feature1='yellow_stripe', salience=0.99)
    red_wire = ccm.Model(isa='wire', state='uncut', color='red', salience=0.99)
    blue_wire = ccm.Model(isa='wire', state='uncut', color='blue', salience=0.99)
    green_wire = ccm.Model(isa='wire', state='uncut', color='green', salience=0.99)


    motor_finst = ccm.Model(isa='motor_finst', state='re_set')


class MotorModule(ccm.Model):  ### defines actions on the environment

    def change_location(self, env_object, slot_value):
        yield 2
        x = eval('self.parent.parent.' + env_object)
        x.location = slot_value
        print env_object
        print slot_value
        self.parent.parent.motor_finst.state = 'finished'
    def cut_wire(self, env_object, slot_value):
        yield 2
        x = eval('self.parent.parent.' + env_object)
        x.state = slot_value
        print env_object
        print slot_value
        self.parent.parent.motor_finst.state = 'finished'
    def motor_finst_reset(self):
        self.parent.parent.motor_finst.state = 're_set'


class MethodModule(ccm.ProductionSystem):  # creates an extra production system for the motor system
    production_time = 0.04


    # adding method


    def do_add(b_method='method:add target:?target state:start'):  # target is the chunk to be altered
        motor.change_location(target, "in_wrap")
        b_method.set('method:add target:?target state:running')
        print 'target object = ', target

    def cut_wire(b_method='method:cut target:?target state:start'):  # target is the chunk to be altered
        motor.cut_wire(target, "cut")
        b_method.set('method:add target:?target state:running')
        print 'target object = ', target

    def done_method(b_method='method:?method target:?target state:running',
                    motor_finst='state:finished'):
        b_method.set('method:?method target:?target state:finished')
        motor.motor_finst_reset()
        print 'finished method =***********************************************', target

    #def done_add(b_method='method:add target:?target state:running', this is done method for a specific method
    #             motor_finst='state:finished'):                      dont think we need this
    #    b_method.set('method:add target:?target state:finished')
    #    motor.motor_finst_reset()
    #    print 'finished==================================================', target





#############################################




# --------------- Vision le ------------------

class VisionModule(ccm.ProductionSystem):
    production_time = 0.045


#
# --------------- Emotion Module ------------------

class EmotionalModule(ccm.ProductionSystem):
    production_time = 0.043


# --------------- Agent ------------------

class MyAgent(ACTR):
    ########### create agent architecture ################################################
    #############################################################

    # module buffers
    b_system = Buffer()  # create system buffers
    b_DM = Buffer()
    b_motor = Buffer
    b_visual = Buffer()
    b_image = Buffer()
    b_focus = Buffer()

    # goal buffers
    b_context = Buffer()
    b_plan_unit = Buffer()  # create buffers to represent the goal module
    b_unit_task = Buffer()
    b_method = Buffer()
    b_operator = Buffer()
    b_emotion = Buffer()

    # associative memory
    DM = Memory(b_DM)  # create the DM memory module

    # perceptual motor module
    vision_module = SOSVision(b_visual, delay=0)  # create the vision module
    motor = MotorModule(b_motor)  # put motor production module into the agent

    # auxillary production modules
    Methods = MethodModule(b_method)  # put methods production module into the agent
    Eproduction = EmotionalModule(b_emotion)  # put the Emotion production module into the agent
    p_vision = VisionModule(b_visual)

    ############ add planning units to declarative memory and set context buffer ###############

    def init():
        DM.add('planning_unit:XY         cuelag:none          cue:start          unit_task:X')
        DM.add('planning_unit:XY         cuelag:start         cue:X              unit_task:Y')
        DM.add('planning_unit:XY         cuelag:X             cue:Y              unit_task:finished')
        b_context.set('finshed:nothing status:unoccupied')

    ########### create productions for choosing planning units ###########

    ## these productions are the highest level of SGOMS and fire off the context buffer
    ## they can take any ACT-R form (one production or more) but must eventually call a planning unit and update the context buffer

    def run_sequence(
            b_context='finshed:nothing status:unoccupied'):  # status:unoccupied triggers the selection of a planning unit
        b_plan_unit.set(
            'planning_unit:XY cuelag:none cue:start unit_task:X state:begin_sequence')  # state: can be begin_situated or begin_sequence
        b_context.set('finished:nothing status:occupied')  # update context status to occupied
        print 'sequence planning unit is chosen'

    def run_situated(
            b_context='finshed:nothing status:occupied'):  # status:unoccupied triggers the selection of a planning unit
        b_plan_unit.set(
            'planning_unit:XY cuelag:none cue:start unit_task:X state:begin_situated')  # state: can be begin_situated or begin_sequence
        b_context.set('finished:nothing status:occupied')  # update context status to occupied
        print 'unordered planning unit is chosen'

    ########## unit task set up ###########

    ## these set up whether it will be an ordered or a situated planning unit

    def setup_situated_planning_unit(
            b_plan_unit='planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:begin_situated'):
        b_unit_task.set('state:start type:unordered')
        b_plan_unit.set(
            'planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running')  # next unit task
        print 'begin situated planning unit = ', planning_unit

    def setup_ordered_planning_unit(
            b_plan_unit='planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:begin_sequence'):
        b_unit_task.set('unit_task:?unit_task state:start type:ordered')
        b_plan_unit.set(
            'planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running')  # next unit task
        print 'begin orderdered planning unit = ', planning_unit

    ## these manage the sequence

    def request_next_unit_task(
            b_plan_unit='planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running',
            b_unit_task='unit_task:?unit_task state:finished type:ordered'):
        DM.request('planning_unit:?planning_unit cue:?unit_task unit_task:? cuelag:?cue')
        b_plan_unit.set(
            'planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:retrieve')  # next unit task
        print 'finished unit task = ', unit_task

    def retrieve_next_unit_task(b_plan_unit='state:retrieve',
                                b_DM='planning_unit:?planning_unit cuelag:?cuelag cue:?cue!finished unit_task:?unit_task'):
        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running')
        b_unit_task.set('unit_task:?unit_task state:start type:ordered')
        print 'unit_task = ', unit_task

    def last_unit_task(b_plan_unit='planning_unit:?planning_unit',
                       b_unit_task='unit_task:finished state:start type:ordered'):
        print 'finished planning unit=', planning_unit
        b_unit_task.set('stop')
        b_context.set('finished:?planning_unit status:unoccupied')

    ################# unit tasks #################

    ## X unit task

    ## these decide if the unit task will be run as part of a sequence of unit tasks 'ordered'
    ## OR as situated unit tasks determined by the environment 'unordered'
    def X_unit_task_unordered(b_unit_task='state:start type:unordered'):
        b_unit_task.set('unit_task:X state:begin type:unordered')
        print 'start unit task X unordered'

    def X_unit_task_ordered(b_unit_task='unit_task:X state:start type:ordered'):
        b_unit_task.set('unit_task:X state:begin type:ordered')
        print 'start unit task X ordered'

    ## the first production in the unit task must begin in this way
    def X_start_unit_task(b_unit_task='unit_task:X state:begin type:?type'):
        b_unit_task.set('unit_task:X state:running type:?type')
        b_focus.set('method1')
        print 'start unit task X'

    ## body of the unit task
    def X1(b_unit_task='unit_task:X state:running type:?type', b_focus='method1'):
        b_focus.set('method2')
        print 'method 1 in unit task X done'

    def X2(b_unit_task='unit_task:X state:running type:?type', b_focus='method2'):
        b_method.set('method:cut target:red_wire state:start')
        b_focus.set('done')
        b_unit_task.set('unit_task:X state:end type:?type')  ## this line ends the unit task
        print 'method 2 in unit task X done'

    ## finishing the unit task
    def finished_ordered(b_method='state:finished', b_unit_task='unit_task:X state:end type:ordered'):
        print 'finished unit task X - ordered'
        b_unit_task.set('unit_task:X state:finished type:ordered')

    def finished_unordered(b_unit_task='unit_task:X state:end type:unordered'):
        print 'finished unit task X - unordered'
        b_unit_task.set('unit_task:X state:finished type:unordered')

    ## Y unit task

    ## these decide if the unit task will be run as part of a sequence of unit tasks 'ordered'
    ## OR as situated unit tasks determined by the environment 'unordered'
    def Y_unit_task_unordered(b_unit_task='state:start type:unordered'):
        b_unit_task.set('unit_task:Y state:begin type:unordered')
        print 'start unit task Y unordered'

    def Y_unit_task_ordered(b_unit_task='unit_task:Y state:start type:ordered'):
        b_unit_task.set('unit_task:Y state:begin type:ordered')
        print 'start unit task Y ordered'

    ## the first production in the unit task must begin in this way
    def Y_start_unit_task(b_unit_task='unit_task:Y state:begin type:?type'):
        b_unit_task.set('unit_task:Y state:running type:?type')
        ## then anything can be added
        b_method.set('method:add target:tomato state:start')
        b_focus.set('')
        print 'start unit task Y'

    ## body of the unit task
    def ytomato(b_unit_task='unit_task:Y state:running type:?type',  ## this line stays the same
                b_method='method:add target:tomato state:finished'):  ## the rest can be anything
        print 'tomato Y method finished'
        b_method.set('method:add target:cucumber state:start')

    def ycucumber(b_unit_task='unit_task:Y state:running type:?type',  ## same
                  b_method='method:add target:cucumber state:finished'):  ## anything
        print 'cucumber Y method finished'
        b_method.set('method:add target:green_pepper state:start')

    def ygreen_pepper(b_unit_task='unit_task:Y state:running type:?type',  ## same
                      b_method='method:add target:green_pepper state:finished'):  ## anything
        b_unit_task.set('unit_task:Y state:end type:?type')  ## this line ends the unit task
        print 'green_pepper Y method finished'

    ## finishing the unit task
    def Y_finished_ordered(b_unit_task='unit_task:Y state:end type:ordered'):
        print 'finished unit task Y - ordered'
        b_unit_task.set('unit_task:Y state:finished type:ordered')

    def Y_finished_unordered(b_unit_task='unit_task:Y state:end type:unordered'):
        print 'finished unit task Y - unordered'
        b_unit_task.set('unit_task:Y state:finished type:unordered')


############## run model #############

tim = MyAgent()  # name the agent
subway = MyEnvironment()  # name the environment
subway.agent = tim  # put the agent in the environment
ccm.log_everything(subway)  # print out what happens in the environment
subway.run()  # run the environment
ccm.finished()  # stop the environment
