class Driver:
    # Initializes the Driver object with an ID
    def __init__(self, driver_id):
        self.driver_id = driver_id
        self.truck = None

    # Assigns a Truck to this Driver and returns True if successful
    def assign_truck(self, truck_list):
        # Find an unassigned Truck to assign to the Driver
        for truck in truck_list:
            if truck.driver is None:
                truck.driver = self
                self.truck = truck
                return True
        return False

    # Removes the Truck from being assigned to this Driver
    def remove_truck(self):
        self.truck.driver = None
        self.truck = None
