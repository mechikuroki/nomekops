from random import randint
from pathlib import Path
import json, os, time
from structures import *
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
    nomekops = HashMap(15)
    nomekop_ids = []
    with open(Path('nomekops.jsonl').resolve(), 'r') as file:
        for i in file:
            obj = json.loads(i)
            nomekop_id = nomekops.hash(obj["name"])
            nomekops.append_hash(obj["name"], Nomekop(obj["name"], obj["attack"], nomekop_id, obj["type"]))
            nomekop_ids.append(nomekop_id)
        nomekop_ids = sorted(nomekop_ids) #no uso los sorts que hice porque los adapté para que ordenen por nombre o tipo o ataque
        return nomekops, nomekop_ids 

def load_earned_badges():
    badges = HashSet(8)
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
    gyms = HashMap(8)
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
            if x[j].name.lower() > x[j + 1].name.lower():
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

def binary_search(mylist, e, offset=0):
    length = len(mylist)
    if length == 0: 
        return False
    
    if length == 1:
        if mylist[0] == e:
            return offset
        return False

    else:
        sec1list = mylist[0:round(length/2)]
        sec2list = mylist[round(length/2):]
        if sec1list[-1] > e:
            return binary_search(sec1list, e, offset) 
        elif sec1list[-1] == e:
            return offset + len(sec1list) - 1
        else:
            return binary_search(sec2list, e, offset + len(sec1list))


def display_team():
    global team
    if len(team) != 0:
        print("Your team is:")
        for i in team:
            print(i.name)
    else:
        print("Main team empty!")

def display_ekopdex():
    global nomekops
    for i in nomekops.hashmap:
        print(f"Name: {i[1].name} | Attack: {i[1].attack} | Type: {i[1].type} | ID: {i[1].id}")

def display_gyms():
    global gyms
    for i in gyms.hashmap:
        print(f"City: {i[0]} | Gym Leader: {i[1].gym_leader} | Specialty: {i[1].specialty}")

def display_captured():
    global captured
    current = captured.head
    if not current:
        print("No nomekops captured!")
        return
    print("You captured:")
    while current:
        print(current.data.name)
        current = current.next

nomekops, nomekop_ids = load_nomekops()
badges = load_earned_badges()
gyms = load_gyms()
captured = load_captured()
team = []
koa = Stack()
healing = Queue()

last_heal_epoch = time.time()
running = True
while running:
    print("---¡¡¡NOMEKOPS!!!---\n1. See Main Team\n2. See Storage\n3. Capture Nomekop\n4. Change Main Team\n5. Sort Storage\n6. Transfer to Professor Koa\n7. Undo Transfer to Koa\n8. Send Nomekop to Nomekop Center\n9. Fight Against a Gym Leader\n10. See Ekopdex\n11. See Earned Badges\n12. Find in Ekopdex\n13. Find in Main Team\n14. Exit")

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
            display_captured()
        case '3':
            nomekop = nomekops.find_random()
            print(f"You captured {nomekop.name}!")
            if len(team) < 6:
                team.append(nomekop)
            else:
                print("Main team full! Adding to storage!")
                add_to_captured(nomekop.name, nomekop.attack, nomekop.type)
        case '4':
            print()
            display_team()
            print()
            display_captured()
            team_full = False if len(team) < 6 else True 
            in_captured = input("Who do you want to add? (answer with the Nomekop's name [CASE SENSITIVE]): ")
            #tenés que llenar el equipo para poder cambiarlo
            if team_full:
                in_team = input("Who do you want to remove? (answer with the Nomekop's position on the list): ")
            try:
                in_captured = remove_from_captured(in_captured)
                if not in_captured:
                    raise Exception
                if team_full:
                    in_team = team.pop(int(in_team) - 1)
                    add_to_captured(in_team.name, in_team.attack, in_team.type)
                team.append(in_captured)
            except:
                print("Error. Try again.")

        case '5':
            display_captured()
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
            display_captured()
            nomekop = input("Who do you want to transfer to Professor Koa? (answer with the Nomekop's name [CASE SENSITIVE]): ")
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
            display_captured()
            nomekop = input("Who do you want to transfer to the Nomekop Center? (answer with the Nomekop's name [CASE SENSITIVE]): ")
            try:
                nomekop = remove_from_captured(nomekop)
                if nomekop == False:
                    raise Exception
                healing.enqueue(nomekop)
                #mandar un pokemon/nomekop al center reinicia la cuenta de todos los demás
                last_heal_epoch = time.time()
            except:
                print("Error. Try again.")
        case '9':
            if len(team) == 0:
                print("Your team is empty!")
                continue
            display_gyms()
            fighter = input("Who do you want to fight with? (answer with the city's name [CASE SENSITIVE]): ")
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
            display_ekopdex()
        case '11':
            badges.display()
        case '12':
            nomekop = input("Who do you want to find in the Ekopdex? (answer with the Nomekop's id): ")
            try:
                nomekop = int(nomekop)
            except:
                print("Invalid input. Try again.")
                continue
            index = binary_search(nomekop_ids, nomekop)
            if index:
                nomekop = nomekops.find_with_hash(index)
                print(f"Name: {nomekop.name} | Attack: {nomekop.attack} | Type: {nomekop.type} | ID: {nomekop.id}")
            else:
                print("Not found.")
                
        case '13':
            nomekop = input("Who do you want to find in the Main Team? (answer with the Nomekop's name [CASE SENSITIVE]): ")
            in_team = False
            for i in team:
                if nomekop == i.name:
                    print("The Nomekop is in the Main Team!")
                    in_team = True
            if not in_team:
                print("The Nomekop is not in the Main Team.")

        case '14':
            running = False
        case _:
            print("Invalid answer. Try again.")

