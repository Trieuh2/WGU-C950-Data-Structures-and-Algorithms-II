# Henry Trieu, WGU ID #001306217

import csv
from datetime import datetime, timedelta

from Driver import Driver
from HashTable import HashTable
from Package import Package
from Truck import Truck

# Constants used to change the total number of Trucks and Drivers
num_trucks = 3
num_drivers = 2

# Space-Time Complexity: O(N)
# Parses Package information from the 'packages.csv' file to create Package objects that are inserted into the HashTable
def load_package_data(ht):
    # Open the packages CSV file
    with open('packages.csv') as csv_file:
        # Create a reader object which will iterate over lines in the packages.csv file
        csv_reader = csv.reader(csv_file, delimiter=',')

        # Iterate through the reader and parse the information from each row
        for row in csv_reader:
            # Store the parsed data as variables and pass them as input for creating a new Package object
            id_number = int(row[0])
            delivery_address = row[1]
            delivery_city = row[2]
            delivery_state = row[3]
            delivery_zip = row[4]
            delivery_deadline = row[5]
            package_mass = row[6]
            special_notes = row[7]
            delivery_status = "At the hub"

            package = Package(id_number, delivery_address, delivery_city, delivery_state, delivery_zip,
                              delivery_deadline, package_mass,
                              special_notes, delivery_status)

            # Insert the newly created Package object into the HashTable
            ht.insert(package)


# Space-Time Complexity: O(N^2)
# Returns a list of distance information parsed from the 'distances.csv' file
def load_distance_data():
    # Open the 'distances.csv' file, parse the values in each cell, and return a 2D list containing the parsed values
    with open('distances.csv') as csv_file:
        # Create a reader object which will iterate over lines in the 'distances.csv' file
        csv_reader = csv.reader(csv_file, delimiter=',')

        # Create the list that will store the distance data
        num_addresses = get_num_addresses()
        distance_data = [[0 for x in range(num_addresses)] for y in range(num_addresses)]

        # Iterate through the reader and parse the distance information between each address
        src_address_index = 0

        for src_address in csv_reader:
            for dest_address_index in range(num_addresses):
                if src_address[dest_address_index] != '':
                    distance_data[src_address_index][dest_address_index] = float(src_address[dest_address_index])
                    distance_data[dest_address_index][src_address_index] = float(src_address[dest_address_index])
            src_address_index = src_address_index + 1

        return distance_data


# Space-Time Complexity: O(N)
# Returns a list of address data parsed from the 'addresses.csv' file
def load_address_data():
    # Open the 'addresses.csv' file
    with open('addresses.csv') as csv_file:
        address_list = []

        # Create a reader object which will iterate over lines in the packages.csv file
        csv_reader = csv.reader(csv_file, delimiter=',')

        # Iterate through the reader and parse the information from each row
        for row_text in csv_reader:
            # Each row contains the full address for a location. Only parse the street address for the address list
            full_address = row_text[0].split("\n")
            street_address = full_address[1].strip()
            address_list.append(street_address)
    return address_list


# Space-Time Complexity: O(N)
# Returns the number of addresses found in the 'addresses.csv' file based on the number of rows
def get_num_addresses():
    num_addresses = 0
    # Open the 'addresses.csv'  file to count the number of rows in the file
    with open('addresses.csv') as csv_file:
        # Create a reader object which will iterate over lines in the 'distances.csv' file
        csv_reader = csv.reader(csv_file, delimiter=',')

        # Count the number of rows/columns, which will determine the size of the list
        for row in csv_reader:
            num_addresses = num_addresses + 1

    return num_addresses


# Space-Time Complexity: O(1)
# Returns the distance between two addresses
def distance_between(address1, address2):
    distance_list = load_distance_data()
    address_list = load_address_data()

    # Find the index of both addresses
    address1_index = address_list.index(address1)
    address2_index = address_list.index(address2)

    return distance_list[address1_index][address2_index]


