
def lifo ( iterable ) :

    new = PersistentStack()

    return new.extend(iterable)

class PersistentStack:

    def __init__ ( self , next = None, item = None ) :

        self.next = next
        self.item = item

    def add ( self , item ) :

        return PersistentStack(self, item)

    def extend ( self , iterable ) :

        new = self

        for item in iterable:

            new = new.add(item)

        return new

    def pop ( self ) :
        return (self.next, self.item)

    def __bool__ ( self ) :
        return self.next is not None

    def __iter__ ( self ) :

        current = self

        while current.next is not None:
            yield current.item
            current = current.next

    def __contains__ ( self , item ) :

        for other in self:
            if item == other:
                return True

        return False
