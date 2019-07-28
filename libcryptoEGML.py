import random
import math


def eratosthenes(N):
    array = [x for x in range(N + 1)]
    for i in range(2, int(math.sqrt(len(array)) + 1)):
        if array[i]:
            for index in range(i ** 2, len(array), i):
                if array[index] and index != i:
                    array[index] = False
    return tuple(filter(lambda a: a, array))


def toBinary(n):
    return tuple(map(int, tuple(str(bin(n))[2:])))


def MillerRabin(n, s):
    for j in range(1, s + 1):
        a = random.randint(1, n - 1)
        b = toBinary(n - 1)
        d = 1
        for i in range(len(b) - 1, -1, -1):
            x = d
            d = (d * d) % n
            if d == 1 and x != 1 and x != n - 1:
                return True  # Составное
            if b[i] == 1:
                d = (d * a) % n
                if d != 1:
                    return True  # Составное
                return False  # Простое


def ferma(n, a):
    return pow(a, n - 1, n) == 1


def prime(n):
    if n % 2 == 0:
        return False
    for prime_ in primes:
        if n % prime_ == 0 and n != prime_:
            return False
    for i in range(50):
        a = random.randint(0, 10 ** 12)
        if not MillerRabin(n, a) or not ferma(n, a):
            break
    else:
        return True
    return False


primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
          109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
          233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
          367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
          499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641,
          643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
          797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
          947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063,
          1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201,
          1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319,
          1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471,
          1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597,
          1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723,
          1733, 1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873,
          1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999]


def get_keys(size, modulo=4):
    p = random.randint(10 ** size, 10 ** (size + 1))
    while not prime(p) or p % modulo != 3:
        p = random.randint(10 ** size, 10 ** (size + 1))
    q = random.randint(10 ** size, 10 ** (size + 1))
    while not prime(q) or q % modulo != 3 or p == q:
        q = random.randint(10 ** size, 10 ** (size + 1))
    return p, q


def n_keys(p, q, prev=None, pair=None):
    assert (prev is None) ^ (pair is None)
    if prev is None:
        return pow(pair[0], pow(2, pair[1], (p - 1) * (q - 1)), p * q)
    else:
        return pow(prev, 2, p * q)
