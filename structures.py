from random import randint
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

#tanto el hash set como el hash map no manejan colisiones porque no las tienen en ningún elemento del juego (todo lo que pueden llegar a tener no está en las manos
#del usuario y es dependiente de unos .jsonl que en el runtime solo se leen).
class HashMap:
    def __init__(self, max_items):
        self.hashmap = []
        for i in range(max_items):
            self.hashmap.append(None)

        self.max_items = max_items

    def hash(self, key):
        return sum(bytearray(key, 'utf-8')) % self.max_items

    def append(self, key, value):
        hashed = self.hash(key)
        self.hashmap[hashed] = (key, value)
        return

    def append_hash(self, key, value):
        #los id son los nombres hasheados en la pokedex/ekopdex, por eso hice esta función
        hashed = self.hash(key)
        self.hashmap[hashed] = (hashed, value)
        return
    
    def find(self, key):
        hashed = self.hash(key)
        if self.hashmap[hashed][0] == key:
            return self.hashmap[hashed][1]
        return False

    def find_with_hash(self, hashed):
        if self.hashmap[hashed]:
            return self.hashmap[hashed][1]
        return False

    def find_random(self):
        return self.hashmap[randint(0, self.max_items - 1)][1]

class HashSet:
    def __init__(self, max_items):
        self.hashset = []
        for i in range(max_items):
            self.hashset.append(None)

        self.max_items = max_items

    def hash(self, data):
         return sum(bytearray(data, 'utf-8')) % self.max_items

    def append(self, data):
        hashed = self.hash(data)
        self.hashset[hashed] = data
        return

    def find(self, data):
        hashed = self.hash(data)
        if self.hashset[hashed] == data:
            return True
        return False

    def display(self):
        for i in self.hashset:
            if i:
                print(i)


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

