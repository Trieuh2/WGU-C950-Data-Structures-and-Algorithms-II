class HashTable:
    # Linear Probing HashTable constructor with an optional initial capacity used to store the Packages
    # Linear Probing is used to decrease the number of collisions for each insertion
    def __init__(self, initial_capacity=40, c1=0, c2=1):
        self.initial_capacity = initial_capacity
        self.package_table = [None] * initial_capacity
        self.bucket_status_table = ["EMPTY_SINCE_START"] * initial_capacity

        # Double hashing constants
        self.c1 = c1
        self.c2 = c2


    # Inserts a new item into the HashTable The key of the item will be the id_number and the value will be all the
    # corresponding components tied to that id_number
    def insert(self, package):
        i = 0
        buckets_probed = 0
        N = len(self.package_table)
        bucket = hash(package.id_number) % N

        # Iterate through the HashTable and insert the package at the next empty bucket
        while buckets_probed < N:
            # Insert package in next empty bucket
            if self.bucket_status_table[bucket] == "EMPTY_SINCE_START" or self.bucket_status_table[bucket] == "EMPTY_AFTER_REMOVAL":
                self.package_table[bucket] = package
                self.bucket_status_table[bucket] = "OCCUPIED"
                return True

            # No empty bucket found yet, increment i and compute next bucket's index
            i = i + 1
            bucket = (hash(package.id_number) + (self.c1 * i) + (self.c2 * i ** 2)) % N

            # Increment number of buckets probed
            buckets_probed = buckets_probed + 1

        # Iterated through the entire HashTable and could not insert the item, resize HashTable and re-insert
        self.resize()
        self.insert(package)
        return True


    # Searches for an item with a matching key in the hashtable. Returns the
    # item if found, or None if not found.
    def lookup(self, key):
        i = 0
        buckets_probed = 0
        N = len(self.package_table)
        bucket = hash(key) % N

        while (self.bucket_status_table[bucket] != "EMPTY_SINCE_START") and (buckets_probed < N):
            if (self.package_table[bucket] is not None) and (self.package_table[bucket].id_number == key):
                return self.package_table[bucket]

            # Increment i and recompute bucket index
            i = i + 1
            bucket = (hash(key) + self.c1 * i + self.c2 * i ** 2) % N

            # Increment number of buckets probed
            buckets_probed = buckets_probed + 1

        return None


    # Resizes the HashTable by doubling its original size
    def resize(self):
        # Create a HashTable with double the initial capacity
        resized_ht = HashTable(initial_capacity=self.initial_capacity * 2, c1 = self.c1, c2 = self.c2)

        # Iterate through the current HashTable and copy the Packages to the new HashTable
        for package in self.package_table:
            resized_ht.insert(package)

        self.initial_capacity = resized_ht.initial_capacity
        self.package_table = resized_ht.package_table
        self.bucket_status_table = resized_ht.bucket_status_table


    # Overloaded print function
    def __str__(self):
        s = "   --------\n"
        index = 0
        for item in self.package_table:
            value = str(item)
            if item is None: value = 'E'
            s += '{:2}:|{:^6}|\n'.format(index, value)
            index += 1
        s += "   --------"
        return s
