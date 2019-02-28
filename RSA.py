import os
from math import gcd
from random import randint


def is_prime(n):
    """
    This functions receives a number and returns whether
    the number is prime (True) or not(False). It is executed in O(n^0.5) efficiency.
    """

    if n == 2 or n == 3:
        return True
    elif n < 2 or n % 2 == 0 or n % 3 == 0:
        return False
    # Looping until we get to square root of the number passed in as a parameter
    for i in range(4, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def write_list_to_file(l, file):
    """
    This function receives two parameters - l and file.
    l is a list which will be written to the file .
    """

    for item in l:
        file.write(str(item) + ",")


def generate_prime_file(a, path=''):
    """
    This function creates a list of prime numbers under the upper boundary denoted as a.
    It will also write the list to a file.
    If the path parameter is not passed in, it will create a new text file in the working directory.
    Otherwise, the list will be written to the path passed in.
    """

    prime_list = [i for i in range(a + 1) if is_prime(i)]
    if path == '':
        try:
            primes_file = open("primes.txt", "wt", encoding='utf-8')
        except Exception as e:
            print(e)
        else:
            write_list_to_file(prime_list, primes_file)
        finally:
            primes_file.close()
    else:
        if os.path.exists(path):
            try:
                primes_file = open(path, "wt", encoding='utf-8')
            except Exception as e:
                print(e)
            else:
                write_list_to_file(prime_list, primes_file)
            finally:
                primes_file.close()
        else:
            try:
                primes_file = open("primes.txt", "wt", encoding='utf-8')
            except Exception as e:
                print(e)
            else:
                write_list_to_file(prime_list, primes_file)
            finally:
                primes_file.close()


def generate_primes(path):
    """
    This function receives a path of a file.
    The file will contain prime numbers which will be read into a list.
    The function returns two different random prime numbers - p and q.
    If an error occurs, p and q will be -1 in default.
    """

    p, q = -1, -1
    try:
        file = open(path, "rt", encoding='utf-8')
    except Exception as e:
        print(e)
    else:
        chunk_size = 256
        prime_list = file.read(chunk_size)
        while True:
            content = file.read(chunk_size)
            if not content:
                break
            prime_list += content
        prime_list = prime_list.split(',')
        prime_list = prime_list[:-2]
        while True:
            q = int(prime_list[randint(0, len(prime_list) - 1)])
            p = int(prime_list[randint(0, len(prime_list) - 1)])
            if p != q:
                break
    finally:
        file.close()
        return p, q


def generate_keys(path):
    """
    This function generates the private and public keys.
    It uses the generate_primes function.
    """

    p, q = generate_primes(path)

    # Creating the modulus - n
    n = p * q

    # Creating the totient - phi
    phi = (p - 1) * (q - 1)

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

    return (e, n), (d, n)


def encrypt(message, pub_key):
    """
    This function receives a message to encrypt and a public-key(denoted by pub_key).
    It returns a string which represents the encrypted message.
    """

    e, n = pub_key
    cipher = [ord(c) for c in message]
    cipher = [(c ** e % n) for c in cipher]
    string_cipher = [chr(c) for c in cipher]
    string_cipher = ''.join(string_cipher)
    return string_cipher


def decrypt(string_cipher, pri_key):
    """
    This function receives a message(string_cipher) to decrypt and a private-key(pri_key).
    It returns a string which represents the original message.
    """

    d, n = pri_key
    cipher = [ord(s) for s in string_cipher]
    cipher = [(s ** d % n) for s in cipher]
    decrypted_data = [chr(s) for s in cipher]
    decrypted_data = ''.join(decrypted_data)
    return decrypted_data


def main():
    generate_prime_file(800)
    pri_key, pub_key = generate_keys("primes.txt")
    message = input("Enter a message to decrypt:\t")
    encrypted_data = encrypt(message, pub_key)
    print("Encrypted data:\t{}".format(encrypted_data))
    print("Decrypted data:\t{}".format(decrypt(encrypted_data, pri_key)))


if __name__ == '__main__':
    main()
