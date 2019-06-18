import _ctypes
import gc
import faulthandler

print("None has id ", id(None))

def di(obj_id):
    return _ctypes.PyObj_FromPtr(obj_id)

class Node(object):
        def __init__(self, data, prev, next):
            # FIXME special case - to prevent reference=0
            if(prev == None and next == None):
                pass

            self.data = data
            # self.prev = prev
            # self.next = next
            # self.nextprev = prev^next
            # self.nextprev = prev.__xor__(next)
            # self.nextprev = Node.__xor__(next)
            self.nextprev = Node.xor(prev, next)
            # self.nextprev = (next if next is not None else 0)^(prev if prev is not None else 0)
        def xor(a, b):
            return id(a)^id(b)
            # if(a is None):
            #     return id(b)
            # elif(b is None):
            #     return id(a)
            # elif(b is None and a is None):
            #     return None
            # else:
            #     return id(a)^id(b)
        def __xor__(self, other):
            pass
            # if(self is None):
            #     return id(other)
            # elif(other is None):
            #     return id(self)
            # elif(self is None and other is None):
            #     return None
            # else:
            #     return id(self)^id(other)

class DoubleList(object):
    head = None
    tail = None

    def append(self, data):
        new_node = Node(data, None, None)
        print("Created new node with id ", id(new_node), " and value ", data)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            # new_node.prev = self.tail
            # new_node.next = None
            # # # new_node.nextprev = Node.xor(self.tail, None)
            new_node.nextprev = Node.xor(self.tail, None)
            # # added - self.tail.prev = 
            # self.tail.next = new_node
            tail_prev = Node.xor(self.tail.nextprev, self.tail)
            tail_next = id(new_node)
            print("Linked node ref ", tail_prev, " to ", tail_next)
            self.tail.nextprev = tail_prev^tail_next
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
        prev_node = None
        while current_node is not None:
            temp_node = current_node
            print(current_node.data)
            access_id = id(prev_node)^current_node.nextprev
            current_node = di(access_id)
            prev_node = temp_node
            # current_node = current_node.next
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