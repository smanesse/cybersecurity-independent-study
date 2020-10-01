import requests
import base64


def main():
    url = input("Enter url: ")
    stuff = input("Enter base64 to decrypt: ")
    blocks = dec(stuff)
    req(blocks, url)
    r = []
    for j in range(len(blocks) // 16):
        print("block " + str(j))
        intermed = []
        for k in range(1, 17):
            if intermed:
                blocks = blocks[:-(len(intermed) + 16)] + bytes([x ^ k for x in intermed]) + blocks[-16:]
            ind = -(16 + k)
            print(ind, blocks[ind])
            for g in range(256):
                print(g)
                if bytes([g]) == blocks[ind] and k == 1:
                    continue
                newblocks = blocks[:ind] + bytes([g]) + blocks[ind + 1:]
                if req(newblocks, url):
                    intermed.insert(0, g ^ k)
                    r.insert(0, (g ^ k) ^ blocks[ind])
                    print("found " + str(g))
                    print(r)
                    break
        blocks = blocks[:-16]
        print(bytes(r))


def req(s, url):
    e = enc(s)
    d = {"value": e}
    resp = requests.post(url, data=d)
    if resp.status_code == 500:
        return False
    return True


def enc(s):
    return base64.b64encode(s).decode('utf-8')


def dec(s):
    return base64.b64decode(s)


if __name__ == "__main__":
    main()
