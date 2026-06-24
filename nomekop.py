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
        #aviso que si la posición dada es mayor a la cantidad de elementos esto lo agrega al final
        new_node = self.Node(data)

        if not self.head:
            self.head = new_node
            self.tail = new_node
            return

        self.tail.next = new_node
        self.tail = new_node
        

    def remove(self, target):
        if not self.head:
            return
        
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
    
    def find_random(self):
        returned = None
        while not returned:
            returned = self.hashmap[randint(0, self.max_items - 1)][randint(0, self.max_collisions - 1)]
        returned = returned[1]
        return returned


class HashSet:
    def __init__(self, max_items, max_collisions):
        self.hashset = []
        for i in range(max_items):
            self.hashset.append([])
            for _ in range(max_collisions):
                self.hashset[i].append(None)

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
    def __init__(self, name, damage, nomekop_id):
        self.name = name
        self.damage = damage
        self.id = nomekop_id

def load_nomekops():
    nomekops = HashMap(15, 3)
    with open(Path('nomekops.jsonl').resolve(), 'r') as file:
        for i in file:
            obj = json.loads(i)
            nomekops.append(obj["name"], Nomekop(obj["name"], obj["damage"], nomekops.hash(obj["name"])))
        return nomekops

def load_badges():
    badges = HashSet(8, 1)
    if os.path.getsize(Path('badges.jsonl').resolve()) != 0:
        with open(Path('badges.jsonl').resolve(), 'r') as file:
            for i in file:
                obj = json.loads(i)
                badges.append(obj["name"])
    return badges

def load_captured():
    global nomekops
    captured = LinkedList()
    if os.path.getsize(Path('captured.jsonl').resolve()) != 0:
        with open(Path('captured.jsonl').resolve(), 'r') as file:
            for idx, i in enumerate(file):
                obj = json.loads(i)
                captured.append(Nomekop(obj["name"], obj["damage"], nomekops.hash(obj["name"])))
    return captured

def add_to_captured(name, damage):
    global captured
    with open(Path('captured.jsonl').resolve(), 'a') as file:
        nomekop = {"name" : name, "damage": damage}
        file.write(json.dumps(nomekop) + '\n')
    captured = load_captured()

def remove_from_captured(name):
    global captured
    x = None
    with open(Path('captured.jsonl').resolve, 'r') as infile, open('out.jsonl', "w") as outfile:
        for line in infile:
            if not line.strip():
                continue
            
            obj = json.loads(line)
        
            if obj.get("name") == name:
                x = obj
                continue  
            
            outfile.write(line)

    os.replace(Path('out.jsonl').resolve(), Path('captured.jsonl').resolve())
    captured = load_captured(x['name'], x['damage'])

def display_team():
    global team
    if len(team) != 0:
        print("Your team is:")
        for i in team:
            print(i.name)
    else:
        print("Main team empty!")

nomekops = load_nomekops()
badges = load_badges()
captured = load_captured()
team = []
koa = Stack()
healing = Queue()

running = True
while running:
    print("---¡¡¡NOMEKOPS!!!---\n1. Ver Equipo Principal\n2. Ver Almacenamiento (PC)\n3. Capturar Nomekop\n4. Cambiar Equipo Principal\n5. Ordenar PC\n6. Transferir al Profesor Koa\n7. Deshacer Transferencia a Koa\n8. Ir al Centro Nomekop\n9. Salir")
    ans = input("What do you want to do?: ")
    match ans:
        case '1':
            display_team()
        case '2':
            captured.display()
        case '3':
            nomekop = nomekops.find_random()
            print(f"You captured {nomekop.name}!")
            add_to_captured(nomekop.name, nomekop.damage)
        case '4':
            display_team()
            captured.display()
            team_full = False if len(team) < 6 else True 
            in_captured = input("Who do you want to add? (answer with the Nomekop's name): ")
            if team_full:
                in_team = input("Who do you want to remove? (answer with the Nomekop's position in the list): ")
            try:
                in_captured = captured.remove(in_captured)
                if in_captured == False:
                    raise Exception
                if team_full:
                    add_to_captured(team.pop(in_team))
                team.append(in_captured)
            except:
                print("Error. Try again.")

        case '5':
            pass
        case '6':
            captured.display()
            name = input("Who do you want to transfer to Professor Koa? (answer with the Nomekop's name): ")
            try:
                name = captured.remove(name)
                if name == False:
                    raise Exception
                koa.push(name)
            except:
                print("Error. Try again.")

        case '7':
            if koa.size() != 0:
                add_to_captured(koa.pop())
                print("Returned nomekop!")
            else:
                print("No nomekops to return.")
        case '8':
            pass
        case '9':
            running = False
        case _:
            print("Invalid answer. Try again.")








