from probability import BayesNet, BayesNode, elimination_ask

class Rooms:
    def __init__(self, neighbours=[], sensors=[], name=None, on_fire=False, time=0):
        self.neighbours = neighbours
        self.sensors = sensors
        self.name = name
        self.on_fire = on_fire
        self.time = time

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
                        self.room_list.append(Rooms([], [], words[i], False, 0))
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

                        for room in room_list:
                            if room.name == word[1]:
                                room.sensors.append(word[0])
                        sensor_list.append(Sensors(False, word[0], float(word[2]), float(word[3]), []))
                except:
                    print("There's a line starting with 'S' that ins't properly defined")

            # If the line is about the propagation probability
            if line[0] == 'P':
                try:
                    word = line.split()
                    self.propagation_prob = word[1]
                except:
                    print("There's a line starting with 'P' that ins't properly defined")

            # If the line is about the Measurement
            if line[0] == 'M':
                self.time_step = self.time_step + 1
                try:
                    tuple = line.split()
                    for i in range(1,len(line)):
                        word = tuple[i].split(":")
                        if word[1] == "F":
                            self.measurement_list.append(Measurements(self.time_step, word[0], False))
                        if word[1] == "T":
                            self.measurement_list.append(Measurements(self.time_step, word[0], True))

                except:
                    print("There's a line starting with 'M' that ins't properly defined")

    def solve(self):
        meas_dict = {}
        for i in range(1, 5):
            for meas in self.measurement_list:
                for sensor in self.sensor_list:
                    if meas.time_step == i and meas.sensors == sensor.name:
                        m = meas.meas_value
                        meas_dict.update({sensor.name + "_" + str(i): m})

        for room in self.room_list:
            elimination_ask(room.name + str(self.time_step), meas_dict, museum).show_approx()

        return (room, likelihood)

fh = open('Input.txt', 'r+')
p = Problem(fh)
p.load(fh)
fh.close()
p.solve()

paix=0

# def solver(input_file):
#     return Problem(input_file).solve()

