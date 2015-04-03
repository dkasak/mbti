import sys

def nix(items, it):
    """ Pick complementary item from a properly sorted iterable of items.

        Args:
            items: iterable of items sorted in such a way that related (but
                   complementary) items are adjacent
            item: single item from the list
        Returns:
            The complementary item of `it` (an element adjacent to it)
        Raises:
            TypeError: if `items` is not iterable
            ValueError: if `it` is not in `items`

        Given a list of items, where related but complementary items are
        adjacent, and an item that is inside that list, produce the
        complementary item. Effectively, this means the previous item if `it`
        is found at an odd index and the next item otherwise.
    """

    odd = lambda x: x % 2 != 0

    items = list(items)

    i = items.index(it)
    if odd(i):
        return items[i-1]
    else:
        return items[i+1]

class Function(object):
    _perceiving = ('N', 'S')
    _judging = ('T', 'F')
    _orientations = ('i', 'e')

    def __init__(self, f):
        if (len(f) != 2 or
            f[0].upper() not in Function._perceiving + Function._judging or
            f[1].lower() not in Function._orientations):
            raise ValueError("Not a valid Myers-Briggs function.")

        self.type = f[0].upper()
        self.orientation = f[1].lower()

    def __invert__(self):
        if self.type in Function._perceiving:
            t = nix(Function._perceiving, self.type)
        else:
            t = nix(Function._judging, self.type)
        o = nix(Function._orientations, self.orientation)
        return Function(t + o)

    def __neg__(self):
        o = nix(Function._orientations, self.orientation)
        return Function(self.type + o)

    def __str__(self):
        return self.type + self.orientation

    def __repr__(self):
        return 'Function("{}{}")'.format(self.type, self.orientation)

class Type(object):
    _order = ('E', 'I', 'S', 'N', 'F', 'T', 'J', 'P')

    def __init__(self, t):
        if len(t.strip("EISNFTPJ")) != 0:
            raise ValueError("Bad letter in type.")
        if len(t) != 4:
            raise ValueError("Types must contain four letters.")
        self.type = ''.join(sorted(t.upper(), key=lambda x: Type._order.index(x)))

    def complement(self):
        c = map(Type.negate, self.type)
        return Type(''.join(c))

    @staticmethod
    def negate(t):
        i = Type._order.index(t)
        if i % 2 == 1:
            return Type._order[i - 1]
        else:
            return Type._order[i + 1]

    def __str__(self):
        return "{type} -> {functions}".format(
                type=self.type,
                functions=self.functions())

    def __repr__(self):
        return 'mbti.Type("{}")'.format(self.type)

    def functions(self):
        disposition = self.type[0]
        perceiving = self.type[1]
        judging = self.type[2]
        public = perceiving if self.type[3] == 'P' else judging
        private = judging if public == perceiving else perceiving

        if disposition == "E":
            fs = [public, private, Type.negate(private), Type.negate(public)]
        else:
            fs = [private, public, Type.negate(public), Type.negate(private)]

        ds = 2 * [disposition, Type.negate(disposition)]
        ds = [d.lower() for d in ds]

        return list(map(''.join, zip(fs, ds)))

def main():
    if len(sys.argv) != 2:
        print("Needs a Myers-Briggs type as a single argument.")
        sys.exit(0)

    t = Type(sys.argv[1])
    print(t)

if __name__ == "__main__":
    main()
