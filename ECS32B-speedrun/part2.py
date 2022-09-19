
"""

I put only the pathFinder function here. I turn the map into an adjacency matrix in part 2.

"""

def pathFinder(curr, dest, AllLocs, mtx, helper_list):
    """
    returns a list from a current location to a destination, much like the form of 'stop';
    using recursion
    """

    # constructs a path/'helper_list' which keeps track of the direction an iteration has
    path = helper_list

    # base case
    if curr in path[0:-1]:
        return path

    # create indices for the adjacency matrix
    i = AllLocs.index(dest)  # int
    j = AllLocs.index(curr)  # int

    # if destination is adjacent
    if mtx[j][i] != 0:
        path.append(AllLocs[i])
        return path

    # otherwise, recursively extend the path
    else:
        adjs = []  # list of ints
        for y in range(0, len(AllLocs)):
            # two 'if' statements to prevent it from walking backwards
            if mtx[j][y] != 0:
                if AllLocs[y] not in path[0:-1]:
                    adjs.append(y)
        # break recursion if 'adjs' is empty
        if len(adjs) < 1:
            return path
        for z in range(0, len(adjs)):
            new_curr = AllLocs[adjs[z]]
            temp_path = list(helper_list)
            temp_path.append(new_curr)
            path = pathFinder(new_curr, dest, AllLocs, mtx, temp_path)
            if path[-1] == dest:
                return path


def getWeight(edges, u, v):
    """
    I also used the get weights function
    """
    for edge in edges:
        if edge[0] == u and edge[1] == v:
            return edge[2]
        if edge[0] == v and edge[1] == u:
            return edge[2]
    return float("inf")

class Package:
    def __init__(self, id):
        self.id = id
        self.address = ""
        self.office = ""
        self.ownerName = ""
        self.collected = False
        self.delivered = False


class Truck:
    def __init__(self, id, n, loc):
        self.id = id
        self.size = n
        self.location = loc
        self.packages = []
        self.mileage = 0
        self.deliveredTo = {}
        self.stops = [loc]
        self.collectedS = 0
        self.deliveredS = 0

        # some stats to keep track of
        self.map = None
        self.AllLocs = None
        self.matrix = None
        self.officeDicts = None  # dictionary of keys: offices, values: list of packages in them
        self.officeListS = None  # list of offices
        self.officeCounter = {}  # dictionary of keys: offices, values: number of packages
        # corresponding to the office initially

    def travelTo(self, dest, info):
        """
        Using the earlier pathFinder function along with driveTo, travelTo will traverse a car to
        its destination.
        """
        the_path = pathFinder(self.location, dest, self.AllLocs, self.matrix, [self.location])
        # info[0] and [1] are AllLocations and the matrix
        for stop in the_path:
            if self.location != stop:
                mileage = getWeight(self.map, self.location, stop)
                self.driveTo(stop, mileage)
                self.stops.append(stop)
            else:
                pass

    # helper function for the later used 'deliveredTo'
    def addOn(self, pk):
        if pk.id not in self.deliveredTo:
            self.deliveredTo[pk.id] = pk.address
        else:
            pass  # else statement never runs

    # helper function
    def collectPackage(self, pk, office):
        if self.location == pk.office and pk not in self.packages and not pk.collected \
                and not pk.delivered and self.size > 0:
            self.addOn(pk)
            self.packages.append(pk)
            self.size -= 1
            pk.collected = True
            self.collectedS += 1
            self.officeCounter[office] -= 1
        else:
            pass  # else statement never runs

    # helper function
    def collectPackages(self, officeDict, office):
        for pk in officeDict[office]:
            if self.size > 0:
                self.collectPackage(pk, office)

    def goCollect(self, officeDict, office, info):
        """
        This function moves the car to post offices accordingly, and runs collectPackages,
         which in turn runs collectPackage.
        """
        # base case
        if len(officeDict[office]) == 0:
            pass
        else:
            officeLocation = str(officeDict[office][0].office)  # location/name
            if self.location != officeLocation:
                self.travelTo(officeLocation, info)
            self.collectPackages(officeDict, office)

    # helper function
    def deliverPackage(self, pk):
        if self.location == pk.address and pk in self.packages and pk.collected and not pk.delivered:
            self.packages.remove(pk)
            self.size += 1
            pk.delivered = True
            self.deliveredS += 1
            self.addOn(pk)
        else:
            pass

    # helper function
    def deliverPackages(self):
        for pk in self.packages:
            if pk.address == self.location:
                self.deliverPackage(pk)
            else:
                pass

    def goDeliver(self, info):
        """
        This function moves the car to addresses accordingly, and runs deliverPackages,
        which in turn runs deliverPackage.
        """
        while len(self.packages) > 0:
            pk = self.packages[0]
            if self.location == pk.address:
                self.deliverPackages()
            else:
                self.travelTo(pk.address, info)
                self.deliverPackages()

    # Don't worry about checking whether the truck is at a post-service office. 
    # The test cases will make sure of that.
    def removePackage(self, pk):
        if pk in self.packages:
            self.packages.remove(pk)
            self.size += 1
            pk.collected = False
            pk.office = self.location
        else:
            pass
        return

    def driveTo(self, loc, dist):
        self.location = loc
        self.mileage += dist

    def getPackagesIds(self):
        pkIds = self.packages
        for i in range(0, len(pkIds)):
            pkIds[i] = pkIds[i].id
        return pkIds

    def getMileage(self):
        print(self.mileage)