# Space-Time Complexity: O(N)
# Initializes the Trucks and Drivers that will be used to deliver the packages
def initialize_trucks_drivers(NUM_TRUCKS, NUM_DRIVERS):
    truck_list = []
    driver_list = []

    # Since Drivers stay with the Truck that they are assigned to, extra Trucks/Drivers are unnecessary for operation
    # The number of Drivers and Trucks will be set to the minimum number of configured Drivers/Trucks
    num_trucks_drivers = min(NUM_TRUCKS, NUM_DRIVERS)

    # Initialize the Truck objects
    for current_truck_num in range(1, num_trucks_drivers + 1, 1):
        truck_id = current_truck_num
        truck = Truck(truck_id)
        truck_list.append(truck)

    # Initialize the Driver objects
    for current_driver_num in range(1, num_trucks_drivers + 1, 1):
        driver_id = current_driver_num
        driver = Driver(driver_id)
        driver.assign_truck(truck_list)
        driver_list.append(driver)

    return truck_list, driver_list


# Space-Time Complexity: O(N^4)
# Efficiently assigns Packages to the Truck until either all assignable Packages are assigned or until the Truck is full
def assign_packages(ht, truck):
    # Assign Packages until the Truck can no longer assign more Packages
    while len(get_assignable_packages(ht, truck)) > 0 and not truck.is_full() and truck.at_hub is True:
        # If the package_list is empty for the Truck, the current address will be set to the mail hub
        if len(truck.packages_id_list) == 0:
            address = truck.hub_address
        else:
            num_packages_in_truck = len(truck.packages_id_list)
            last_package_added_id = truck.packages_id_list[num_packages_in_truck - 1]
            last_package_added = ht.lookup(last_package_added_id)
            address = last_package_added.delivery_address

        # Space-Time Complexity: O(N)
        # Assign the closest Package to the last address
        nearest_package = find_nearest_package_in_list(address, get_assignable_packages(ht, truck))
        truck.assign_package(nearest_package)

        # Space-Time Complexity: O(N)
        # Handle Wrong Address case
        if nearest_package.id_number == 9:
            nearest_package.delivery_address = "410 S State St"
            nearest_package.delivery_city = "Salt Lake City"
            nearest_package.delivery_state = "UT"
            nearest_package.delivery_zip = "84111"
            sort_truck_package_list(ht, truck)

        # Space-Time Complexity: O(N^3) worst-case
        # If we've assigned a Package that exists in the associated Packages list, then ensure that we add the rest of
        # those Packages as well.
        for list in get_lists_associated_packages(ht):
            if nearest_package in list:
                for associated_package in list:
                    if associated_package.is_truck_assigned() is False:
                        truck.assign_package(associated_package)
        # If we added associated Packages, sort the truck's Package list to ensure it the route is optimized
        sort_truck_package_list(ht, truck)


# Space-Time Complexity: O(N^2)
# Sorts the list of Packages in the Truck to be ordered with priority of the shortest distance between each Package
def sort_truck_package_list(ht, truck):
    # Create a sorted Package_id list
    sorted_package_id_list = []
    current_address = truck.hub_address
    package_list = truck.get_package_list(ht)

    # Iterate through the Package list and add the Package IDs in the order of the shortest distance between each
    # Package
    while len(package_list) != 0:
        nearest_package = find_nearest_package_in_list(current_address, package_list)
        sorted_package_id_list.append(nearest_package.id_number)
        current_address = nearest_package.delivery_address
        package_list.remove(nearest_package)

    # Set the sorted list as the Truck's package id list
    truck.packages_id_list = sorted_package_id_list


# Space-Time Complexity: O(N)
# Returns the Package with the shortest distance between the current address and delivery address of the Package
def find_nearest_package_in_list(current_address, package_list):
    # Variables to store the nearest Package
    nearest_package = None
    nearest_package_distance = None

    # Algorithm to find the next Package with the shortest distance between the current address and the delivery address
    for package in package_list:
        if package is not None:
            # If we don't have a current package to start the comparisons, find the first package
            if nearest_package is None:
                nearest_package = package
                nearest_package_address = nearest_package.delivery_address
                nearest_package_distance = distance_between(nearest_package_address, current_address)
            # If nearest_package has been assigned, compare it against the current package being iterated list
            else:
                package_address = package.delivery_address
                package_distance = distance_between(package_address, current_address)

                # If the current package being iterated has a shorter distance from our current address, make this
                # our new nearest package
                if package_distance < nearest_package_distance:
                    nearest_package = package
                    nearest_package_distance = package_distance

    return nearest_package


