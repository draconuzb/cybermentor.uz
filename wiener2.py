import math

N = 63597359086757660548411955320221160773871395432704364400607328796049485462311248266474988521127497599179652807161211775675030390944778632602973028780452701260948792975144968160045502074557471375222774999137925290681833662720120550448283374054852135310607476135235560331932579481449940617695915208667751010203
e = 23971058863507827624654241013670493863525997842009548595818737207216511537021369967614247320251209543409648952367036679016292971603553775972022076169290810518147222029078377682600110755911014499862535018091141450607142918718617237158670654898967663370268671347225275371305314377808688899206526254341490710309

C = 10392441812871137280488119885280748043606369269723916654812040857154987597452551493499078537179371093149260435708040282584278286062867985223526192587444657102839484395530989789779916539491795568550915955467225499464343147017539934550768390328795354308791658017150353039567697066043855144533499598019999407348

def continued_fraction(num, den):
    cf = []
    while den:
        q = num // den
        cf.append(q)
        num, den = den, num - q * den
    return cf

def convergents(cf):
    convs = []
    h_prev2, h_prev1 = 0, 1
    k_prev2, k_prev1 = 1, 0
    for a in cf:
        h = a * h_prev1 + h_prev2
        k = a * k_prev1 + k_prev2
        convs.append((h, k))
        h_prev2, h_prev1 = h_prev1, h
        k_prev2, k_prev1 = k_prev1, k
    return convs

cf = continued_fraction(e, N)
convs = convergents(cf)

found = False
for k, d in convs:
    if k == 0 or d == 0:
        continue
    if (e * d - 1) % k != 0:
        continue
    phi = (e * d - 1) // k
    b = N - phi + 1
    disc = b * b - 4 * N
    if disc < 0:
        continue
    sq = math.isqrt(disc)
    if sq * sq != disc:
        continue
    x1 = (b + sq) // 2
    x2 = (b - sq) // 2
    if x1 * x2 == N:
        print("FOUND d =", d)
        m = pow(C, d, N)
        mb = m.to_bytes((m.bit_length() + 7) // 8, 'big')
        print("plaintext:", mb)
        found = True
        break

if not found:
    print("Wiener attack failed to find d; trying larger convergent search / e might need mod phi reduction")
