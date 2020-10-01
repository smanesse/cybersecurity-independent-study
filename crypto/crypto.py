import requests, base64


def main():
    url = input("Enter url: ")
    stuff = input("Enter base64 to decrypt: ")



def enc(s):
    return base64.b64encode(s).decode('utf-8')


def dec(s):
    return base64.b64decode(s)


if __name__ == "__main__":
    main()
