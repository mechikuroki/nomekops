from random import randint
from pathlib import Path
import json, os, time
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None

    def append(self, data):
        new_node = self.Node(data)

        if not self.head:
            self.head = new_node
            self.tail = new_node
            return

        self.tail.next = new_node
        self.tail = new_node
        

    def remove(self, target):
        if not self.head:
            return False
        
        if self.head.data.name == target:
            x = self.head.data
            if self.head == self.tail:
                self.tail = None
            self.head = self.head.next
            return x
            
        current = self.head
        while current.next:
            if current.next.data.name == target:
                x = self.head.data
                if current.next == self.tail:
                    self.tail = current  
                current.next = current.next.next  
                return x
            current = current.next
        return False

    def remove_first(self):
        if not self.head:
            return False
        
        x = self.head.data

        if self.tail == self.head:
            self.head = None
            self.tail = None
            return x
        self.head = self.head.next
        return x

    def size(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def display(self):
        print()
        current = self.head
        if not current:
            print("No nomekops captured!")
            return
        print("You captured:")
        while current:
            print(current.data.name)
            current = current.next
        print()


class HashMap:
    def __init__(self, max_items, max_collisions):
        self.hashmap = []
        for i in range(max_items):
            self.hashmap.append([])
            for _ in range(max_collisions):
                self.hashmap[i].append(None)

        self.hashmap = tuple(self.hashmap)
        self.max_items = max_items
        self.max_collisions = max_collisions

    def hash(self, key):
         return sum(bytearray(key, 'utf-8')) % self.max_items

    def append(self, key, value):
        hashed = self.hash(key)
        for idx, i in enumerate(self.hashmap[hashed]):
            if i == None:
                self.hashmap[hashed][idx] = (key, value)
                return


    def find(self, key):
        hashed = self.hash(key)
        for idx, i in enumerate(self.hashmap[hashed]):
            if i[0] == key:
                return i[1]
        return False

    def find_random(self):
        returned = None
        while not returned:
            returned = self.hashmap[randint(0, self.max_items - 1)][randint(0, self.max_collisions - 1)]
        returned = returned[1]
        return returned

    def display(self):
        for i in self.hashmap:
            for j in i:
                if j:
                    try:
                        print(f"Name: {j[0]} | Attack: {j[1].attack} | Type: {j[1].type}")
                    except:
                        print(f"City: {j[0]} | Gym Leader: {j[1].gym_leader} | Specialty: {j[1].specialty}")


class HashSet:
    def __init__(self, max_items, max_collisions):
        self.hashset = []
        for i in range(max_items):
            self.hashset.append([])

        self.hashset = tuple(self.hashset)
        self.max_items = max_items
        self.max_collisions = max_collisions

    def hash(self, data):
         return sum(bytearray(data, 'utf-8')) % self.max_items

    def append(self, data):
        hashed = self.hash(data)
        for idx, i in enumerate(self.hashset[hashed]):
            if i == None:
                self.hashset[hashed][idx] = data
                return

    def find(self, data):
        hashed = self.hash(data)
        for idx, i in enumerate(self.hashset[hashed]):
            if i == data:
                return True
        return False

class Queue:
    def __init__(self):
        self.queue = []
    def enqueue(self, item):
        self.queue.append(item)
    def dequeue(self):
        try:
            return self.queue.pop(0)
        except:
            pass
    def peek(self):
        try:
            print(self.queue[1])
        except:
            pass
    def size(self):
        return len(self.queue)


class Stack:
    def __init__(self):
        self.stack = []
    def push(self, item):
        self.stack.append(item)
    def pop(self):
        try:
            return self.stack.pop()
        except:
            pass
    def peek(self):
        try:
            print(self.stack[-1])
        except:
            pass
    def size(self):
        return len(self.stack)

#------------------------------------------------------------

class Nomekop:
    def __init__(self, name, attack, nomekop_id, nomekop_type):
        self.name = name
        self.attack = attack
        self.id = nomekop_id
        self.type = nomekop_type 

class Gym:
    def __init__(self, city, gym_leader, specialty, badge):
        self.city = city
        self.gym_leader = gym_leader
        self.specialty = specialty
        self.badge = badge

    def fight(self):
        return self.badge if randint(0, 1) == 1 else None


def load_nomekops():
    nomekops = HashMap(15, 3)
    with open(Path('nomekops.jsonl').resolve(), 'r') as file:
        for i in file:
            obj = json.loads(i)
            nomekops.append(obj["name"], Nomekop(obj["name"], obj["attack"], nomekops.hash(obj["name"]), obj["type"]))
        return nomekops

def load_earned_badges():
    badges = HashSet(8, 2)
    if os.path.getsize(Path('earned_badges.jsonl').resolve()) != 0:
        with open(Path('earned_badges.jsonl').resolve(), 'r') as file:
            for i in file:
                obj = json.loads(i)
                badges.append(obj["name"])
    return badges

def add_to_badges(badge):
    global badges
    if badges.find(badge) != False:
        return
    with open(Path('earned_badges.jsonl').resolve(), 'a') as file:
        x = {"name" : badge}
        file.write(json.dumps(x) + '\n')
    badges = load_earned_badges()  

def load_captured():
    captured = LinkedList()
    if os.path.getsize(Path('captured.jsonl').resolve()) != 0:
        with open(Path('captured.jsonl').resolve(), 'r') as file:
            for idx, i in enumerate(file):
                obj = json.loads(i)
                captured.append(Nomekop(obj["name"], obj["attack"], nomekops.hash(obj["name"]), obj["type"]))
    return captured

def load_gyms():
    gyms = HashMap(8, 2)
    with open(Path('gyms.jsonl').resolve(), 'r') as file:
        for idx, i in enumerate(file):
            obj = json.loads(i)
            gyms.append(obj["city"], Gym(obj["city"], obj["gym_leader"], obj["specialty"], obj["badge_name"]))
    return gyms


def add_to_captured_list(x):
    global captured
    open(Path('captured.jsonl').resolve(), 'w').close()
    with open(Path('captured.jsonl').resolve(), 'a') as file:
        for i in x:
            nomekop = {"name" : i.name, "attack" : i.attack, "type" : i.type}
            file.write(json.dumps(nomekop) + '\n')
    captured = load_captured()

def add_to_captured(name, attack, ntype):
    global captured
    with open(Path('captured.jsonl').resolve(), 'a') as file:
        nomekop = {"name" : name, "attack": attack, "type" : ntype}
        file.write(json.dumps(nomekop) + '\n')
    captured = load_captured()


def remove_from_captured(name):
    global captured
    x = None
    matched = False
    with open(Path('captured.jsonl').resolve(), 'r') as infile, open('out.jsonl', "w") as outfile:
        for line in infile:
            if not line.strip():
                continue
            
            obj = json.loads(line)
        
            if obj.get("name") == name and matched == False:
                x = obj
                matched = True
                continue  
            
            outfile.write(line)

    os.replace(Path('out.jsonl').resolve(), Path('captured.jsonl').resolve())
    captured = load_captured()
    return Nomekop(x['name'], x['attack'], nomekops.hash(x['name']), x["type"])

def sort_by_type():
    global captured
    x = [captured.remove_first() for _ in range(captured.size())] 
    n = len(x)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if x[j].type.lower() < x[min_idx].type.lower():
                min_idx = j
        x[i], x[min_idx] = x[min_idx], x[i]
    add_to_captured_list(x)


def sort_by_name():
    global captured
    x = [captured.remove_first() for _ in range(captured.size())] 
    n = len(x)
    for i in range(n):
        switched = False
        for j in range(0, n - i - 1):
            if x[j].type.lower() < x[j + 1].type.lower():
                x[j], x[j + 1] = x[j + 1], x[j]
                switched = True
        if not switched:
            break
    add_to_captured_list(x)

def sort_by_attack():
    global captured
    x = [captured.remove_first() for _ in range(captured.size())]
    quicksort(x)
    add_to_captured_list(x)


def quicksort_part(arr, low, high):
    pivot = arr[high].attack
    i = low - 1

    for j in range(low, high):
        if arr[j].attack <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i+1


def quicksort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_index = quicksort_part(arr, low, high)
        quicksort(arr, low, pivot_index - 1)
        quicksort(arr, pivot_index + 1, high)

def display_team():
    global team
    if len(team) != 0:
        print("Your team is:")
        for i in team:
            print(i.name)
    else:
        print("Main team empty!")

nomekops = load_nomekops()
badges = load_earned_badges()
gyms = load_gyms()
captured = load_captured()
team = []
koa = Stack()
healing = Queue()

last_heal_epoch = time.time()
running = True
while running:
    print("---¡¡¡NOMEKOPS!!!---\n1. See Main Team\n2. See Storage\n3. Capture Nomekop\n4. Change Main Team\n5. Sort Storage\n6. Transfer to Professor Koa\n7. Undo Transfer to Koa\n8. Send Nomekop to Nomekop Center\n9. Fight Against a Gym Leader\n10. See Ekopdex\n11. See Earned Badges\n12. Exit")

    if healing.size() > 0 and time.time() - last_heal_epoch > 60:
        nomekop = healing.dequeue()
        add_to_captured(nomekop.name, nomekop.attack, nomekop.type)
        last_heal_epoch = time.time()
        print()
        print("Nomekop returned fron Nomekop Center!")
        print()

    ans = input("What do you want to do?: ")
    match ans:
        case '1':
            display_team()
        case '2':
            captured.display()
        case '3':
            nomekop = nomekops.find_random()
            print(f"You captured {nomekop.name}!")
            add_to_captured(nomekop.name, nomekop.attack, nomekop.type)
        case '4':
            display_team()
            captured.display()
            team_full = False if len(team) < 6 else True 
            in_captured = input("Who do you want to add? (answer with the Nomekop's name): ")
            if team_full:
                in_team = input("Who do you want to remove? (answer with the Nomekop's position on the list): ")
            try:
                in_captured = remove_from_captured(in_captured)
                if in_captured == False:
                    raise Exception
                if team_full:
                    in_team = team.pop(in_team)
                    add_to_captured(in_team.name, in_team.attack, in_team.type)
                team.append(in_captured)
            except:
                print("Error. Try again.")

        case '5':
            captured.display()
            sort = input("Do you want to sort by name (1), type (2) or attack (3)?: ")
            match sort:
                case '1':
                    sort_by_name()
                case '2':
                    sort_by_type()
                case '3':
                    sort_by_attack()
                case _:
                    print("Invalid input. Try again.")
            
        case '6':
            captured.display()
            nomekop = input("Who do you want to transfer to Professor Koa? (answer with the Nomekop's name): ")
            try:
                nomekop = remove_from_captured(nomekop)
                if nomekop == False or koa.size() > 5:
                    raise Exception
                koa.push(nomekop)
            except:
                print("Error. Try again.")

        case '7':
            if koa.size() != 0:
                x = koa.pop()
                add_to_captured(x.name, x.attack, x.type)
                print("Returned nomekop!")
            else:
                print("No nomekops to return.")
        case '8':
            captured.display()
            nomekop = input("Who do you want to transfer to the Nomekop Center? (answer with the Nomekop's name): ")
            try:
                nomekop = remove_from_captured(nomekop)
                print(nomekop)
                if nomekop == False:
                    raise Exception
                healing.enqueue(nomekop)
                last_heal_epoch = time.time()
            except:
                print("Error. Try again.")
        case '9':
            gyms.display()
            fighter = input("Who do you want to fight with? (answer with the city's name): ")
            fighter = gyms.find(fighter)
            if fighter:
                fighter = fighter.fight()
                if fighter:
                    add_to_badges(fighter)
                    print("You won!")
                else:
                    print("You lost!")
            else:
                print("Invalid input. Try again.")
        case '10':
            nomekops.display()
        case '11':
           pass
        case '12':
            running = False
        case _:
            print("Invalid answer. Try again.")








