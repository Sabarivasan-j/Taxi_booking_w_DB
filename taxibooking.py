from taxi import Taxi

def create_taxis(n):
    taxis = []
    for _ in range(n):
        t = Taxi()
        t.save_to_db()
        taxis.append(t)
    return taxis

def get_free_taxis(all_taxis, pickup, pickup_time):
    free_taxis = []
    for t in all_taxis:
        distance = abs(ord(t.current_spot) - ord(pickup))
        if pickup_time >= t.free_time and distance <= (pickup_time - t.free_time):
            free_taxis.append(t)
    return free_taxis

def book_taxi(customer_id, pickup_point, drop_point, pickup_time, taxi_list):
    booked_taxi = None
    min_distance = float('inf')

    for t in taxi_list:
        distance_bw_cust_taxi = abs(ord(pickup_point) - ord(t.current_spot)) * 15
        if distance_bw_cust_taxi < min_distance:
            booked_taxi = t
            min_distance = distance_bw_cust_taxi

    if booked_taxi is None:
        print("No taxi available to book.")
        return

    distance_bw_pick_drop = abs(ord(pickup_point) - ord(drop_point)) * 15
    earnings = ((distance_bw_pick_drop - 5) * 10) + 100
    drop_time = pickup_time + (distance_bw_pick_drop // 15)
    trip_detail = f"{customer_id}\t{pickup_point}\t{drop_point}\t{pickup_time}\t{drop_time}\t{earnings}"

    # Update taxi details
    booked_taxi.free_time = drop_time
    booked_taxi.current_spot = drop_point
    booked_taxi.total_earning += earnings
    booked_taxi.add_trip(customer_id, pickup_point, drop_point, pickup_time, drop_time, earnings, trip_detail)

    print(f"Taxi {booked_taxi.id} is Booked Successfully!")

def main():
    taxis = create_taxis(4)
    customer_id = 1

    while True:
        print("Enter 1 for Booking:")
        print("Enter 2 for Printing Taxi Details:")
        print("Enter 3 to Exit:")
        choice = input()

        if choice == '1':
            print("Enter Pickup point (A-F): ")
            pickup_point = input().upper()
            print("Enter Drop point (A-F): ")
            drop_point = input().upper()
            print("Enter Pickup Time (integer): ")
            try:
                pickup_time = int(input())
            except ValueError:
                print("Invalid time input.")
                continue

            # Validate input
            if pickup_point not in ['A','B','C','D','E','F'] or drop_point not in ['A','B','C','D','E','F']:
                print("Invalid pickup or drop location. Valid locations: A,B,C,D,E,F")
                continue

            free_taxis = get_free_taxis(taxis, pickup_point, pickup_time)
            if not free_taxis:
                print("All taxis are busy. No taxis can be allotted.")
                continue

            # Sort free taxis by total earnings ascending
            free_taxis.sort(key=lambda x: x.get_total_earning())

            book_taxi(customer_id, pickup_point, drop_point, pickup_time, free_taxis)
            customer_id += 1

        elif choice == '2':
            print("Taxi details:")
            for t in taxis:
                t.print_taxi_details()
            for t in taxis:
                t.print_trip_details()

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