# Space-Time Complexity: O(N^5)
# Deliver Packages until all Packages in the HashTable are delivered
def deliver_all_packages(ht, truck_list):
    while not all_packages_delivered(ht):
        for truck in truck_list:
            # Set the Delivery Status to "En route" for all Packages that will be delivered during this delivery trip
            truck.set_packages_en_route(ht)

            current_address = truck.hub_address
            current_package_index = 0

            # Deliver all the Packages that are loaded onto the Truck
            while len(truck.packages_id_list) > 0:
                # Find the Package in the HashTable and mark it as Delivered
                package_id = truck.packages_id_list[current_package_index]
                package = ht.lookup(package_id)

                # Calculate the distance traveled and add it to the total mileage covered by the Truck
                distance_traveled = distance_between(current_address, package.delivery_address)
                truck.deliver_package(ht, package_id, distance_traveled)

                # After all calculations, the Package's delivery address is now the current address
                current_address = package.delivery_address

            # After delivering all Packages, the Truck returns to the hub
            truck.send_back_to_hub(distance_between(current_address, truck.hub_address))
        # Assign more Packages
        for truck in truck_list:
            assign_packages(ht, truck)


# Space-Time Complexity: O(N)
# Returns True if all Packages have been delivered
def all_packages_delivered(ht):
    for package in ht.package_table:
        if package is not None and package.delivery_timestamp is None:
            return False
    return True


# Space-Time Complexity: O(N)
# Returns a list of unassigned Packages in the HashTable
def get_unassigned_packages(ht):
    unassigned_packages = []

    for package in ht.package_table:
        if package is not None and package.is_truck_assigned() is False:
            unassigned_packages.append(package)

    return unassigned_packages


# Space-Time Complexity: O(N^3)
# Returns a list of Packages that are assignable to the provided Truck
def get_assignable_packages(ht, truck):
    # Determine all Packages that cannot be assigned to the Truck first and then create a list of Packages that can
    # be assigned to the passed Truck
    unassignable_packages = get_unassignable_packages(ht, truck)
    assignable_packages = []

    # Iterate through the package table and find the Packages that can be assigned to the provided Truck
    for package in get_unassigned_packages(ht):
        # Check if the package has to be delivered by a specific Truck
        if package is not None and package not in unassignable_packages:
            assignable_packages.append(package)

    return assignable_packages


# Space-Time Complexity: O(N^3)
# Returns a list of unassigned Packages that cannot be assigned to the provided Truck
def get_unassignable_packages(ht, truck):
    unassignable_packages = []
    associated_package_lists = get_lists_associated_packages(ht)

    # Iterate through the Package list
    for package in ht.package_table:
        if package is not None:
            # If a Package is already assigned to a Truck, append it to the list
            if package.is_truck_assigned():
                unassignable_packages.append(package)

            # If a Package is required to be on a Truck different from the one passed, add the Package to the
            # unassignable Packages list
            elif package.get_required_truck_id() is not None and package.get_required_truck_id() is not truck.id:
                unassignable_packages.append(package)

                # If the current unassignable Package ends up in one of the lists of associated Packages, ensure
                # all associated Packages are added to the unassignable Packages list
                if len(associated_package_lists) > 0:
                    for list in associated_package_lists:
                        if package in list:
                            for associated_package in list:
                                if associated_package not in unassignable_packages:
                                    unassignable_packages.append(associated_package)

            # If the Package is delayed and has not arrived at the depot yet, it cannot be assigned to the Truck yet
            elif package.get_delayed_arrival_time() is not None and package.get_delayed_arrival_time() > truck.time_obj:
                if package not in unassignable_packages:
                    unassignable_packages.append(package)

    return unassignable_packages


# Space-Time Complexity: O(N^3)
# Returns a list of lists, each of which are a combination of Packages that must be delivered together on the
# same Truck and same delivery trip
def get_lists_associated_packages(ht):
    # List of associated package lists that contain Packages that must be delivered together
    associated_packages_lists = []

    # Space-Time Complexity: O(N^3)
    # Create the associated package lists and combine them if necessary
    for current_package in ht.package_table:
        if current_package is not None and "Must be delivered with" in current_package.special_notes:
            # Create a new list of associated Packages that must be delivered with the current Package
            associated_packages = find_directly_associated_packages(ht, current_package)

            # Variables to check if we need to combine lists of associated Packages that must be delivered together
            combine_lists = False
            list_to_combine = None

            # Space-Time Complexity: O(N^2)
            # Check if a Package in the current list already exists in a list that we've appended to the master list
            if len(associated_packages_lists) > 0:
                for package in associated_packages:
                    for list in associated_packages_lists:
                        if package in list:
                            combine_lists = True
                            list_to_combine = list
                            break

            # Space-Time Complexity: O(N)
            # If any Packages in the current associated_packages exist in a list that was appended to the master
            # list, do not add a new list but instead add directly to the already created list
            if combine_lists:
                for package in associated_packages:
                    if package not in list_to_combine:
                        list_to_combine.append(package)
            # If none of the Packages in the current associated_packages exist in a list that was appended to the
            # master list, add this as a new list
            else:
                associated_packages_lists.append(associated_packages)
    return associated_packages_lists


