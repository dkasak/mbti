import sys

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
