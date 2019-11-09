### Template ###

import search
import copy

def calculate_time(t):
    if t < 100:
        minutes = t
        time_min = minutes
    else:
        hours = int(t*0.01)
        minutes = abs(t - hours*100)
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

    def __init__(self, a_dep=None, a_arr=None, dl=None, profit={}, flight=None, done=False):
        # a_dep -> departure airport
        # a_arr -> arrival airport
        # dl -> leg duration
        # profit -> dictionary of all class profits
        # flight -> [plane that flew, time of departure of that plane, profit of that flight]
        # done -> True if the leg was already done, False otherwise

        self.a_dep = a_dep
        self.a_arr = a_arr
        self.dl = dl
        self.profit = profit
        self.flight = flight
        self.done = done
    
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

    def __init__(self, p_list=None, l_list=None, p_cost=0):
        # p_list -> list of all airplanes
        # l_list -> list of all legs that need to be done
        # p_cost -> cost of the path taken so far

        self.p_list = p_list
        self.l_list = l_list
        self.p_cost = p_cost

    # By doing this, when we print the object, we get all the attributes printed
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    # Auxiliary Function
    def __members(self):
        return (tuple(self.p_list), tuple(self.l_list))
    
    # Checks the equality between two possible objects
    def __lt__(self, other):
        return self.p_cost > other.p_cost
        
    # # Checks the equality between two possible objects
    # def __hash__(self):
    #     return hash(self.__members())