# Space-Time Complexity: O(N^2)
# Helper function for assign_packages_associative Parses the Special Notes of a Package and returns a list of
# Packages that the inputted Package must be delivered with
def find_directly_associated_packages(ht, package):
    if "Must be delivered with" in package.special_notes:
        # Create a new list
        associated_packages = [package]

        # Find the IDs of other packages that this current Package must be delivered with
        special_notes_commas_excluded = package.special_notes.replace(",", " ")
        tokenized_special_notes = special_notes_commas_excluded.split()
        package_ids_list = [int(i) for i in tokenized_special_notes if i.isdigit()]

        # Append IDs of additional Packages that must be delivered with the Package passed in the parameter
        for package_id in package_ids_list:
            package = ht.lookup(package_id)
            associated_packages.append(package)
            additional_packages = find_directly_associated_packages(ht, package)

            if additional_packages is not None:
                for additional_package in additional_packages:
                    if additional_package not in associated_packages:
                        associated_packages.append(additional_package)

        return associated_packages


# Displays a menu of options for the end-user to select from to perform different actions
def prompt_interactive_menu(ht, truck_list):
    # Display the title of the application
    print("===========================================")
    print("Western Governors University Parcel Service")
    print("===========================================")

    # Display menu options
    print("Please select a menu option to generate a report or retrieve package information.\n")
    print("\t 1. General Report")
    print("\t 2. Package Query")
    print("\t 3. Exit")
    valid_options = [1, 2, 3]

    # Prompt the user for option selection:
    option = None

    while option is None:
        user_input = input("\nEnter your option selection here: ")

        if user_input.isdigit() and int(user_input) in valid_options:
            option = int(user_input)
        else:
            print("Error: Invalid option provided.")

    # Process the option selected by the end-user:
    if option == 1: general_report(ht, truck_list)
    if option == 2: query_specific_package(ht, truck_list)
    if option == 3:
        print("The program will now close.")
        quit()


# Prompts the user for a time and displays the status report of all Packages at the specified time
def general_report(ht, truck_list):
    # Prompt for a time to generate the report
    report_datetime = prompt_time()

    # Display the status of all Packages at the time of the report
    print("=========================================")
    print("Status report of all packages at " + report_datetime.strftime("%I:%M %p"))
    print("=========================================")

    # For each Package, print out all the delivery information and status at the requested time
    for package in range(1, len(ht.package_table) + 1):
        if package is not None:
            display_package_query(ht, package, report_datetime)

    # Print the total mileage of all Truck at the specified time
    print_total_mileage_at_time(truck_list, report_datetime)

    # Prompt the user for the next action to perform
    prompt_interactive_menu(ht, truck_list)


# Returns the total mileage of all Trucks at the specified time
def print_total_mileage_at_time(truck_list, report_datetime):
    # Convert the specified time from datetime to timedelta to perform comparative operations
    report_timedelta = timedelta(hours=report_datetime.hour, minutes=report_datetime.minute)

    # Store the total mileage for all Trucks in a variable
    total_mileage = 0

    # For each truck, find the amount of distance covered closest to the specified report time
    for truck in truck_list:
        if len(truck.mileage_timestamps) > 0:
            index = len(truck.mileage_timestamps) - 1

            while index > 0:
                # Respective mileage and timestamp extracted from the Truck's mileage_timestamp list
                timestamp_mileage = truck.mileage_timestamps[index][0]
                timestamp_timedelta = truck.mileage_timestamps[index][1]

                if timestamp_timedelta <= report_timedelta:
                    total_mileage += timestamp_mileage
                    print("Truck %d's mileage: %0.2f miles" % (truck.id, timestamp_mileage))
                    break
                else:
                    index = index - 1
            if index == 0:
                print("Truck %d's mileage: %0.2f miles" % (truck.id, 0.00))
    # Print the total mileage at the specified time
    print("\nThe total mileage of all trucks at " + report_datetime.strftime("%I:%M %p") + " is %0.2f miles" %
        total_mileage)


