import _ctypes
import gc
import faulthandler
import sys
from time import sleep

# disable generational garbage collection - detection of cycles.
# Doesn't detect reference counts
gc.disable()
faulthandler.enable()

print("None has id ", id(None))

# convert obj_id to its original object
def di(obj_id):
    return _ctypes.PyObj_FromPtr(obj_id)

class Node(object):
        def __init__(self, data, prev, next):
            # FIXME special case - to prevent reference=0
            # if(prev == None and next == None):
                # pass

            self.data = data
            self.nextprev = Node.xor(prev, next)
            # self.nextprev = (next if next is not None else 0)^(prev if prev is not None else 0)
        def xor(a, b):
            return id(a)^id(b)
        def __xor__(self, other):
            pass
            # legacy unpythonic code
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

        _ctypes.Py_INCREF(new_node)
        print("Created new node with id ", id(new_node), " and value ", data,
        " and # refs: ", sys.getrefcount(new_node))
        print("Referencing the new object: ", gc.get_referrers(new_node))
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.nextprev = Node.xor(self.tail, None)
            
            # detected self reference, happens with first element.
            if(self.tail.nextprev == 0):
                tail_prev = id(None)
            else:
                tail_prev = id(None)^self.tail.nextprev

            tail_next = id(new_node)
            print("Linked node ref ", tail_prev, " to ", tail_next)
            self.tail.nextprev = tail_prev^tail_next
            self.tail = new_node
 
    def remove(self, node_value):
        current_node = self.head
        next_node = self.head
 
        while next_node is not None:
            prev_node = current_node if next_node is not self.head else None
            current_node = next_node
            if current_node.data == node_value:
                # if it's not the first element
                if prev_node is not None:
                    # to splice out, we recalculate nextprev
                    next_node = di(current_node.nextprev^id(prev_node))

                    # targets prev's next
                    prev_prev_node = di(prev_node.nextprev^id(current_node))
                    prev_node.nextprev = Node.xor(prev_prev_node, next_node)
                    ## current_node.prev.next = current_node.next

                    # targets next's previous
                    next_next_node = di(next_node.nextprev^id(current_node))
                    next_node.nextprev = Node.xor(prev_node, next_next_node)
                    ## current_node.next.prev = current_node.prev
                else:
                    # otherwise we have no prev (it's None), head is the next one, and prev becomes None
                    self.head = current_node.next
                    current_node.next.prev = None
                return
            next_node = di(current_node.nextprev^id(prev_node))
            
    def show(self):
        print("Show list data:")
        current_node = self.head
        prev_node = None
        while current_node is not None:
            temp_node = current_node
            print(current_node.data, '- ref count: ', sys.getrefcount(current_node))
            print(gc.get_referrers(current_node))
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
d = DoubleList()
 
d.append(5)
d.append(6)
d.append(50)
d.append(30)

d.show()

# cont = True
# wait = True
# access = 0
# while cont:
#     while(wait):
#         sleep(1)
#     print(di(access))
#     sleep(1)
# d.remove(70)
d.remove(50)
# d.remove(5)
 
d.show()

# increasing the reference counts is sufficient for our use case
# but it may lead to too many reference counts and so garbage collection may not work.
# upon element deletion, we'll have to call del manually.