class ASARProblem(search.Problem):

    def __init__(self):
        self.initial = None # place here the initial state (or None)
        self.airplanes = []
        self.airports = []
        self.legs = []
        self.state_list = []
        #self.possible_actions = []
        
    
    def actions(self, s):
        N=len(self.airports)
        A=len(self.airplanes)
    
        if s is None:
            a = [0]*A
        
            possible_actions=[] #define empty matrix 
            for i in range(A): 
                row=[] 
                for k in range(N**A): 
                    row.append(0) 
                possible_actions.append(row) 
            
            
            for k in range(1, N**A):
                for i in range(A):
                    if k % 4**i == 0:

                        possible_actions[i][0]=self.airports[0].code
                        
                        if a[i] < N-1:
                            a[i]=a[i]+1
                        else:
                            a[i]=0
                    possible_actions[i][k]=self.airports[a[i]].code

            #Transpose matrix to be used correctly by results
            possible_actions = [[possible_actions[i][j] for i in range(len(possible_actions))] for j in range(len(possible_actions[0]))]
            aix=0
        else:
            # print("actions state is not none")
            possible_actions = []
            i=0
            for leg in s.l_list:
                if not leg.done: #if the leg is not done
                    #print(i)
                    i=i+1
                    for plane in s.p_list:
                        # print('Plane: ',plane.code, 'Plane Pos: ',plane.pos)
                        # print('First: ', (leg.a_dep.code == plane.pos))
                        if (leg.a_dep.code == plane.pos):
                            # print('T_Open : ', leg.a_arr.t_open, 'P_ava + leg.dl: ',(plane.t_avail + leg.dl), 'T_close: ', leg.a_arr.t_close)
                            # print((leg.a_arr.t_open <= (plane.t_avail + leg.dl) <= leg.a_arr.t_close))
                            if (leg.a_arr.t_open <= (plane.t_avail + leg.dl) <= leg.a_arr.t_close):
                                # print((leg.a_dep.t_open <= plane.t_avail <= leg.a_dep.t_close)) 
                                if (leg.a_dep.t_open <= plane.t_avail <= leg.a_dep.t_close):
                                    possible_actions.append([plane, leg])
                        #if (leg.a_dep.code == plane.pos) and (leg.a_arr.t_open <= (plane.t_avail + leg.dl) <= leg.a_arr.t_close) and (leg.a_dep.t_open <= plane.t_avail <= leg.a_dep.t_close):
                            #possible_actions.append([plane, leg])
                            aix = 0
        aix=0
        return copy.deepcopy(possible_actions)
        

    def result(self, state, action):
        
        if state is None :
            # print("Is None  - action:", action)
            new_state = []
            new_state = State(copy.deepcopy(self.airplanes),copy.deepcopy(self.legs), 0)
            i=0
            for plane in new_state.p_list:
                plane.pos = action[i]
                # print('plane_pos: ', action[i])
                plane.pos_init = action[i]
            
                for airport in self.airports:
                    if airport.code == action[i]:
                        plane.t_avail = airport.t_open # + plane.t_rot
                i=i+1
            #print("first state: ", plane.code, plane.pos)
            self.state_list.append(new_state)
            
            
        else:
            new_state = []
            # print("action:", action[0].code , action[0].pos, action[1].a_dep.code, action[1].a_arr.code)
            # print("Result: State is not None")
            new_state = copy.deepcopy(state) # make = state

            for plane in new_state.p_list:
                if plane.__eq__(action[0]):
                    plane.pos = action[1].a_arr.code
                    plane.t_arr = action[0].t_avail + action[1].dl
                    plane.t_avail = plane.t_arr + plane.t_rot
                    # print("plane positions:", plane.code, "-", plane.pos)
            for leg in new_state.l_list:
                if leg.__eq__(action[1]) and leg.done == False:
                    leg.flight=[action[0].code, action[0].t_avail, leg.profit[action[0].classe]]
                    leg.done = True
                  #  print("leg done:", leg.a_dep.code, leg.a_arr.code, action[0].code)
                    axi = 0
            self.state_list.append(new_state)
        aix=0
        return new_state
        
        
    def goal_test(self, state):

        if state is None:
            #print("goal state: False")
            return False
        else:
            for plane in state.p_list:
                if plane.pos != plane.pos_init:
                    #print("goal: False")
                    return False
            for leg in state.l_list:
                if leg.flight is None:
                    #print("goal: False")
                    return False
        #print("goal: True")
        return True
        
        
    def path_cost(self, c, state1, action, state2):

        #print("pathcost calculated")

        if state1 is None:
            c = c + 0
        else:
            c = c + 1/(action[1].profit[action[0].classe])
        state2.p_cost = c
        #print("cost:", state2.p_cost)
        return c  
        

    def heuristic(self, node):
        # note: use node.state to access the state
        h = 1
        return h
        
    
    def save(self, fh, state):
        # note: fh is an opened file object
        if state is None:
            fh.write("Unfeasible")
            return 
        # save into variable list of all the legs objects
        planes_list = state.p_list
        leg_list = state.l_list
        profit = 0

        for plane in planes_list:
            plane_leg_list = []
            for leg in leg_list:
                # check code of airplane
                if leg.flight[0] == plane.code and leg.done == True:
                    # load values from leg_list
                    code_plane, time_dep, prof = leg.flight

                    # Get hours with floor division
                    hours = int(time_dep) // 60
                    if len(str(hours)) < 2:
                        hours = '0'+str(hours)
                    # Get additional minutes with modulus
                    minutes = int(time_dep) % 60
                    if len(str(minutes)) < 2:
                        minutes = str(minutes) + '0'
                    total_time = str(hours)+str(minutes)
                    # save total profit 
                    profit = profit + int(prof)
                    # list to save printable data of this plane
                    data = [total_time, leg.a_dep.code, leg.a_arr.code]
                    # data = [time_dep, dep_airport, arr_airport]
                    plane_leg_list.append(data) # considering data = [...] and not [[...]] / else code change needed
                else: pass
            
            # sort list of legs of the airplane by ascending order of tipe departure
            plane_leg_list.sort(key=lambda x : x[0] , reverse = False)
            # turn each value of list into a string
            
            # Start Pinrting 
            for leg in leg_list:
                if plane.code in leg.flight:
                    fh.write('S ' + plane.code + " ")
                    # plane_leg_list = [[time_dep, dep_airport, arr_airport], [time_dep, dep_airport, arr_airport] ... ]
                    # Loop for write all those values
                    for row in plane_leg_list:
                        for element in row:
                            fh.write(str(element) + ' ')
            # add new line
            fh.write('\n')
            
        # Write final line with total profit
        fh.write('P ' + str(profit))

        

        
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
            
            # remove any word that is a space
            #words = [x.strip(' ') for x in words]
            #words = [value for value in words if value != ""]

            # If the line is about the Airport
            if line[0] == 'A':
                try:
                    code, t_open, t_close = words[1:]
                    # create and append a new airport object into the airports list
                    self.airports.append(Airport(calculate_time(int(t_open)), calculate_time(int(t_close)), code))
                except:
                    print("There's a line starting with 'A' that ins't properly defined")

            # If the line is about the Leg                           
            if line[0] == 'L':
                try:
                    a_dep, a_arr, dl = words[1:4]
                    # initialize a Leg object from the first 4 key informations
                    for i in range(len(self.airports)):
                        if self.airports[i].code == a_dep:
                            air_dep=self.airports[i]
                        if self.airports[i].code == a_arr:
                            air_arr=self.airports[i]
                    new_leg = Leg(air_dep, air_arr, calculate_time(int(dl)), profit={}, done = False)
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
                            plane.t_rot = calculate_time(int(dr))
                        else:
                            pass
                except:
                    print("There's a line starting with 'C' that ins't properly defined")
