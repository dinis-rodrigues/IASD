### Template ###

import search

def calculate_time(t):
    hours = int(t*0.01)
    minutes = abs(t - hours*100)
    print(hours, minutes)
    time_min = hours*60 + minutes
    return time_min

class Airplane():

    def __init__(self, classe=None, t_rot=None, pos=None, pos_init=None, code=None, t_arr=None, t_avail=None):
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
        
    # By doing this, when we print the object, we get all the attributes printed
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    # Auxiliary Function
    def __members(self):
        return (self.code, self.classe)
    
    # Checks the equality between two possible objects
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__members() == other.__members()
        else:
            return False
        
    # Hashes the object
    def __hash__(self):
        return hash(self.__members())
        
class Airport():

    def __init__(self, t_open=None, t_close=None, code=None):
        self.t_open = t_open
        self.t_close = t_close
        self.code = code
        
    # By doing this, when we print the object, we get all the attributes printed
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    # Auxiliary Function
    def __members(self):
        return (self.code, self.t_close)
    
    # Checks the equality between two possible objects
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__members() == other.__members()
        else:
            return False
        
    # Hashes the object
    def __hash__(self):
        return hash(self.__members())
    

class Leg():

    def __init__(self, a_dep=None, a_arr=None, dl=None, profit={}):
        # a_dep -> departure airport
        # a_arr -> arrival airport
        # dl -> leg duration
        # profit -> dictionary of all class profits
        
        self.a_dep = a_dep
        self.a_arr = a_arr
        self.dl = dl
        self.profit = profit
    
    # By doing this, when we print the object, we get all the attributes printed
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    # Auxiliary Function
    def __members(self):
        return (self.a_dep, self.dl)
    
    # Checks the equality between two possible objects
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__members() == other.__members()
        else:
            return False
        
    # Checks the equality between two possible objects
    def __hash__(self):
        return hash(self.__members())


class State():

    def __init__(self, p_list=None, l_list=None):
        # p_list -> list of all airplanes
        # l_list -> list of all legs that need to be done

        self.p_list = p_list
        self.l_list = l_list

    # By doing this, when we print the object, we get all the attributes printed
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    # Auxiliary Function
    def __members(self):
        return (self.p_list, self.l_list)
    
    # Checks the equality between two possible objects
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__members() == other.__members()
        else:
            return False
        
    # Checks the equality between two possible objects
    def __hash__(self):
        return hash(self.__members())



class ASARProblem(search.Problem):

    def __init__(self):
        self.initial = None # place here the initial state (or None)
        self.airplanes = []
        self.airports = []
        self.legs = []
        
    
    def actions(self, s):
        #s -> state
        possible_actions = []

        for leg in s.l_list:
            for plane in s.p_list:
                if plane.pos == 0: #if it's the initial state, create a list of all the initial actions
                    pass
                    # --------------------------------------
                elif (leg.a_dep.code == plane.pos) and (leg.a_arr.t_open < (plane.t_avail + leg.dl) < leg.a_arr.t_close) and (leg.a_dep.t_open < plane.t_avail < leg.a_dep.t_close):
                    possible_actions.append([plane, leg])

                    
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
    
    def save(self, fh, state):
        # note: fh is an opened file object
        # for plane in self.airplanes:
        #     if plane:
        #         pass

        pass
        
    def load(self, fh):
        # note: fh is an opened file object
        # note: self.initial may also be initialized here
        
        # Store Lines of file into a list variable lines = []
        lines=[]
        for line in fh: 
            if line == '\n':
                pass
            else:
                line = line.replace("\n", "")
                lines.append(line)
                
        # sort list to do airplanes first, then legs, then planes and finnaly classes
        sort_order = ['A', 'L', 'P', 'C'] 
        lines = [tuple for x in sort_order for tuple in lines if tuple[0] == x]
        
        # Create and store objects from the information of lines in this loop
        for line in lines:
            words = line.split() # breaks down the line into words
            # If the line is about the Airport
            if line[0] == 'A':
                try:
                    code, t_open, t_close = words[1:]
                    # create and append a new airport object into the airports list
                    self.airports.append(Airport(int(t_open), int(t_close), code))
                except:
                    print("There's a line starting with 'A' that ins't properly defined")

            # If the line is about the Leg                           
            if line[0] == 'L':
                try:
                    a_dep, a_arr, dl = words[1:4]
                    # initialize a Leg object from the first 4 key informations
                    for i in range(len(airports)):
                        if airports[i].code == a_dep:
                            air_dep=airports[i]
                        if airports[i].code == a_arr:
                            air_arr=airports[i]
                    new_leg = Leg(air_dep, air_arr, int(dl), profit={})
                    # The loop goes 2 by 2
                    for number in range(4, len(words), 2):
                        classe = words[number]
                        profit = words[number+1]
                        # Store the the class and the correspondent profit into a dict
                        new_leg.profit[classe] = int(profit)
                    # append the final object in the legs list
                    self.legs.append(new_leg)
                    new_leg = None # empty the variable for safety reasons
                except:
                    print("There's a line starting with 'L' that ins't properly defined")

            # If the line is about the Airplane
            if line[0] == 'P':
                try:
                    # Get the 2 key informations about the Plane
                    # and append the Plane in the planes list
                    code, classe = words[1:]
                    self.airplanes.append(Airplane(classe=classe, code=code))
                except:
                    print("There's a line starting with 'P' that ins't properly defined")
            
            # If the line is about the Clases
            if line[0] == 'C':
                try:
                    classe, dr = words[1:]
                    # check the class of each plane in our list
                    # and update the rotation time
                    for plane in self.airplanes:
                        if plane.classe == classe:
                            plane.t_rot = dr
                        else:
                            pass
                except:
                    print("There's a line starting with 'C' that ins't properly defined")
    

