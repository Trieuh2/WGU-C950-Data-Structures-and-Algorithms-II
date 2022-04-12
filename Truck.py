from datetime import timedelta


class Truck:
    # Constants used to change the properties of all Truck objects created
    average_speed = 18
    max_num_packages = 16

    # Truck constructor with optional parameter to define the average speed (in miles per hour) that the truck travels
    def __init__(self, truck_id, mph=average_speed, max_num_packages=max_num_packages):
        self.id = truck_id
        self.packages_id_list = []
        self.mph = mph
        self.max_num_packages = max_num_packages
        self.total_distance_traveled = 0
        self.mileage_timestamps = []
        self.driver = None
        self.time_obj = timedelta(hours=8, minutes=0, seconds=0)
        self.hub_address = "4001 South 700 East"
        self.at_hub = True


    # Adds the package to the list of packages that will be delivered by this Truck
    def assign_package(self, package):
        # Only add the Package to the Truck if it does not exceed the maximum number of Packages the Truck can hold
        if len(self.packages_id_list) < self.max_num_packages:
            self.packages_id_list.append(package.id_number)
            package.assigned_truck_id = self.id
        else:
            return False


    # Space-Time Complexity: O(N)
    # Sets the Delivery Status to "En route" for all Packages loaded onto the Truck
    def set_packages_en_route(self, ht):
        for package_id in self.packages_id_list:
            package = ht.lookup(package_id)
            package.delivery_status = "En route"
            package.en_route_timestamp = self.time_obj


    # Delivers the Package
    def deliver_package(self, ht, package_id, distance_traveled):
        package = ht.lookup(package_id)
        self.packages_id_list.remove(package_id)
        self.at_hub = False
        self.add_mileage(distance_traveled)
        self.time_obj += timedelta(minutes=(distance_traveled / self.mph * 60))
        self.mileage_timestamps.append([self.total_distance_traveled, self.time_obj])
        package.delivery_status = "Delivered"
        package.delivery_timestamp = self.time_obj


    # Sends the Truck back to the hub and updates the distance covered and time passed for the Truck
    def send_back_to_hub(self, distance_from_hub):
        self.add_mileage(distance_from_hub)
        self.time_obj += timedelta(minutes=(distance_from_hub / self.mph * 60))
        self.mileage_timestamps.append([self.total_distance_traveled, self.time_obj])
        self.at_hub = True


    # Adds mileage to the total distance traveled metric
    def add_mileage(self, miles):
        self.total_distance_traveled = self.total_distance_traveled + miles


    # Returns a list of Package objects correlating to the Truck's packages_id_list
    def get_package_list(self, ht):
        packages_list = []

        for package_id in self.packages_id_list:
            packages_list.append(ht.lookup(package_id))

        return packages_list


    # Returns True if the Truck's number of Packages assigned is equal to the maximum number of Packages it can carry
    def is_full(self):
        if len(self.packages_id_list) == self.max_num_packages:
            return True
        return False
