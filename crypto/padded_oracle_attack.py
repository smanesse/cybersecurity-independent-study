import requests
import base64

def main():
    url=input("Enter url: ")
    ind = url.index("=") + 1
    first_part = url[:ind]
    stuff = url[ind:]
    blocks = dec(stuff)
    r = []
    for j in range(len(blocks)//16):
        print("block " + str(j))
        intermed = []
        for k in range(1, 17):
            if intermed:
                blocks = blocks[:-(len(intermed) + 16)] + bytes([x^k for x in intermed]) + blocks[-16:]
            ind = -(16 + k)
            print(ind, blocks[ind])
            for i in range(256):
                if bytes([i]) == blocks[ind]:
                    continue
                newblocks = blocks[:ind] + bytes([i]) + blocks[ind + 1:]
                if req(newblocks, first_part):
                    intermed.insert(0, i^k)
                    r.insert(0, (i ^ k) ^ blocks[ind])
                    print("found " + str(i))
                    print(r, intermed)
                    break
        blocks = blocks[:-16]
        print(bytes(r))
    
    
def req(s, url):
    e = enc(s)
    resp = requests.get(url + e)
    if "FLAG" in resp.text and "f50ce2f711f8939ae8d3076901f3328eb6be9a450ef851bc563d070246e51923" not in resp.text:
        print(resp.text)
    if "Incorrect padding" in resp.text or "PaddingException" in resp.text:
        return False
    return True


def enc(s):
    return base64.b64encode(s).decode('ascii').replace("=", "~").replace("/", "!").replace("+","-")

def dec(s):
    return base64.b64decode(s.replace("~", "=").replace("!", "/").replace("-", "+"))

if __name__ == "__main__":
    main()