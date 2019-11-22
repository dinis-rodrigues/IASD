
from probability import elimination_ask


class Rooms:
    def __init__(self):
        self.neighboors = []
        self.sensors = []
        self.name = 0
        self.on_fire = False
        self.time = 0

class Sensors:
    def __init__(self):
        self.measure = False
        self.name = 0
        self.tpr = 0
        self.fpr = 0
        self.l = []


class Measurements:
    def __init__(self):
        self.time_step = 0
        self.sensors = []

        self.time = 0




class Problem:
    def __init__(self, fh):
        # definir lista para o BayesNet
        # cpt = P(X | parents) = p, P(X = true| parents) = p -> probabilidade condicionada do quarto X estar on fire
        # lista como input para bayesNet = [X, parents, cpt]
        # parents = (R1, R2, ... Rn)
        # X = R1

        # Place here your code to load problem from opened file object fh
        # and use probability.BayesNet() to create the Bayesian network
        
        pass
    def solve(self):
    # Place here your code to determine the maximum likelihood solution
    # returning the solution room name and likelihood
    # use probability.elimination_ask() to perform probabilistic inference
        return (room, likelihood)
        
    def solver(self, input_file):
        return Problem(input_file).solve()
   
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

    # sort list to do airplanes first, then legs, then planes and finnaly classes
    sort_order = ['R', 'C', 'S', 'P', 'M']
    lines = [tuple for x in sort_order for tuple in lines if tuple[0] == x]

    # Create and store objects from the information of lines in this loop
    for line in lines:
        words = line.split()  # breaks down the line into words

        # remove any word that is a space
        # words = [x.strip(' ') for x in words]
        # words = [value for value in words if value != ""]

        # If the line is about the Rooms
        if line[0] == 'R':
            try:
                code, t_open, t_close = words[1:]
                # create and append a new airport object into the airports list
                self.airports.append(Airport(calculate_time(int(t_open)), calculate_time(int(t_close)), code))
            except:
                print("There's a line starting with 'R' that ins't properly defined")

        # If the line is about the Connections
        if line[0] == 'C':
            try:
                a_dep, a_arr, dl = words[1:4]
                # initialize a Leg object from the first 4 key informations
                for i in range(len(self.airports)):
                    if self.airports[i].code == a_dep:
                        air_dep = self.airports[i]
                    if self.airports[i].code == a_arr:
                        air_arr = self.airports[i]
                new_leg = Leg(air_dep, air_arr, calculate_time(int(dl)), profit={}, done=False)
                # The loop goes 2 by 2
                for number in range(4, len(words), 2):
                    classe = words[number]
                    profit = words[number + 1]
                    # Store the the class and the correspondent profit into a dict
                    new_leg.profit[classe] = int(profit)
                # append the final object in the legs list
                self.legs.append(new_leg)
                new_leg = None  # empty the variable for safety reasons
            except:
                print("There's a line starting with 'C' that ins't properly defined")

        # If the line is about the Sensors
        if line[0] == 'S':
            try:
                # Get the 2 key informations about the Plane
                # and append the Plane in the planes list
                code, classe = words[1:]
                self.airplanes.append(Airplane(classe=classe, code=code))
            except:
                print("There's a line starting with 'S' that ins't properly defined")

        # If the line is about the propagation probability
        if line[0] == 'P':
            try:
                classe, dr = words[1:]
                # check the class of each plane in our list
                # and update the rotation time
                for plane in self.airplanes:
                    if plane.classe == classe:
                        plane.t_rot = calculate_time(int(dr))
                        axis = 0
                    else:
                        pass
            except:
                print("There's a line starting with 'P' that ins't properly defined")

        # If the line is about the Measurement
        if line[0] == 'M':
            try:
                classe, dr = words[1:]
                # check the class of each plane in our list
                # and update the rotation time
                for plane in self.airplanes:
                    if plane.classe == classe:
                        plane.t_rot = calculate_time(int(dr))
                        axis = 0
                    else:
                        pass
            except:
                print("There's a line starting with 'M' that ins't properly defined")





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