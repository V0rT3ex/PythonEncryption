from math import gcd
from random import randint


def generate_keys(n, phi):
    """
    This function receives the modulus(n) and the totient(phi)
    and retrieves two keys: private and public key.
    """

    # Creating the public key
    e = randint(2, phi - 1)
    # Looping until e is relatively prime to phi
    while True:
        if gcd(e, phi) == 1:
            break
        e = randint(2, phi - 1)

    # Creating the private key
    k = 1
    while True:
        d = (1 + k * phi) / e
        if d - int(d) == 0:
            d = int(d)
            break
        k += 1

    return e, d


def main():
    pass


if __name__ == '__main__':
    main()
