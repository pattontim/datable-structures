import _ctypes
import gc
import faulthandler

def di(obj_id):
    return _ctypes.PyObj_FromPtr(obj_id)

class Node(object):
        def __init__(self, data, prev, next):
            self.data = data
            # self.prev = prev
            # self.next = next
            # self.nextprev = prev^next
            # self.nextprev = prev.__xor__(next)
            # self.nextprev = Node.__xor__(next)
            self.nextprev = Node.xor(prev, next)
            # self.nextprev = (next if next is not None else 0)^(prev if prev is not None else 0)
        def xor(a, b):
            if(a is None):
                return b
            elif(b is None):
                return a
            elif(b is None and a is None):
                return None
            else:
                return di(id(a)^id(b))
        def __xor__(self, other):
            if(self is None):
                return other
            elif(other is None):
                return self
            elif(self is None and other is None):
                return None
            else:
                return di(id(self)^id(other))

class DoubleList(object):
    head = None
    tail = None

    def append(self, data):
        new_node = Node(data, None, None)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            # new_node.prev = self.tail
            # new_node.next = None
            new_node.nextprev = Node.xor(self.tail, None)
            # # added - self.tail.prev = 
            # self.tail.next = new_node
            tail_prev = Node.xor(self.tail.nextprev, self.tail)
            tail_next = new_node
            self.tail.nextprev = Node.xor(tail_prev, new_node)
            self.tail = new_node
 
# Solution: make XOR return the actual object, which is treated by assignment like an object (doesn't copy)

    def remove(self, node_value):
        current_node = self.head
 
        while current_node is not None:
            if current_node.data == node_value:
                # if it's not the first element
                if current_node.prev is not None:
                    current_node.prev.next = current_node.next
                    current_node.next.prev = current_node.prev
                else:
                    # otherwise we have no prev (it's None), head is the next one, and prev becomes None
                    self.head = current_node.next
                    current_node.next.prev = None
 
            next_node = Node.xor(current_node.prev, current_node.nextprev)
            current_node = next_node
            # current_node = current_node

 
    def show(self):
        print("Show list data:")
        current_node = self.head
        while current_node is not None:
            print(current_node.data)
            current_node = current_node.next
        # while current_node is not None:
        #     print (current_node.prev.data if hasattr(current_node.prev, "data") else None, 
        #     '->', 
        #     current_node.next.data if hasattr(current_node.next, "data") else None,
        #     ':', current_node.data)
 
        #     current_node = current_node.next
        print("*"*50)

# Required for ref by ID not to be deleted
gc.disable()
faulthandler.enable()

d = DoubleList()
 
d.append(5)
d.append(6)
d.append(50)
d.append(30)
 
d.show()
 
# d.remove(50)
# d.remove(5)
 
# d.show()