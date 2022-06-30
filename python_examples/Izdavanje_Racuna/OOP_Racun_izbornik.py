import datetime
import os
import msvcrt as m


class Racun:
    '''
    U klasu Racun se dodaju stavke i iznos u obliku rjecnika kao argument
    Za svaki račun se automatski generira broj računa u obliku R-00-X
    Svaki račun ima i vrijeme izdavanja
    '''

    PDV = 0.25
    br_racuna = 0
    br_racuna_lista = []      # key of dict , value racun instanca

    def __init__(self, racun_stavke=None):
        self.racun_stavke = racun_stavke
        self.datum_izdavanja = datetime.datetime.now().strftime('%B %d, %Y  %H:%M:%S')
        Racun.br_racuna += 1
        self.br_racuna = f'R-00-{Racun.br_racuna}'             # br racuna se sprema za svaku instancu (str)
        Racun.br_racuna_lista.append(self.br_racuna) # sprema string svakog instanciranog računa u clasnu varijablu(lst)

        self.ukupan_iznos = 0
        for value in self.racun_stavke.values():
            self.ukupan_iznos += value

    def pdv_ukupno(self):
        osnovica = self.ukupan_iznos / (1 + self.PDV)          # namjerno self.pdv jer neke stavke mogu biti drugacije oporezivane
        return self.ukupan_iznos - osnovica

    def ispis_racuna(self):
        print('\n')
        print('*' * 50)
        print(f'\n\tRAČUN:\t\t{self.br_racuna}') #
        print(f'\tDATUM:\t\t{self.datum_izdavanja}\n')
        print('-' * 50)
        print('\n\tProizvod\t\tCijena')

        for proizvod, cijena in self.racun_stavke.items():
            if len(proizvod) < 10:
                print(f'\t{proizvod}\t\t\t{cijena} kn')
            elif len(proizvod) < 18:
                print(f'\t{proizvod}\t\t{cijena} kn')
            else:
                print(f'\t{proizvod}\t{cijena} kn')

        print()
        print('-' * 50)
        print(f'\n\tIznos PDV-a:\t{self.pdv_ukupno():.2f} kn')
        print(f'\n\tUkupan iznos:\t{self.ukupan_iznos:.2f} kn\n')
        print('*' * 50)
        print('\n')

    @classmethod             # nepotrebno classmethod jer je dio glavnog koda u njoj, cisto za vjezbu
    def novi_racun(cls):     # --> instanca_racuna = Racun.novi_racun(rjecnik)
        rjecnik = {}
        while True:
            proizvod = input(' NAZIV proizvoda: ')
            cijena = float(input(' CIJENA proizvoda (kn): '))
            rjecnik[proizvod] = cijena
            opcija = input('\n ENTER - Nastavi dodavati | s - Spremi račun | q - Izlaz \n >> ')

            if opcija == 'q':
                return  # potpuno izlazi, treba sredit ili maknut
            elif opcija == 's':
                return cls(rjecnik)
            else:
                continue


# 1
def instanca_racuna():

    while True:
        sucelje_novi_racun()
        naziv_racuna = Racun.novi_racun()      # kreira se Racun object nije nuzan zapravo @classmethod

        glavni_rjecnik[naziv_racuna.br_racuna] = naziv_racuna   # glavni_rjecnik {br racuna : racun object}
        sucelje_novi_racun()
        print(' Račun je gotov!')
        naziv_racuna.ispis_racuna()

        opcija = input(' ENTER - Dodaj novi račun | q - Izlaz\n >> ')

        if opcija == 'q':
            break
        else:
            continue


# 2
def pojedini_racun():
    clear_screen()
    print('-' * 65)
    print('\t\t\tPREGLED RAČUNA')
    print('-' * 65)
    print()

    for brracuna in Racun.br_racuna_lista:
        print(f' {brracuna}')

    print()
    broj = input(' Upiši redni broj računa: R-00-')

    if ('R-00-' + broj) in Racun.br_racuna_lista:
        glavni_rjecnik['R-00-' + broj].ispis_racuna()          # pristup Racun objectu preko glavnog rjecnika
        opcija = input(' ENTER - Pogledaj novi račun | q - Izlaz\n >> ')

        if opcija == 'q':
            return
        else:
            pojedini_racun()

    else:
        print('\n Odabrani račun NE postoji!\n')
        opcija = input(' Enter - Pokušaj ponovo | q - Izlaz\n >>')

        if opcija == 'q':
            return
        else:
            pojedini_racun()


# 3
def popis_racuna():
    clear_screen()
    print('-' * 65)
    print('\t\t\tPOPIS RAČUNA')
    print('-' * 65)
    print()

    for brracuna, instanca in glavni_rjecnik.items():
        print(f' {brracuna}   {instanca.datum_izdavanja}')

    # for i in range(len(Racun.br_racuna_lista)):
    #     print(f' {Racun.br_racuna_lista[i]}\t  {lista_instanci_racuna[i].datum_izdavanja}')
    opcija = input('\n ENTER - nazad\n >>')


# 4
def storniraj():
    clear_screen()
    print('-' * 65)
    print('\t\t\tSTORNIRANJE RAČUNA')
    print('-' * 65)
    print()
    print(' Izdani računi do sada:\n')
    for i in Racun.br_racuna_lista:
        print(f'\t{i}')
    brisi = input('\n Unesi broj računa za storniranje: R-00-')

    if ('R-00-' + brisi) in Racun.br_racuna_lista:
        Racun.br_racuna_lista.remove('R-00-' + brisi)    # brise iz Racun.liste
        del glavni_rjecnik['R-00-' + brisi]
        # lista_instanci_racuna.remove()[int(brisi)-1]
        print(f'\n Račun R-00-{brisi} je storniran.\n')
        opcija = input(' Enter - Storniraj ponovo | q - Izlaz\n >>')
        if opcija == 'q':
            return
        else:
            storniraj()
    else:
        print('\n Odabrani račun NE postoji!\n')
        opcija = input(' Enter - Pokušaj ponovo | q - Izlaz\n >>')
        if opcija == 'q':
            return
        else:
            storniraj()


def wait():
    print('\nPritisni bilo koju tipku za nastavak.\n')
    m.getch()


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def sucelje_novi_racun():
    clear_screen()
    print('-' * 65)
    print('\t\t\t NOVI RAČUN')
    print('-' * 65)
    print()


def izbornik_opcija():
    clear_screen()
    print('_' * 65)
    print()
    print('\t\t\t GLAVNI IZBORNIK')
    print('_' * 65)
    print()
    print('''
 1. NOVI RAČUN
 2. PRIKAŽI POJEDINI RAČUN
 3. POPIS RAČUNA
 4. STORNIRAJ RAČUN
 5. IZLAZ''')


glavni_rjecnik = {}   # {R-00-1: instanca racuna}

while True:

    izbornik_opcija()
    opcija = int(input('\n Odaberite opciju: '))

    if opcija == 1:
        instanca_racuna()
    elif opcija == 2:
        pojedini_racun()
    elif opcija == 3:
        popis_racuna()
    elif opcija == 4:
        storniraj()
    elif opcija == 5:
        quit()
    else:
        print('\nNepostojeća opcija. Pokušajte ponovo')
        wait()







