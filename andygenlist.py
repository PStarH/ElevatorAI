import random

def generate_random_person(num_floors):
    f1 = random.randint(1, num_floors-1)
    if random.randint(0,1) == 0:
        f2 = 0
    else:
        choices = [i for i in range(1, num_floors)]
        choices.remove(f1)
        f2 = choices[random.randint(0,len(choices)-1)]
    person = {
        "floor1": f1,
        "floor2": f2,
        "time": random.randint(0, 1799)
    }
    return person

def output(num_floors, num_people_on_upper_floors, num_people_on_base_floor):
    elevator_floor = 1

    outlist = []

    print(f"Elevator starts at floor {elevator_floor}.")
    #people demanding elevator at first floor
    for i in range(num_people_on_base_floor):
        person = generate_random_person(num_floors)
        outlist.append((person['time'],1,person['floor1']))
        # print(f"Person {i + 1} on floor {1} wants to go {person['floor1']} at time {person['time']}.")
    #people demanding elevator at upper floors  
    for i in range(num_people_on_upper_floors):
        person = generate_random_person(num_floors)
        outlist.append((person['time'],person['floor1'],person['floor2']))
        # print(f"Person {i + 1} on floor {person['floor1']} wants to go {person['floor2']} at time {person['time']}.")
    return outlist

# num_floors = int(input("please senter the number of floors: "))
# num_people_on_upper_floors = int(input("enter the number of people above first floor: "))
# num_people_on_base_floor = int(input("please enter the number of people on the first floor: "))
# print(output(num_floors, num_people_on_upper_floors, num_people_on_base_floor))