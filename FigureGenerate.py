from FSM import *

class Figure(object):
    def __init__(self):
        self.set_figure()
    def set_figure(self,weight = 10,height = 160):
        self.weight = weight
        self.height = height
    def print_figure(self,weight,height):
        print('Current Weight: %d,Current Height: %d' % (self.weight,self.height))

record = Figure()

machine = Machine(record,states = states,transitions = transitions,initial = 'Set_service',after_state_change = ['set_figure','print_figure'])

record.get_graph().draw('State_diagram.png',prog = 'dot')
