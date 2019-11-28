
#import probability


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

    def solve():
        meas_dict = {}
        for i in range(1, 5):
            for meas in measurement_list:
                for sensor in sensor_list:
                    if meas.time_step == i and meas.sensors == sensor.name:
                        m = meas.meas_value
                        meas_dict.update({sensor.name + "_" + str(i): m})

        for room in self.room_list:
            elimination_ask(room.name + str(self.time_step), meas_dict, museum).show_approx()

        return (room, likelihood)



def solver(input_file):
    return Problem(input_file).solve()

class BayesNet:
    """Bayesian network containing only boolean-variable nodes."""

    def __init__(self, node_specs=None):
        """Nodes must be ordered with parents before children."""
        self.nodes = []
        self.variables = []
        node_specs = node_specs or []
        for node_spec in node_specs:
            self.add(node_spec)

    def add(self, node_spec):
        """Add a node to the net. Its parents must already be in the
        net, and its variable must not."""
        node = BayesNode(*node_spec)
        assert node.variable not in self.variables
        assert all((parent in self.variables) for parent in node.parents)
        self.nodes.append(node)
        self.variables.append(node.variable)
        for parent in node.parents:
            self.variable_node(parent).children.append(node)

    def variable_node(self, var):
        """Return the node for the variable named var.
        >>> burglary.variable_node('Burglary').variable
        'Burglary'"""
        for n in self.nodes:
            if n.variable == var:
                return n
        raise Exception("No such variable: {}".format(var))

    def variable_values(self, var):
        """Return the domain of var."""
        return [True, False]

    def __repr__(self):
        return 'BayesNet({0!r})'.format(self.nodes)

"""
The algorithm described in Figure 14.11 of the book is implemented by the function elimination_ask. We use this for inference. The key idea is that we eliminate the hidden variables by interleaving joining and marginalization. It takes in 3 arguments X the query variable, e the evidence variable and bn the Bayes network.

The algorithm creates factors out of Bayes Nodes in reverse order and eliminates hidden variables using sum_out. Finally it takes a point wise product of all factors and normalizes. Let us finally solve the problem of inferring

P(Burglary=True | JohnCalls=True, MaryCalls=True) using variable elimination.
"""
class BayesNode:
    """A conditional probability distribution for a boolean variable,
    P(X | parents). Part of a BayesNet."""

    def __init__(self, X, parents, cpt):
        """X is a variable name, and parents a sequence of variable
        names or a space-separated string.  cpt, the conditional
        probability table, takes one of these forms:
        * A number, the unconditional probability P(X=true). You can
          use this form when there are no parents.
        * A dict {v: p, ...}, the conditional probability distribution
          P(X=true | parent=v) = p. When there's just one parent.
        * A dict {(v1, v2, ...): p, ...}, the distribution P(X=true |
          parent1=v1, parent2=v2, ...) = p. Each key must have as many
          values as there are parents. You can use this form always;
          the first two are just conveniences.
        In all cases the probability of X being false is left implicit,
        since it follows from P(X=true).
        >>> X = BayesNode('X', '', 0.2)
        >>> Y = BayesNode('Y', 'P', {T: 0.2, F: 0.7})
        >>> Z = BayesNode('Z', 'P Q',
        ...    {(T, T): 0.2, (T, F): 0.3, (F, T): 0.5, (F, F): 0.7})
        """
        if isinstance(parents, str):
            parents = parents.split()

        # We store the table always in the third form above.
        if isinstance(cpt, (float, int)):  # no parents, 0-tuple
            cpt = {(): cpt}
        elif isinstance(cpt, dict):
            # one parent, 1-tuple
            if cpt and isinstance(list(cpt.keys())[0], bool):
                cpt = {(v,): p for v, p in cpt.items()}

        assert isinstance(cpt, dict)
        for vs, p in cpt.items():
            assert isinstance(vs, tuple) and len(vs) == len(parents)
            assert all(isinstance(v, bool) for v in vs)
            assert 0 <= p <= 1

        self.variable = X
        self.parents = parents
        self.cpt = cpt
        self.children = []



def elimination_ask(X, e, bn):
    """
    [Figure 14.11]
    Compute bn's P(X|e) by variable elimination.
    >>> elimination_ask('Burglary', dict(JohnCalls=T, MaryCalls=T), burglary
    ...  ).show_approx()
    'False: 0.716, True: 0.284'"""
    assert X not in e, "Query variable must be distinct from evidence"
    factors = []
    for var in reversed(bn.variables):
        factors.append(make_factor(var, e, bn))
        if is_hidden(var, X, e):
            factors = sum_out(var, factors, bn)
    return pointwise_product(factors, bn).normalize()


