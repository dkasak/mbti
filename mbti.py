import sys

def nix(items, it):
    """ Pick complementary item from an appropriately sorted iterable of items.

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
    perceiving = ('N', 'S')
    judging = ('T', 'F')
    orientations = ('i', 'e')

    def __init__(self, f):
        if (len(f) != 2 or
            f[0].upper() not in Function.perceiving + Function.judging or
            f[1].lower() not in Function.orientations):
            raise ValueError("Not a valid Myers-Briggs function.")

        self.type = f[0].upper()
        self.orientation = f[1].lower()

    def __invert__(self):
        if self.type in Function.perceiving:
            t = nix(Function.perceiving, self.type)
        else:
            t = nix(Function.judging, self.type)
        o = nix(Function.orientations, self.orientation)
        return Function(t + o)

    def __neg__(self):
        o = nix(Function.orientations, self.orientation)
        return Function(self.type + o)

    def __str__(self):
        return self.type + self.orientation

    def __repr__(self):
        return 'Function("{}{}")'.format(self.type, self.orientation)

class Type(object):
    def __init__(self, t):
        if len(t) != 4:
            raise ValueError("Argument must be either a MBTI type or an "
                             "iterable of four MBTI functions.")
        try:
            if sorted([x.type for x in t]) != (
                    sorted(Function.perceiving + Function.judging)):
                raise ValueError("Passed functions do not make a MBTI type.")

            t = Type.from_functions(t)
        except (TypeError, AttributeError):
            if len(t.strip("EISNFTPJ")) != 0:
                raise ValueError("Bad letter in type.")

        def normalize(t):
            letters = ('E', 'I', 'S', 'N', 'F', 'T', 'J', 'P')
            return ''.join(sorted(t.upper(), key=lambda x: letters.index(x)))

        self.type = normalize(t)

    def complement(self):
        """ Creates the complement type (the type with all functions inverted)."""
        return Type([~f for f in self.primary])

    def __invert__(self):
        """ Same as Type.complement. """
        return self.complement()

    @staticmethod
    def from_functions(fs):
        disposition = fs[0].orientation.upper()
        perceiving = fs[0].type if fs[0].type in Function.perceiving else fs[1].type
        judging = fs[0].type if fs[0].type in Function.judging else fs[1].type
        public = fs[0].type if fs[0].orientation == 'e' else fs[1].type
        strategy = 'P' if public == perceiving else 'J'
        return disposition + perceiving + judging + strategy

    def __str__(self):
        return "{type} -> [{functions}]".format(
                type=self.type,
                functions=", ".join(map(str, self.primary)))

    def __repr__(self):
        return 'Type("{}")'.format(self.type)

    @property
    def primary(self):
        disposition = self.type[0]
        perceiving = self.type[1]
        judging = self.type[2]
        public = perceiving if self.type[3] == 'P' else judging
        private = judging if public == perceiving else perceiving

        public = Function(public + 'e')
        private = Function(private + 'i')

        if disposition == "E":
            fs = [public, private, ~private, ~public]
        else:
            fs = [private, public, ~public, ~private]

        return fs

    @property
    def shadow(self):
        return [-f for f in self.primary]

def main():
    if len(sys.argv) != 2:
        print("Needs a Myers-Briggs type as a single argument.")
        sys.exit(0)

    t = Type(sys.argv[1])
    print(t)

if __name__ == "__main__":
    main()
