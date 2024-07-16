import sys

from ride_model import Ride
from min_heap import MinHeap
from min_heap import MinHeapNode
from reb_black_tree import RedBlackTree, RBTNode


def insert_ride(ride, heap, rbt):
    if rbt.get_ride(ride.rideNumber) is not None:
        add_to_output(None, "Duplicate RideNumber", False)
        sys.exit(0)
        return
    rbt_node = RBTNode(None, None)
    min_heap_node = MinHeapNode(ride, rbt_node, heap.curr_size + 1)
    heap.insert(min_heap_node)
    rbt.insert(ride, min_heap_node)


def add_to_output(ride, message, list):
    file = open("output_file.txt", "a")
    if ride is None:
        file.write(message + "\n")
    else:
        message = ""
        if not list:
            message += ("(" + str(ride.rideNumber) + "," + str(ride.rideCost) + "," + str(ride.tripDuration) + ")\n")
        else:
            if len(ride) == 0:
                message += "(0,0,0)\n"
            for i in range(len(ride)):
                if i != len(ride) - 1:
                    message = message + ("(" + str(ride[i].rideNumber) + "," + str(ride[i].rideCost) + "," + str(
                        ride[i].tripDuration) + "),")
                else:
                    message = message + ("(" + str(ride[i].rideNumber) + "," + str(ride[i].rideCost) + "," + str(
                        ride[i].tripDuration) + ")\n")

        file.write(message)
    file.close()


def print_ride(rideNumber, rbt):
    res = rbt.get_ride(rideNumber)
    if res is None:
        add_to_output(Ride(0, 0, 0), "", False)
    else:
        add_to_output(res.ride, "", False)


def print_rides(l, h, rbt):
    list = rbt.get_rides_in_range(l, h)
    add_to_output(list, "", True)


def get_next_ride(heap, rbt):
    if heap.curr_size != 0:
        popped_node = heap.pop()
        rbt.delete_node(popped_node.ride.rideNumber)
        add_to_output(popped_node.ride, "", False)
    else:
        add_to_output(None, "No active ride requests", False)


def cancel_ride(ride_number, heap, rbt):
    heap_node = rbt.delete_node(ride_number)
    if heap_node is not None:
        heap.delete_element(heap_node.min_heap_index)


def update_ride(rideNumber, new_duration, heap, rbt):
    rbt_node = rbt.get_ride(rideNumber)
    if rbt_node is None:
        print("")
        # add_to_output(None, "No ride found to update", False)
    elif new_duration <= rbt_node.ride.tripDuration:
        heap.update_element(rbt_node.min_heap_node.min_heap_index, new_duration)
    elif rbt_node.ride.tripDuration < new_duration <= (2 * rbt_node.ride.tripDuration):
        cancel_ride(rbt_node.ride.rideNumber, heap, rbt)
        insert_ride(Ride(rbt_node.ride.rideNumber, rbt_node.ride.rideCost + 10, new_duration), heap, rbt)
    else:
        cancel_ride(rbt_node.ride.rideNumber, heap, rbt)


if __name__ == "__main__":
    heap = MinHeap()
    rbt = RedBlackTree()
    file = open("output_file.txt", "w")
    file.close()
    file = open("input.txt", "r")
    for s in file.readlines():
        n = []
        for num in s[s.index("(") + 1:s.index(")")].split(","):
            if num != '':
                n.append(int(num))
        if "Insert" in s:
            insert_ride(Ride(n[0], n[1], n[2]), heap, rbt)
        elif "Print" in s:
            if len(n) == 1:
                print_ride(n[0], rbt)
            elif len(n) == 2:
                print_rides(n[0], n[1], rbt)
        elif "UpdateTrip" in s:
            update_ride(n[0], n[1], heap, rbt)
        elif "GetNextRide" in s:
            get_next_ride(heap, rbt)
        elif "CancelRide" in s:
            cancel_ride(n[0], heap, rbt)