# Queries and displays Package information
def query_specific_package(ht, truck_list):
    # Prompt the user for a time to generate a report and the specific Package to query
    report_datetime = prompt_time()
    package_id = prompt_package_id(ht)

    # Display information regarding the package at the specified time
    print("========================================")
    print("Querying package information at " + report_datetime.strftime("%I:%M %p"))
    print("========================================")
    display_package_query(ht, package_id, report_datetime)

    # Prompt the user for the next action to perform
    prompt_interactive_menu(ht, truck_list)


# Prints out information related to the specified Package at the specified time
def display_package_query(ht, package_id, report_datetime):
    # Retrieve the Package
    package = ht.lookup(package_id)

    # Convert the specified report's time from datetime type to timedelta type
    report_timedelta = timedelta(hours=report_datetime.hour, minutes=report_datetime.minute)

    # Build a String to print out for the current Package
    package_info_status = "[Package ID = %d] " % package.id_number

    # Generate the delivery status information
    if package.en_route_timestamp > report_timedelta:
        package_info_status += "\tDelivery Status: At the hub"
    elif package.delivery_timestamp > report_timedelta:
        # Convert the delivery timestamp from timedelta to datetime for printing purposes
        delivery_timestamp_datetime = datetime.strptime(str(package.delivery_timestamp), "%H:%M:%S")
        package_info_status += "\tDelivery Status: En route to delivery address, expected delivery at " + delivery_timestamp_datetime.strftime(
            "%I:%M %p")
    else:
        # Convert the delivery timestamp from timedelta to datetime for printing purposes
        delivery_timestamp_datetime = datetime.strptime(str(package.delivery_timestamp), "%H:%M:%S")
        package_info_status += "\tDelivery Status: Delivered at " + delivery_timestamp_datetime.strftime("%I:%M %p")

    # Build the Delivery Information
    package_info_status += "\tAddress: " + package.delivery_address
    package_info_status += "\tCity: " + package.delivery_city
    package_info_status += "\tZIP Code: " + package.delivery_zip
    package_info_status += "\tPackage Weight: " + package.package_mass + " kilograms"
    package_info_status += "\tDelivery Deadline: " + package.delivery_deadline

    # Display information regarding the package at the specified time
    print(package_info_status)


# Prompts the user for a time used to generate reporting
def prompt_time():
    report_datetime = None

    # Prompt the user for a specified time
    while report_datetime is None:
        try:
            report_datetime = datetime.strptime(
                input("Please provide a time for the report in the format [HOUR:MINUTE AM/PM]: "), "%I:%M %p")
        except:
            print("\tError: Invalid time format. Please try again.\n")

    return report_datetime


# Prompts the user for the ID of a Package
def prompt_package_id(ht):
    package_id = None

    # Prompt the user for a Package ID
    while package_id is None:
        user_input = input("Please enter the ID of the package you would like to view: ")

        if user_input.isdigit():
            if ht.lookup(int(user_input)) is not None:
                package_id = int(user_input)
            else:
                print("\tNo package found with the provided ID.\n")
        else:
            print("\tError: Invalid input. Please try again.\n")
    return package_id


def main():
    # Initialize a HashTable and load the package data into the HashTable
    delivery_ht = HashTable()
    load_package_data(delivery_ht)

    # Create the Trucks and Drivers
    truck_list, driver_list = initialize_trucks_drivers(num_trucks, num_drivers)

    # If there are any Packages arriving late at the depot, one of the Trucks will start at the delayed start time
    delayed_start_time = None

    for package in delivery_ht.package_table:
        if package is not None and package.get_delayed_arrival_time() is not None:
            if delayed_start_time is None or delayed_start_time > package.get_delayed_arrival_time():
                delayed_start_time = package.get_delayed_arrival_time()

    if len(truck_list) > 1:
        last_truck_index = len(truck_list) - 1
        truck_list[last_truck_index].time_obj = delayed_start_time

    # Assign all the Packages to the Trucks
    for truck in truck_list:
        assign_packages(delivery_ht, truck)

    # Deliver Packages until all Packages are delivered
    deliver_all_packages(delivery_ht, truck_list)

    # Display the menu options
    prompt_interactive_menu(delivery_ht, truck_list)


if __name__ == "__main__":
    main()
