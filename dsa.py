import random as rnd

from Crypto.Hash import SHA256
from primes_generator import PrimeGenerator


def sha256(seed):
    f = SHA256.new()
    f.update(str(seed))
    return int(f.hexdigest(), base=16)


def it_egcd(a, b):
    states = []
    while a != 0:
        states.append((a, b))
        a, b = b % a, a
        g, x, y = b, 0, 1

    for a, b in reversed(states):
        x, y = y - (b / a) * x, x

    return g, x, y


def mul_by_mod(a, b, mod):
    return (a % mod * b % mod + mod) % mod


def div_by_mod(a, b, mod):
    g, x, y = it_egcd(b, mod)
    if (g == 1):
        x = (x % mod + mod) % mod
    return mul_by_mod(a, x, mod)


class DSAResult(object):
    def __init__(self, r, s):
        self.r, self.s = r, s

    def is_valid(self, m, p, q, g, y):
        if self.r <= 0 or self.r >= q:
            return False
        if self.s <= 0 or self.s >= q:
            return False
        w = div_by_mod(1, self.s, q)
        u1 = mul_by_mod(sha256(m), w, q)
        u2 = mul_by_mod(self.r, w, q)
        v = mul_by_mod(pow(g, u1, p), pow(y, u2, p), p) % q
        return v == self.r


class DSA(object):
    def __init__(self, length, n, seed_len):
        self.length = length
        self.n = n
        self.seed_len = seed_len

    def generate(self, m):
        p, q = PrimeGenerator(10).generate(self.length, self.n, self.seed_len)
        g = pow(2, (p - 1) / q, p)
        x = rnd.randrange(1, q)
        y = pow(g, x, p)
        k = rnd.randrange(1, q)
        r = pow(g, k, p) % q
        s = mul_by_mod(div_by_mod(1, k, q), sha256(m) + x*r, q)
        return DSAResult(r, s), p, q, g, y


if __name__ == '__main__':
    obj, p, q, g, y = DSA(2048, 224, 256).generate(11111)
    print obj.is_valid(11111, p, q, g, y)
