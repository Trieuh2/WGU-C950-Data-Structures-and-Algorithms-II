from datetime import datetime, timedelta


class Package:
    # Constructor for the Package object
    # Creates a Package object with the attributes passed into the constructor method
    def __init__(self, id_number, delivery_address, delivery_city, delivery_state, delivery_zip, delivery_deadline,
                 package_mass, special_notes, delivery_status):
        self.id_number = id_number
        self.delivery_address = delivery_address
        self.delivery_city = delivery_city
        self.delivery_state = delivery_state
        self.delivery_zip = delivery_zip
        self.delivery_deadline = delivery_deadline
        self.package_mass = package_mass
        self.special_notes = special_notes
        self.delivery_status = delivery_status
        self.assigned_truck_id = None
        self.on_truck = False
        self.en_route_timestamp = None
        self.delivery_timestamp = None


    # Returns True if the Package is assigned to a Truck
    def is_truck_assigned(self):
        if self.assigned_truck_id is None:
            return False
        return True


    # Returns the id of the Truck that must deliver the Package
    def get_required_truck_id(self):
        if "Can only be on truck" in self.special_notes:
            # Find the specific Truck
            specified_truck_id = [int(i) for i in self.special_notes.split() if i.isdigit()][0]
            return specified_truck_id
        return None


    # If the Package arrives at the depot late, this function returns the delayed arrival time
    def get_delayed_arrival_time(self):
        if "Delayed on flight---will not arrive to depot until" in self.special_notes:
            tokenized_special_notes = self.special_notes.split()
            for token in tokenized_special_notes:
                try:
                    timestamp = datetime.strptime(token, "%H:%M")
                    delayed_arrival_timedelta = timedelta(hours=timestamp.hour, minutes=timestamp.minute)
                    return delayed_arrival_timedelta
                except:
                    pass
        # Packages with the wrong address will also be considered delayed Packages and be able to get delivered after
        # the address is updated, at 10:20 AM
        if "Wrong address listed" in self.special_notes:
            delayed_arrival_timedelta = timedelta(hours=10, minutes=20)
            return delayed_arrival_timedelta
        return None


    # Converts the delivery_deadline from String format to timedelta format and returns the timedelta value
    def get_delivery_deadline_timedelta(self):
        tokenized_special_notes = self.delivery_deadline.split()
        for token in tokenized_special_notes:
            try:
                timestamp = datetime.strptime(token, "%H:%M")
                delivery_deadline_timedelta = timedelta(hours=timestamp.hour, minutes=timestamp.minute)
                return delivery_deadline_timedelta
            except:
                pass

