from probability import BayesNet, BayesNode, elimination_ask
import itertools
import time


class Rooms:
    def __init__(self, neighbours=[], sensors=None, name=None, on_fire=False, time=0):
        self.neighbours = neighbours
        self.sensor = sensors
        self.name = name
        self.on_fire = on_fire
        self.time = time
        self.bayes = []

class Sensors:
    def __init__(self, measure=False, name=None, tpr=0, fpr=0, l=[]):
        self.measure = measure
        self.name = name
        self.tpr = tpr
        self.fpr = fpr
        self.l = l

class Measurements:
    def __init__(self, time_step=0, sensors=[], meas_value=None):
        self.time_step = time_step
        self.sensors = sensors
        self.meas_value = meas_value

class Problem:
    def __init__(self, fh):
        # Place here your code to load problem from opened file object fh
        # and use probability.BayesNet() to create the Bayesian network
        self.room_list = []
        self.sensor_list = []
        self.propagation_prob = 0
        self.time_step = 0
        self.measurement_list = []
        self.loaded = self.load(fh)
        self.bayes = self.create()
        self.p_dict = {}


    def solve(self):
        # Build Evidence of measurements for elimination_ask = ev_dict
        ev_dict={} # for the elimination ask
        for m in self.measurement_list:
            s_name = m.sensors + '_' + str(m.time_step)
            ev_dict[s_name] = m.meas_value

        # Get likelihood for each room and store value in dictionary
        for room in self.room_list:
            r_name = room.name + '_' + str(self.time_step)
            # get likelihood of room being on fire = True
            likelihood = elimination_ask(r_name, ev_dict, self.bayes)[True]
            # Save values
            self.p_dict[r_name] = likelihood
        # Get max value
        room_name = max(self.p_dict, key=self.p_dict.get)
        max_likelihood = self.p_dict[room_name]
        return (room_name, max_likelihood)

    def create(self):
        baye = []
        for step in range(self.time_step+1):
            for room in self.room_list:
                # Create parents at t=0
                if step == 0:
                    baye.append((room.name + '_' + str(step), '', 0.5))
                else:
                    # Start building the child nodes
                    parent = None
                    parent = room.name + '_' + str(step-1)
                    # Add parents of current node
                    for neighboor in room.neighbours:
                        parent = parent + ' ' + neighboor + '_' + str(step-1)
                    
                    # Append to list, a tuple witt all the info of the current node
                    r_name = room.name + '_' + str(step)
                    baye.append((r_name, parent, self.get_prob(room = room)))
                    # Do sensors now
                    if room.sensor:
                        s_name = room.sensor.name+'_'+str(step)
                        r_name = room.name + '_' + str(step)
                        baye.append((s_name, r_name, self.get_prob(sensor = room.sensor)))
                    # if step == self.time_step:
                    #     parent = None
                    #     parent = room.name + '_' + str(step)
                    #     for neighboor in room.neighbours:
                    #         parent = parent + ' ' + neighboor + '_' + str(step)

                    #     r_name = room.name + '_' + str(step+1)
                    #     baye.append((r_name, parent, self.get_prob(room = room)))
                    
        print(baye)
        return BayesNet(baye)

    # Makes a binary table and creates a dictionary with the corresponding probability values
    def get_prob(self, room=[],sensor=[]):
        # start dictionary
        prob_dict = {}
        # If input is a room
        if room:
            # length of neighbours is always +1 because we need to count with itself as well
            num = len(room.neighbours)+1
            # generate binary list
            bin_table = list(itertools.product([False, True], repeat=num))
            for row in bin_table:
                # Check if they are all 'False'
                if all(item == False for item in row):
                    prob_dict[row] = 0
                # Check if they are all 'True'
                elif all(item == True for item in row):
                    prob_dict[row] = 1
                # if first element is 'False', it's now assured that there's at least a 'True' after
                elif row[0] == False:
                    prob_dict[row] = self.propagation_prob
                # if first element is 'True', it's now assured that there's at least a 'False' after
                elif row[0] == True:
                    prob_dict[row] = 1
        # If input is a sensor
        else:
            prob_dict[False] = sensor.fpr
            prob_dict[True] = sensor.tpr
        return prob_dict


    def load(self, fh):
        # note: fh is an opened file object
        # note: self.initial may also be initialized here

        # Store Lines of file into a list variable lines = []
        lines = []
        for line in fh:
            if line == '\n':
                pass
            else:
                line = line.replace("\n", "")
                lines.append(line)

        # sort list to do rooms first, then connections, then sensors, then propagation probability and measurements
        sort_order = ['R', 'C', 'S', 'P', 'M']
        lines = [tuple for x in sort_order for tuple in lines if tuple[0] == x]

        # Create and store objects from the information of lines in this loop
        for line in lines:

            # remove any word that is a space
            # words = [x.strip(' ') for x in words]
            # words = [value for value in words if value != ""]

            # If the line is about the Rooms
            if line[0] == 'R':
                try:
                    words = line.split()  # breaks down the line into words
                    # create and append a new room object into the room list
                    for i in range(1,len(words)):
                        self.room_list.append(Rooms([], None, words[i], False, 0))
                except:
                    print("There's a line starting with 'R' that ins't properly defined")

            # If the line is about the Connections
            if line[0] == 'C':
                try:
                    tuple = line.split()
                    for i in range(1,len(tuple)):
                        word = tuple[i].split(",")
                        for room in self.room_list:
                            if room.name == word[0]:
                                room.neighbours.append(word[1])
                            if room.name == word[1]:
                                room.neighbours.append(word[0])
                except:
                    print("There's a line starting with 'C' that ins't properly defined")

            # If the line is about the Sensors
            if line[0] == 'S':
                try:
                    tuple = line.split()
                    for i in range(1, len(tuple)):
                        word = tuple[i].split(":")
                        # Modified this to add sensor object in room as well, instead of only the name
                        sens = Sensors(False, word[0], float(word[2]), float(word[3]), [])
                        for room in self.room_list:
                            if room.name == word[1]:
                                room.sensor = sens
                        self.sensor_list.append(sens)
                except:
                    print("There's a line starting with 'S' that ins't properly defined")

            # If the line is about the propagation probability
            if line[0] == 'P':
                try:
                    word = line.split()
                    self.propagation_prob = float(word[1])
                except:
                    print("There's a line starting with 'P' that ins't properly defined")

            # If the line is about the Measurement
            if line[0] == 'M':
                self.time_step = self.time_step + 1
                try:
                    tuple = line.split()
                    for i in range(1,len(tuple)):
                        word = tuple[i].split(":")
                        if word[1] == "F":
                            self.measurement_list.append(Measurements(self.time_step, word[0], False))
                        if word[1] == "T":
                            self.measurement_list.append(Measurements(self.time_step, word[0], True))

                except:
                    print("There's a line starting with 'M' that ins't properly defined")
        return True

def solver(fh):
        return Problem(fh).solve()

# Time for execution time
start_time = time.time()
# Open file
fh = open('tests/P1.txt', 'r+')
# Solve and print solution
print('\n Solution -> ', solver(fh))
# Close file
fh.close()
# Get execution time
print("--- %s seconds ---" % (time.time() - start_time))
# Aux for debug
a = 0
