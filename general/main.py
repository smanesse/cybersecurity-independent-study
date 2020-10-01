import argparse
import itertools

u = ""

subs = {
    "a": ["@", "4", "^"],
    "b": ["13"],
    "e": ["3", "&"],
    "g": ["&"],
    "h": ["#"],
    "i": ["!", "1"],
    "k": ["|<"],
    "l": ["1", "!"],
    "o": ["0"],
    "s": ["$", "5", "z", "zz", "zzz"],
    "t": ["7"],
    "v": ["\\/"],
    "z": ["2"]
}


def main(u, outfile="passwords.txt"):
    # index characters
    d = {}
    # pair with subs
    r = []
    for i in range(len(u)):
        c = u[i]
        if c in d.keys():
            d[c].append(i)
        else:
            d[c] = [i]
        r.append([c, c.upper()] + subs.get(c, []) + ["", "!", "1234", "2020", "2019"])
    r = itertools.product(*r)
    with open(outfile, "wt") as f:
        f.writelines(map(j, r))


def j(i):
    return "".join(i) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate potential passwords from a username')
    parser.add_argument("username", help="username to generate passwords from", type=str)
    parser.add_argument("-o", "--output", help="outfile", type=str, default="passwords.txt")
    args = parser.parse_args()
    main(args.username.lower(), args.output)
