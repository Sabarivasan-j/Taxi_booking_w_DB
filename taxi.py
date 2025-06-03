from db_connection import get_connection

class Taxi:
    taxi_count = 0

    def __init__(self, current_spot='A', free_time=6, total_earning=0):
        self.id = None
        self.current_spot = current_spot
        self.free_time = free_time
        self.total_earning = total_earning
        self.trips = []

    def save_to_db(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Taxi (currentSpot, freeTime, totalEarning) VALUES (?, ?, ?)",
            (self.current_spot, self.free_time, self.total_earning)
        )
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    def update_to_db(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Taxi SET currentSpot = ?, freeTime = ?, totalEarning = ? WHERE id = ?",
            (self.current_spot, self.free_time, self.total_earning, self.id)
        )
        conn.commit()
        conn.close()

    def add_trip(self, customer_id, pickup, drop_loc, pickup_time, drop_time, amount, trip_detail):
        self.trips.append(trip_detail)
        self.update_to_db()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO Trip (taxiId, customerId, pickup, dropLoc, pickupTime, dropTime, amount) 
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (self.id, customer_id, pickup, drop_loc, pickup_time, drop_time, amount)
        )
        conn.commit()
        conn.close()

    def print_taxi_details(self):
        print(f"Taxi id - {self.id} Current Spot - {self.current_spot} Total Earnings - {self.total_earning} Free Time - {self.free_time}")
        print("-----------------------------------------------------------------------")

    def print_trip_details(self):
        print(f"Taxi - {self.id} Total Earnings - {self.total_earning}")
        print("Taxi ID\tCustomer ID\tFrom\tTo\tPickupTime\tDropTime\tAmount")
        for trip in self.trips:
            print(f"   {self.id}\t{trip}")
        print("======================================================================")

    def get_total_earning(self):
        return self.total_earning
