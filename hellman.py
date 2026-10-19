import random

#teste de primalidade (Miller-Rabin) 
def eh_primo(n, testes=20):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13):
        if n % q == 0:
            return n == q
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(testes):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

#gera p primo "seguro": p = 2*q + 1, com q primo
def gera_p(bits):
    while True:
        q = random.getrandbits(bits - 1) | (1 << (bits - 2)) | 1
        p = 2 * q + 1
        if eh_primo(q) and eh_primo(p):
            return p, q

# acha raiz primitiva módulo p 
# como p-1 = 2*q, g é raiz primitiva se g^2 != 1 e g^q != 1 (mod p)
def acha_g(p, q):
    g = 2
    while pow(g, 2, p) == 1 or pow(g, q, p) == 1:
        g += 1
    return g

#Diffie-Hellman 
p, q = gera_p(256)
g = acha_g(p, q)

a = random.randrange(2, p - 1)   # segredo de Alice
b = random.randrange(2, p - 1)   # segredo de Bob

A = pow(g, a, p)   # Alice envia A para Bob
B = pow(g, b, p)   # Bob envia B para Alice

s_alice = pow(B, a, p)   # Alice calcula s
s_bob = pow(A, b, p)     # Bob calcula s

print("p =", p)
print("g =", g)
print("a =", a)
print("b =", b)
print("A =", A)
print("B =", B)
print("s (Alice) =", s_alice)
print("s (Bob)   =", s_bob)
print("Segredos iguais?", s_alice == s_bob)