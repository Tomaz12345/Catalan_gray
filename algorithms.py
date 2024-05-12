def is_dyck_word(word):
    num_ones = 0
    num_zeros = 0

    for i, w in enumerate(word):
        if w == "1":
            num_ones += 1
        else:
            num_zeros += 1

        if num_zeros > num_ones:
            return False
    return True

def coolex(n):
    #binary: binarni niz s toliko 0 kot 1
    binary = "1" * n + "0" * n
    binary0 = binary
    
    while True:
        #print(binary)
        if is_dyck_word(binary):
            yield binary

        if "01" not in binary:
            # na zacetek dam zadnjega
            binary = binary[-1:] + binary[:-1]
        else:
            indexof01 = binary.index("01")
            
            if indexof01 + 2 < len(binary):
                # na zacetek dam tistega,
                # ki sledi prvi pojavitvi "01"
                binary = binary[indexof01+2] \
                        + binary[:indexof01+2] \
                        + binary[indexof01+3:]
            else:
                # na zacetek dam zadnjega
                binary = binary[-1:] + binary[:-1]
        
        if binary == binary0:
            # ko se ponovi zacetni element,
            # zakljucim
            return

def num_ones_zeros(binary):
    ones = 0
    zeros = 0
    for i, b in enumerate(binary):
        if b == "1":
            if zeros > 0:
                break
            ones += 1
        else:
            zeros += 1
    return ones, zeros

def coolex2(n):
    """
    n: dolzina binarnega niza
    """

    first_dyck_word = "10" + "1" * (n-1) + "0" * (n-1)
    dyck_word = first_dyck_word

    while True:
        yield dyck_word
        p, q = num_ones_zeros(dyck_word)
        
        if p == n and q == n:
            return
        
        if dyck_word[p+q+1] == "1":
            dyck_word = "11" + "1" * (p-1) + "0" * q + "1" + dyck_word[p+q+2:]
        elif dyck_word[p+q+1] == "0" and p == q:
            dyck_word = "11" + "1" * (p-1) + "0" * q + "0" + dyck_word[p+q+2:]
        else: # p > q
            dyck_word = "10" + "1" * (p-1) + "0" * q + "1" + dyck_word[p+q+2:]

    
    return


def first_two_blocks_sizes(dyck):
    size_1s = 0
    size_0s = 0
    
    while dyck[size_1s] == "1":
        size_1s += 1
    size_0s += 1
    
    while dyck[size_1s+size_0s] == "0":
        size_0s += 1
    # snd_1s_index=size_0s, size_1s
    
    return size_1s, size_0s

def dyck_gen(n):
    # n: polovicna dolzina
    dyck = "10" + "1" * (n-1) + "0" * (n-1)
    
    while True:
        yield dyck
        size_1s, size_0s = first_two_blocks_sizes(dyck)
        snd_1s = size_0s + size_1s
        after = dyck[snd_1s:(snd_1s+2)]
        remainder = dyck[(snd_1s+2):]
        
        if after == "11":
            dyck = "11" + "1" * (size_1s-1) \
                + "0" * (size_0s) + "1" + remainder
        
        elif after == "10":
            if size_1s == size_0s:
                dyck = "11" + "1" * (size_1s-1) \
                    + "0" * (size_0s) + "0" + remainder
            
            else:
                # size_1s > size_0s
                dyck = "10" + "1" * (size_1s-1) \
                    + "0" * (size_0s) + "1" + remainder
        
        if dyck == "1" * n + "0" * n:
            # koncamo
            yield dyck
            return

#for e in dyck_gen(3):
    #print(e)


def closing(dyck):
    stack = 0
    for i, d in enumerate(dyck):
        if d == "1":
            stack += 1
        else:
            #d == "0"
            stack -= 1
        
        if stack == 0:
            return i

def dyck2triangulation(dyck, nodes=None):
    n = int(len(dyck)/2)
    # [−2,−1,0,1,...,n−1]
    # #[y,x,v0,v1,...,v(n−1)]
    if nodes is None:
        nodes = list(range(-2,n))
    edges = []
    #trikotnik ima prazno triangulacijo
    
    if len(nodes) <= 3:
        return edges
    index_of_closing = closing(dyck)
    # (sig0)sig1
    sig0 = dyck[1:index_of_closing]
    sig1 = dyck[(index_of_closing+1):]
    
    yi = 0
    xi = 1
    k = int(len(sig0)/2) #vk
    ki = k + 2
    
    if len(sig0) == 0:
        edges += [(nodes[yi],nodes[ki])]
        nodes1 = [nodes[yi]]+nodes[ki:]
        edges += dyck2triangulation(sig1,nodes1)
    
    if len(sig1) == 0:
        edges += [(nodes[xi],nodes[ki])]
        nodes0 = [nodes[ki]] + nodes[xi:ki]
        edges += dyck2triangulation(sig0,nodes0)
    
    return edges

#print(dyck2triangulation("10101100"))

def vrni_str_motzkin(w):
    if type(w) == list:
        return "".join(map(str,w)).replace("-1", "-")
    else:
        return w.replace("-1", "-")

def motzkin(k,m):
    n = 2 * k + m
    # Motzkinova beseda s fiksno vsebino ima k enic, k nicel
    # in m pomisljajev("−") ter velja, da vsak prefix vsebuje
    # najvec toliko nicel kolikor enic
    # v nasem primeru je −1="−" za lazje racunanje
    b = [2] + [1] * k + [-1] * m + [0] * k
    x = n - 1
    y = m + k + 1
    z = k + 1
    
    #zacetna_motzkin = b[1:].replace("-1", "-")
    zacetna_motzkin = vrni_str_motzkin(b[1:])
    #for i in range(len(zacetna_motzkin)):
    #    if zacetna_motzkin[i] == -1:
    #        zacetna_motzkin[i] = "-"

    #izpisi = ["zacetnabeseda: "]
    #izpisi.extend(zacetna_motzkin)
    #print("".join(izpisi))
    yield zacetna_motzkin
            
    while x < n-1 or b[x] != 1:
        q = b[x-1]
        r = b[x]
        if x + 1 <= n:
            p = b[x+1]
        b[x] = b[x-1]
        b[y] = b[y-1]
        b[z] = b[z-1]
        b[1] = r
        y += 1
        z +=1
        x += 1
                
        if p == 0:
            if z-2 > (x-y):
                b[1] = 1
                b[2] = 0
                b[x] = r
                z = 2
                y = 2
                x = 3
            else:
                x += 1
                
        elif x <= n and \
            (q == 1 or (q == -1 and (b[x] == -1 or b[x] == 0)) \
            or (q == 0 and b[x] == 0)):
            b[x] = 1
            b[x-1] =- 1
            b[1] =- 1
            z = 1
        if b[2] > b[1]:
            z = 1
            y = 2
            x = 2
        #print(b[1:])
        #print(vrni_str_motzkin(b[1:]))
        yield vrni_str_motzkin(b[1:])
    
    return

    """koncna_motzkin = vrni_str_motzkin(b[1:])
    #for i in range(len(koncna_motzkin)):
    #    if koncna_motzkin[i] == -1:
    #        koncna_motzkin[i] = "-"
    izpisi2 = ["koncnabeseda: "]
    izpisi2.extend(koncna_motzkin)
    print("".join(izpisi2))"""