"""
Copy your Package and Truck classes here
"""


def getAllLocs(map):
    """
    This function returns a list of all unique locations on the map, helpful later
    """
    ini = []
    for tup in map:
        if tup[0] not in ini:
            ini.append(tup[0])
        if tup[1] not in ini:
            ini.append(tup[1])
    return ini


# helper function for 'genMatrix'
def genEmptyMatrix(AllLocs):
    rep = []
    mtx = []
    for i in range(0, len(AllLocs)):
        mtx.append([])
    for i in range(0, len(AllLocs)):
        for j in range(0, len(AllLocs)):
            mtx[i].append(0)
    return mtx


def genMatrix(AllLocs, map):  # map?
    """
    generates an 1-step adjacency matrix as a list of lists
    """
    mtx1 = genEmptyMatrix(AllLocs)
    mtx = mtx1
    print('map:', map[0:15])
    for tup in map:
        i = AllLocs.index(tup[0])
        j = AllLocs.index(tup[1])
        mtx[i][j] = 1
        mtx[j][i] = 1
    return mtx


def genOfficeDict(packages):
    """
    This function simply generates a dictionary where the keys are all unique offices, and the
    values for each key/office is a list of all packages in that office.
    Helpful for later
    """
    dictr = {}
    for pk in packages:
        if pk.office not in dictr:
            dictr[pk.office] = [pk]
        else:
            if pk not in dictr[pk.office]:
                dictr[pk.office].append(pk)
    return dictr


def doDeliveries(truck, officeDict, office, info):
    """
    This function does deliveries based on an office and tracks package completion
    """
    while truck.officeCounter[office] > 0:
        truck.goCollect(officeDict, office, info)
        truck.goDeliver(info)


"""
deliveryService
"""
def deliveryService(map, truck, packages):

    deliveredTo = {}  # keys = package id, value = address of package
    stops = []  # ordered list of stops

    # here I generate some variables within the function
    officeDict = genOfficeDict(packages)  # Dict of office name:pk.id; for package tracking
    officeList = []  # list of offices
    for office in officeDict:
        officeList.append(office)
    AllLocs = getAllLocs(map)  # a list of all locations in the map, used for matrix construction
    matrix = genMatrix(AllLocs, map)  # an adjacency matrix representing connectivity of edges.

    # as well as pass the information to the truck object
    truck.officeDicts = officeDict
    truck.officeListS = officeList
    for office in officeDict:
        truck.officeCounter[office] = len(officeDict[office])
    truck.AllLocs = AllLocs
    truck.matrix = matrix
    truck.map = map
    info = [AllLocs, matrix]

    # I am collecting packages by office
    for office in officeList:
        doDeliveries(truck, officeDict, office, info)

    ### DEL ### DEL ### DEL
    print('\n HOW ABOUT\nlen(truck.deliveredTo) \n', len(truck.deliveredTo),' and len(truck.stops):\n',
          len(truck.stops),
          '\nstops:', len(truck.stops),
          '\ncollected:', truck.collectedS,
          '\ndelivered:', truck.deliveredS)

    deliveredTo = truck.deliveredTo
    stops = truck.stops
    return (deliveredTo, stops)

