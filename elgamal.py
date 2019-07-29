from random import randint
import crypto

prime = 54263660766762467
fn = prime - 1
dividers = crypto.factorize(fn)
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
message = 24346
k = randint(2, fn - 1)
a, b = pow(i, k, prime), (pow(y, k, prime) * message) % prime
print('Encrypted message:', str(a) + ';', b)
decrypted = (b * pow(a, prime - 1 - rnd, prime)) % prime
print('Decrypted message:', decrypted)
