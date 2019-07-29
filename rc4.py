import crypto


text = 'Hello, Привет!'.encode('utf-8')
print(list(map(lambda a: hex(a), text)))


p, q = crypto.get_rc4_keys(16, 4)
print(p)
f = 20533365656
noise = []
for i in range(len(text)):
    n = crypto.n_keys(p, q, prev=f)
    noise.append(hex(n))
    f = n

encoded = []
for i, j in zip(text, noise):
    encoded.append(hex(i ^ int(j, 16)))
print(encoded)
print(noise)
decoded = []
string = bytearray()
for i, j in zip(encoded, noise):
    string.append(int(i, 16) ^ int(j, 16))
print(string.decode('utf-8'))
