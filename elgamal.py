from random import randint


def prime_(n):
    if n == 2:
        return n
    if n % 2 == 0:
        return 2
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return i
    return n


def factorize(n):
    result = n
    primes = set()
    while result != 1:
        x = prime_(result)
        primes.add(x)
        result //= x
    return primes


prime = 54263660766762467
fn = prime - 1
dividers = factorize(fn)
for i in range(1, prime + 1):
    for j in dividers:
        if pow(i, int(fn / j), prime) == 1:
            break
    else:
        break
else:
    raise SystemError
rnd = randint(2, fn - 1)
y = pow(i, rnd, prime)
print('Public key:', y)
print('Private key:', rnd)
print('-------------------')
message = 54263660766762474
k = randint(2, fn - 1)
a, b = pow(i, k, prime), (pow(y, k, prime) * message) % prime
print('Encrypted message:', str(a) + ';', b)
decrypted = (b * pow(a, prime - 1 - rnd, prime)) % prime
print('Decrypted message:', decrypted)
