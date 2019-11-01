### Template ###

import search

class Airplane():

    def __init__(self, classe, t_rot, pos, pos_init, code, t_arr, t_avail):
        # t_rot -> rotation time
        # pos -> plane position (airport)
        # pos_init -> first plane position (airport)
        # code -> plane code
        # t_arr -> arrival time
        # t_avail -> time at which the plane is available for departure

        self.classe = classe
        self.t_rot = t_rot
        self.pos = pos
        self.pos_init = pos_init
        self.code = code
        self.t_arr = t_arr
        self.t_avail = t_avail

class Airport():

    def __init__(self, t_open, t_close, code):
        self.t_open = t_open
        self.t_close = t_close
        self.code = code

class Leg():

    def __init__(self, a_dep, a_arr, dl, profit):
        # a_dep -> departure airport
        # a_arr -> arrival airport
        # dl -> leg duration
        # profit -> dictionary of all class profits
        
        self.a_dep = a_dep
        self.a_arr = a_arr
        self.dl = dl
        self.profit = profit


class State():

    def __init__(self, p_list, l_list):
        # p_list -> list of all airplanes
        # l_list -> list of all legs that need to be done

        self.p_list = p_list
        self.l_list = l_list




class ASARProblem(search.Problem):

    def __init__(self):
        self.initial = # place here the initial state (or None)
    
    def actions(self, s):
        #s -> state
        for leg in s.l_list:
            for plane in s.p_list:
                if plane.

        pass

    def result(self, state, action):
        pass
        
    def goal_test(self, state):
        pass
        
    def path_cost(self, c, state1, action, state2):
        pass
        
    def heuristic(self, node):
        # note: use node.state to access the state
        pass
        
    def load(self, fh):
        # note: fh is an opened file object
        # note: self.initial may also be initialized here
        pass
    
    def save(self, fh, state):
        # note: fh is an opened file object
        pass
