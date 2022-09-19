from csv import *
from numpy import matrix

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

        self.pkToDeliver = []
        self.offices = []  # str
        self.map = {}
        self.deliveredTo = {}
        self.stops = [loc]

    def pickOffice(self):
        if self.location[:3] == "UPS":
            return self.location
        else:
            dd = [len([pk.office == office for pk in self.pkToDeliver]) for office in self.offices]
            dd = [min(self.size, ddi) for ddi in dd]
            return self.offices[dd.index(max(dd))]

    def getCity(self, key):
        if key[0] == self.location:
            return key[1]
        return key[0]

    def OneStop(self, addr):
        return [key for key in self.map if self.location in key and addr in key]

    def inMap(self, addr):
        return [key for key in self.map if addr in key]

    def pathFind(self, paths, addr):
        # extend list of lists until you can go to ind 0
        newPaths = []
        for path in paths:
            for arr in self.inMap(path[-1]):
                newCity = self.getCity(arr)
                if newCity not in path:
                    newPaths.append(path + [newCity])
        paths = newPaths
        validPath = [p for p in paths if p[-1] == addr]
        if validPath:
            print(validPath[0])
            return validPath[0]


    def navigate(self, addr):
        if self.location == addr:
            pass
        else:
            dist = self.OneStop(addr)  # false, or the distance
            if dist:
                self.driveTo(addr, dist)
            # handles dis 2 or more
            else:
                paths = [self.inMap(self.location)]
                for i in range(len(paths)):
                    for loc in paths[i][0]:
                        if loc != self.location:
                            paths[i][0] = loc
                path = self.pathFind(paths, addr)
                while path:
                    print()
                    dist = self.map[self.OneStop(path[0])[0]]
                    loc = self.getCity(self.OneStop(path[0])[0])
                    self.driveTo(loc, dist)
                    path = path[1:]

    def collectPackage(self, pk):
        if self.location in self.offices:
            if pk.office == self.location:
                pk.collected = True
                self.packages.append(pk)
        else:
            self.navigate(pk.office)



    def deliverPackage(self, pk):
        print("Delivering", pk.id, pk.address)
        if self.location == pk.address:
            pk.delivered = True
            self.packages.remove(pk)
            self.pkToDeliver.remove(pk)
            self.deliveredTo[pk] = pk.address
            print("DELIVERED", pk.address)
        else:
            print("NAV TO PK", pk.id, pk.address)
            self.navigate(pk.address)
            self.deliverPackage(pk)

    def deliverPackages(self):
        while self.pkToDeliver:
            office = self.pickOffice()
            self.navigate(office)
            pkFromOffice = [pk for pk in self.pkToDeliver if pk.office == office]
            while pkFromOffice and len(self.packages) <= self.size:
                self.collectPackage(pkFromOffice.pop())
            for package in self.packages:
                self.deliverPackage(package)

    # Don't worry about checking whether the truck is at a post-service office.
    # The test cases will make sure of that.
    def removePackage(self, pk):
        if self.location in self.offices and pk in self.packages:
            self.packages.remove(pk)

    def driveTo(self, loc, dist):
        # for 1 dist
        for edge in self.map:
            if loc in edge and self.location in edge:
                self.location = loc
                self.mileage += self.map[dist[0]]
                print("drove to ", self.location)
                return

    def getPackagesIds(self):
        return [package.id for package in self.packages]

def getDistance(truck):
    print([pk.id for pk in truck.packages])

def driveTo(truck, address):
    print(address)


def deliveryService(map, truck, packages):
    for package in packages:
        truck.pkToDeliver.append(package)
    truck.map = {(arr[0], arr[1]): arr[2] for arr in map}
    for key in truck.map:
        for city in key:
            if city[:3] == "UPS":
                truck.offices += [city]
    truck.deliverPackages()

    deliveredTo = {}  # package id to addresses  str:str
    stops = []  # addresses
    return (deliveredTo, stops)



def setupMap(map_file):
    map = []
    with open(map_file) as csvfile:
        r = reader(csvfile, delimiter=',')
        for row in r:
            map.append((row[0], row[1], int(row[2])))
    return map

def setupPackages(pk_file):
    packages = []
    with open(pk_file) as csvfile:
        r = reader(csvfile, delimiter=',')
        for row in r:
            pk = Package(row[0])
            pk.office = row[1]
            pk.address = row[2]
            packages.append(pk)
    return packages

def getWeight(edges, u, v):
    for edge in edges:
        if edge[0] == u and edge[1] == v:
            return edge[2]
        if edge[0] == v and edge[1] == u:
            return edge[2]
    print("Error: City", u, "and City", v, "are not adjacent.")
    return float("inf")

def mileage(map, stops):
    total = 0
    for i in range(1, len(stops)):
        total += getWeight(map, stops[i-1], stops[i])
    return total



mileage_of_all_maps = 0

# test_map1
map1 = setupMap("map1 copy.txt")
packages1 = setupPackages("packages1 copy.txt")
truck = Truck("truck", 5, "UPS")
print("---------")
print("truck", truck)
print("map", map1)
_, stops = deliveryService(map1, truck, packages1)
current_mileage = mileage(map1, stops)
mileage_of_all_maps += current_mileage
print("Truck's mileage using the setup in test_map1 =", current_mileage)

"""





# test_map1_smallTruck
map1 = setupMap("map1.txt")
packages1 = setupPackages("packages1.txt")
truck = Truck("truck", 3, "UPS")
_, stops = deliveryService(map1, truck, packages1)
current_mileage = mileage(map1, stops)
mileage_of_all_maps += current_mileage
print("Truck's mileage using the setup in test_map1_smallTruck =", current_mileage)

# test_map2
map2 = setupMap("map2.txt")
packages2 = setupPackages("packages2.txt")
truck = Truck("truck", 5, "UPS1")
_, stops = deliveryService(map2, truck, packages2)
current_mileage = mileage(map2, stops)
mileage_of_all_maps += current_mileage
print("Truck's mileage using the setup in test_map2 =", current_mileage)

# test_map3_packages3
map3 = setupMap("map3.txt")
packages3 = setupPackages("packages3.txt")
truck = Truck("truck", 5, "UPS1")
_, stops = deliveryService(map3, truck, packages3)
current_mileage = mileage(map3, stops)
mileage_of_all_maps += current_mileage
print("Truck's mileage using the setup in test_map3_packages3 =", current_mileage)
"""


"""
# test_map3_packages4
map3 = setupMap("map3.txt")
packages4 = setupPackages("packages4.txt")
truck = Truck("truck", 5, "UPS1")
_, stops = deliveryService(map3, truck, packages4)
current_mileage = mileage(map3, stops)
mileage_of_all_maps += current_mileage
print("Truck's mileage using the setup in test_map3_packages4 =", current_mileage)

# test_map4_packages4
map4 = setupMap("map4.txt")
packages4 = setupPackages("packages4.txt")
truck = Truck("truck", 5, "UPS1")
_, stops = deliveryService(map4, truck, packages4)
print(stops)
current_mileage = mileage(map4, stops)
mileage_of_all_maps += current_mileage
print("Truck's mileage using the setup in test_map4_packages4 =", current_mileage)

print()
print("The total mileage of all the maps =", mileage_of_all_maps)
"""























