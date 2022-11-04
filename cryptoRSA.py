import secrets


# Quanto maior, mais seguro. No entanto, grandes números consomem poder de processamento brutal
MAX_PRIME_BITS = 8
MIN_PRIME_BITS = 6

# Tamanho de cada letra criptografada
CHAR_SIZE = 6


# Esta função gera um número primo aleatório com base na biblioteca de segurança de segredos e no intervalo de nbits
def Random_prime():
    random_number = secrets.randbits(MAX_PRIME_BITS)

    if (random_number < (2 ** MIN_PRIME_BITS)) or (random_number % 2 == 0):
        return Random_prime()

    for i in range(2, random_number // 2):
        if (random_number % i) == 0:
            return Random_prime()

    return random_number


# Esta função chama Random_prime() para gerar dois números primos distintos p e q
def Random_p_q():
    p = Random_prime()
    q = Random_prime()
    if p == q:
        return Random_p_q()
    else:
        return p, q


def MDC(a, b):
    if a == 0:
        return b
    else:
        gdc = MDC(b % a, a)
        return gdc


# A função totiente de Euler descobre quantos números são primos do espaço Phi(x)
def Phi(p, q):
    return (p - 1) * (q - 1)


# e != 1, 1 < e < Phi
def publicKey(phi):
    id = False
    p_key = 0
    i = 1 + secrets.randbelow(phi - 1) % 100
    while id != True:
        i += 1
        if MDC(phi, i) == 1:
            id = True
            p_key = i
    return p_key


# Gerador keys
def generator():
    p, q = Random_p_q()
    fi = Phi(p, q)
    public_key = publicKey(fi)
    modular_key = p * q

    # Este loop encontra o inverso modular de 'e' que satisfaz a equação d*e % Phi = 1
    private_key = fi // public_key
    key = False
    while key == False:
        private_key += 1
        if ((private_key * public_key) % fi) == 1:
            key = True

    return public_key, modular_key, private_key, fi


# Encriptador
def lock(text, e, n):
    c = ""
    for i in text:
        x = (ord(i) ** e) % n
        k = CHAR_SIZE - len(str(x))

        while k > 0:
            c += "0"
            k -= 1

        c += str(x)

    return c


# Decriptador
def unlock(text, d, n):
    m = ""
    u = ""

    for i in text:
        u += i

        if len(u) == CHAR_SIZE:
            m += chr((int(u) ** d) % n)
            u = ""

    return m
