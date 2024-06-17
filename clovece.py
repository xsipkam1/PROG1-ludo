#===========================================================================================#
# Názov:    clovece.py                                                                      #
# Popis:    Hra človeče nehnevaj sa medzi dvoma botmi.                                      #
# Autor:    Michal Šípka                                                                    #
# Dátum:    20.11.2021                                                                      #
#===========================================================================================#

#naimportovanie potrebných knižníc
import random

#============================================================================================#
#                                    Definíce funkcií                                        #
#============================================================================================#

#vygeneruje a vráti šachovnicu o veľkosti n x n
def vygeneruj_sachovnicu(n):
    sachovnica = []

    for i in range(n):
        sachovnica.append([" " for i in range(n)])

    for i in range(n//2):
        sachovnica[i][(n//2)-1] = "*"
        sachovnica[i+1][n//2] = "D"
        sachovnica[i][(n//2)+1] = "*"

        sachovnica[(n//2)-1][i] = "*"
        sachovnica[n//2][i+1] = "D"
        sachovnica[(n//2)+1][i] = "*"

        sachovnica[((n//2)+1)+i][(n//2)-1] = "*"
        sachovnica[(n//2)+i][n//2] = "D"
        sachovnica[((n//2)+1)+i][(n//2)+1] = "*"

        sachovnica[(n//2)-1][((n//2)+1)+i] = "*"
        sachovnica[n//2][(n//2)+i] = "D"
        sachovnica[(n//2)+1][((n//2)+1)+i] = "*"

    sachovnica[0][n//2] = "*"
    sachovnica[n//2][0] = "*"
    sachovnica[n-1][n//2] = "*"
    sachovnica[n//2][n-1] = "*"
    sachovnica[n//2][n//2] = "X"
    return sachovnica

#očíslovanie po stranách šachovnice pre lepšiu orientáciu
def ocislovanie(i):
    x = str(i)
    if len(x) > 1:
        print(x[len(x)-1], end=" ")
    else:
        print(x, end=" ")

#nakreslenie šachovnice spolu s aktuálnymi polohami hráča A a hráča B
def nakresli_sachovnicu(sachovnica,y_A,x_A,y_B,x_B):
    sachovnica[y_A][x_A] = "A"
    sachovnica[y_B][x_B] = "B"

    #horizontálne očíslovanie
    print("  ", end="")
    for i in range(n):
        ocislovanie(i)
    print()

    if pocet_A_v_domceku > 0:
        for i in range(pocet_A_v_domceku):
            sachovnica[n//2-(i+1)][n//2] = "A"
    if pocet_B_v_domceku > 0:
        for i in range(pocet_B_v_domceku):
            sachovnica[n//2+(i+1)][n//2] = "B"

    #vertikálne očíslovanie + výpis šachovnice po riadkoch
    r=0
    for pole in sachovnica:
        ocislovanie(r)
        print(" ".join(pole))
        r+=1

#zistí a vráti počet políčok šachovnice
def zisti_pocet_policok(sachovnica):
    pocet_policok = -1
    pocet_domcekov = 0
    for pole in sachovnica:
        for policko in pole:
            if policko == "*":
                pocet_policok += 1
            if policko == "D":
                pocet_domcekov += 1
    pocet_domcekov_A = int(pocet_domcekov/4)
    policka_total = pocet_policok+pocet_domcekov_A
    return policka_total

#do zoznamu načíta presnú sekvenciu súradníc, po ktorých sa hráč A pohybuje, a potom zoznam vráti
def pohyb_A():
    z=[]
    for i in range(n//2-1):
        z.extend([[i,n//2+1]])
    for i in range(n//2):
        z.extend([[n//2-1,n//2+1+i]])

    z.extend([[n//2,n-1]])

    for i in range(n//2-1):
        z.extend([[n//2+1,n-1-i]])
    for i in range(n//2):
        z.extend([[n//2+1+i,n//2+1]])

    z.extend([[n-1,n//2]])

    for i in range(n//2-1):
        z.extend([[n-1-i,n//2-1]])
    for i in range(n//2):
        z.extend([[n//2+1,n//2-1-i]])

    z.extend([[n//2,0]])

    for i in range(n//2-1):
        z.extend([[n//2-1,i]])
    for i in range(n//2):
        z.extend([[n//2-1-i, n//2-1]])

    z.extend([[0,n//2]])

    for i in range(n//2-1):
        z.extend([[i+1,n//2]])

    return z

#pretransformuje zoznam so sekvenciou súradníc hráča A na zoznam so sekvenciou súradníc hráča B,
#a potom tento pretransformovaný zoznam vráti
def pohyb_B(z, pocet_policok):
    order_B = []
    pocet_policok=pocet_policok-((n//2)-2)
    index = pocet_policok//2
    while index < len(z):
        order_B.append(z[index])
        index+=1
        if index == len(z)-(n//2-1):
            index = 0
        if index == (pocet_policok//2):
            break
    for i in range(1,n//2):
        order_B.extend([[n-(i+1),n//2]])
    return order_B

#funkcia vráti súradnice 'y' a 'x', na ktoré sa hráč presunie, keď sa dostane do domčeka
def domceky(hrac, pocet_v_domceku):
    for i in range(1,n//2):
        if hrac == "A":
            if pocet_v_domceku == i:
                y=n//2-i
                x=n//2
                break
        elif hrac == "B":
            if pocet_v_domceku == i:
                y=n//2+i
                x=n//2
                break
    return y,x

#funkcia vygeneruje náhodné číslo od 1 do 6, a potom ho vráti
def hod(hrac):
    hod = random.randint(1,6)
    print("Hrac", hrac, "hodil", hod)
    return hod

#funckia vráti súradnice 'y' a 'x', na ktoré sa hráč presunie, keď hodí kockou
def posun(moves, pozicia):
    y = moves[pozicia][0]
    x = moves[pozicia][1]
    return y,x

#funkcia skontroluje, či hráč dostal všetky figúrky do domčeka
def check_domceky(hrac, pocet_v_domceku):
    if pocet_v_domceku == (n-3)/2:
        print("Hrac", hrac, "dostal vsetky figurky do domcekov.")
        return True

#============================================================================================#
#                                    Hlavný cyklus hry                                       #
#============================================================================================#

while True:
    try:
        n=int(input("Zadaj velkost sachovnice: "))
        if n%2==0:
            print("Velkost sachovnice musi byt neparne cislo.")
            continue
        elif n<5:
            print("Velkost sachovnice musi byt minimalne 5.")
            continue
        else:
            #štartovné súradnice hráča A, súčet hodov hráča A, počet figúrok hráča A v domčeku
            y_A = 0
            x_A = n//2+1
            sucet_A = 0
            pocet_A_v_domceku = 0

            #štartovné súradnice hráča B, súčet hodov hráča B, počet figúrok hráča B v domčeku
            y_B = n-1
            x_B = n//2-1
            sucet_B = 0
            pocet_B_v_domceku = 0

            a = vygeneruj_sachovnicu(n)
            h_A = zisti_pocet_policok(a)
            h_B = zisti_pocet_policok(a)
            p_A = pohyb_A()
            p_B = pohyb_B(p_A, h_B)
            nakresli_sachovnicu(a,y_A,x_A,y_B,x_B)
            print()
            turn_A = True #ak turn_A = True, hráč A začína prvý, ak turn_A = False, hráč B začína prvý
            koniec = False

            while not koniec:
                while turn_A == True:
                    hod_A=hod("A")
                    sucet_A += hod_A

                    #ak súčet hodov hráča A prekročí počet políčok, tak to znamená, že sa dostal do domčeka
                    if sucet_A >= h_A:
                        pocet_A_v_domceku += 1
                        sucet_A = 0
                        h_A -= 1
                        y_A,x_A = domceky("A",pocet_A_v_domceku)
                        a = vygeneruj_sachovnicu(n)
                        nakresli_sachovnicu(a,y_A,x_A,y_B,x_B)

                        if check_domceky("A", pocet_A_v_domceku):
                            koniec = True
                            break

                        y_A = 0
                        x_A = n//2+1
                        print()
                        turn_A = False
                        break

                    a = vygeneruj_sachovnicu(n)
                    y_A,x_A = posun(p_A,sucet_A)
                    nakresli_sachovnicu(a,y_A,x_A,y_B,x_B)
                    print()

                    #ak hráč A stúpi na políčko kde je hráč B, hráč B sa presunie na štart a hráč A hádže kockou znova
                    if y_A == y_B and x_A == x_B:
                        if y_B != n-1 and x_B != n//2-1: #neplatí, ak hráč A stúpi na štartovnú pozíciu hráča B
                            sucet_B = 0
                            y_B = n-1
                            x_B = n//2-1
                            a = vygeneruj_sachovnicu(n)
                            nakresli_sachovnicu(a,y_A,x_A,y_B,x_B)
                            print()
                            continue

                    turn_A = False
                    break

                while turn_A == False:
                    hod_B=hod("B")
                    sucet_B += hod_B

                    #ak súčet hodov hráča B prekročí počet políčok, tak to znamená, že sa dostal do domčeka
                    if sucet_B >= h_B:
                        pocet_B_v_domceku += 1
                        sucet_B = 0
                        h_B -= 1
                        y_B,x_B=domceky("B",pocet_B_v_domceku)
                        a = vygeneruj_sachovnicu(n)
                        nakresli_sachovnicu(a,y_A,x_A,y_B,x_B)
                        if check_domceky("B", pocet_B_v_domceku):
                            koniec = True
                            break

                        y_B = n-1
                        x_B = n//2-1
                        print()
                        turn_A = True
                        break

                    a = vygeneruj_sachovnicu(n)
                    y_B,x_B = posun(p_B,sucet_B)
                    nakresli_sachovnicu(a,y_A,x_A,y_B,x_B)
                    print()

                    #ak hráč B stúpi na políčko kde je hráč A, hráč A sa presunie na štart a hráč B hádže kockou znova
                    if y_B == y_A and x_B == x_A:
                        if y_A != 0 and x_A != n//2+1:  #neplatí, ak hráč B stúpi na štartovnú pozíciu hráča A
                            sucet_A = 0
                            y_A = 0
                            x_A = n//2+1
                            a = vygeneruj_sachovnicu(n)
                            nakresli_sachovnicu(a,y_A,x_A,y_B,x_B)
                            print()
                            continue

                    turn_A = True
                    break
        break
    except:
        continue
