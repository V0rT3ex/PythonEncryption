from math import gcd
from random import randint


def is_prime(n):
    """
    This function receives a number - n.
    It returns whether n is prime or not.
    Time complexity is O(n**0.5) in the worst case.
    """

    if n == 2 or n == 3:
        return True
    elif n < 2 or n % 2 == 0 or n % 3 == 0:
        return False

    # Looping until i reaches the square root of n
    for i in range(4, int(n ** 0.5)):
        if n % i == 0:
            return False
    return True


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
    p = int(input("Insert the first prime number:\t"))
    q = int(input("Insert the second prime number:\t"))
    n = p * q
    phi = (p - 1) * (q - 1)
    e, d = generate_keys(n, phi)
    message = input("Enter a message to decrypt:\t")
    cipher = [ord(s) for s in message]
    cipher = [(c ** e % n) for c in cipher]
    string_cipher = [chr(c) for c in cipher]
    string_cipher = ''.join(string_cipher)
    print("Encrypted data:\t{}".format(string_cipher))
    cipher = [(c ** d % n) for c in cipher]
    string_cipher = [chr(c) for c in cipher]
    string_cipher = ''.join(string_cipher)
    print("Decrypted data:\t{}".format(string_cipher))


if __name__ == '__main__':
    main()
