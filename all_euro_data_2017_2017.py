import xlrd
from TdP_collections.map.avl_tree import AVLTreeMap
from enum import Enum
import array

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

book = xlrd.open_workbook("all-euro-data-2016-2017.xls")
#avoided_divs = [1,2,3,4,6,7,8,10,12,14,19]
avoided_divs = []
for i in range(22):
    if(i != 0):
        avoided_divs.append(i)
max_squadre = 24 #max num di squadre in un campionato quindi 24 rappresenta 2 giornate in ipotesi di partita rinviata

class Campionati():




    class Risultato(Enum):
        VITTORIA = "H"
        PAREGGIO = "D"
        SCONFITTA = "A"

    class Campionato():

        class Giornata():
            def __init__(self,num_giornata, campionato, partite = None):
                self._num_giornata = num_giornata
                self._partite = partite
                self._campionato = campionato
                self._date = AVLTreeMap()

            def __str__(self):
                str = "Num giornata " + str(self._num_giornata)

                return str

            def partite(self):
                for p in self._partite.positions():
                    yield p.element()._value

        class Partita():
            def __init__(self, giornata, data, hometeam, awayteam, fthg, ftag, ftr, hthg, htag, htr):
                self._giornata = giornata
                self._data = data
                self._hometeam = hometeam
                self._awayteam = awayteam
                self._fthg = fthg
                self._ftag = ftag
                self._ftr = ftr
                self._hthg = hthg
                self._htag = htag
                self._htr = htr

            def __str__(self):
                data = xlrd.xldate_as_tuple(self._data,0)
                stri = str(data[2]) + "/" + str(data[1])+"/"+str(data[0]) + " " + self._hometeam + "-" +self._awayteam
                #print(str(data[2]) + "/" + str(data[1])+"/"+str(data[0]) + " " + self._hometeam + "-" +self._awayteam )
                return stri

        class Chiave_Partita():
            def __init__(self,data, hometeam):
                self._data = data
                self._hometeam = hometeam

            def __eq__(self, other):
                return self._data == other._data and self._hometeam == other._hometeam

            def __gt__(self, other):
                return self._data > other._data

            def __lt__(self, other):
                return not self.__gt__(other)
            def __str__(self):
                return str(self._data) + str(self._hometeam)

        #SQUADRA
        class Squadra():
            def __init__(self, nome, campionato):
                self._nome = nome
                self._campionato = campionato
                self._partite = AVLTreeMap()

            def __eq__(self, other):
                return self._nome == other._nome
            def __gt__(self, other):
                return self._nome > other._nome
            def __lt__(self, other):
                return not self.__gt__(other)
            def __str__(self):
                return self._nome
        #SQUADRA

        #INIT CAMPIONATO
        def __init__(self,name = None, sheet = None):
            self._name = name
            self._sheet = sheet
            self._trova_squadre(self)
            self.init_squad_list()
            self._trova_giornate(self)
            self._num_partite = sheet.nrows - 1
            self._num_giornate = int(self._num_partite /( len(self._squadre) / 2 ))

        def init_squad_list(self):
            for s in self.squadre():
                for q in self.squadre():
                    if(q != s):
                        s._partite[q] = []
        def __str__(self):
            return self._name + " Num giornate " + str(self._num_giornate) + " Squadre " + str(len(self._squadre))

        def squadre(self):
            for s in self._squadre.positions():
                yield s.element()._value

        def giornate(self):
            for p in self._giornate.positions():
                yield p.element()._value

        def _trova_squadre(self, campionato):
            squadre = AVLTreeMap()
            for i in range(1, max_squadre): #(sheet.nrows - 1)
                squadra_locale = self.Squadra(campionato._sheet.cell_value(rowx=i, colx=2), self)
                squadra_ospite = self.Squadra(campionato._sheet.cell_value(rowx=i, colx=3), self)
                if(not squadre.__contains__(squadra_locale._nome)):
                    #squadre.append(squadra_locale)
                    squadre[squadra_locale._nome] = squadra_locale



                if (not squadre.__contains__(squadra_ospite._nome)):
                    #squadre.append(squadra_ospite)
                    squadre[squadra_ospite._nome] = squadra_ospite

            self._squadre = squadre

        def _trova_giornate(self, campionato):
            giocato = []
            mancano = []

            dict_mancano = {}
            num_da_recup = 0
            squadre_rec = []
            for s in campionato._squadre:
                mancano.append(s)

            self._giornate = AVLTreeMap()
            num_giornata = 0
            giornata_succ = False
            self._giornate[num_giornata] = self.Giornata(num_giornata, campionato)
            self._giornate[num_giornata]._partite = AVLTreeMap()
            for i in range(1, campionato._sheet.nrows):

                if (num_giornata == 25):
                    print("Lol")
                fthg = campionato._sheet.cell_value(rowx=i, colx=4)
                ftag = campionato._sheet.cell_value(rowx=i, colx=5)
                ftr = campionato._sheet.cell_value(rowx=i, colx=6)
                hthg = campionato._sheet.cell_value(rowx=i, colx=7)
                htag = campionato._sheet.cell_value(rowx=i, colx=8)
                htr = campionato._sheet.cell_value(rowx=i, colx=9)
                # chiave_partita = self.Chiave_Partita(data_partita,hometeam)  PROBLEMA di inserimento di questa chiave in AVL
                chiave_partita = i - 1

                data_partita = campionato._sheet.cell_value(rowx=i, colx=1)
                #giorno_partita = xlrd.xldate_as_tuple(data_partita,0)[2]

                hometeam = campionato._sheet.cell_value(rowx=i, colx=2)
                hometeam_squadra = campionato._squadre[hometeam]
                awayteam = campionato._sheet.cell_value(rowx=i, colx=3)
                awayteam_squadra = campionato._squadre[awayteam]
                contains_hometeam = giocato.__contains__(hometeam)
                contains_awayteam = giocato.__contains__(awayteam)
                if(contains_hometeam or contains_awayteam): # prossima giornata
                    giornata_succ = True
                else:
                    giornata_succ = False

                if(not giornata_succ):
                    giocato.append(hometeam)
                    giocato.append(awayteam)
                    mancano.remove(hometeam)
                    mancano.remove(awayteam)
                    self._giornate[num_giornata]._date[data_partita] = True
                    self._giornate[num_giornata]._partite[chiave_partita] = self.Partita(self._giornate[num_giornata],data_partita,hometeam,awayteam,fthg,ftag,ftr,hthg,htag,htr)
                    home = campionato._squadre[hometeam]

                    campionato._squadre[hometeam_squadra]._partite[awayteam_squadra].append(self._giornate[num_giornata]._partite[chiave_partita])
                    campionato._squadre[awayteam_squadra]._partite[hometeam_squadra] = [self._giornate[num_giornata]._partite[chiave_partita]]
                else:
                    if (len(mancano) != 0):
                        print("Giornata {0}".format(num_giornata))
                        dict_mancano[num_giornata] = mancano.copy()
                        for i in mancano:
                            print(i)
                    mancano.clear()
                    for s in campionato._squadre:
                        mancano.append(s)
                    num_giornata += 1
                    giocato.clear()
                    giocato.append(hometeam)
                    giocato.append(awayteam)
                    mancano.remove(hometeam)
                    mancano.remove(awayteam)

                    self._giornate[num_giornata] = self.Giornata(num_giornata, campionato)
                    self._giornate[num_giornata]._partite = AVLTreeMap()
                    self._giornate[num_giornata]._date[data_partita] = True
                    self._giornate[num_giornata]._partite[chiave_partita] = self.Partita(self._giornate[num_giornata], data_partita, hometeam, awayteam, fthg, ftag, ftr, hthg, htag, htr)
                    campionato._squadre[hometeam]._partite[awayteam] = [self._giornate[num_giornata]._partite[chiave_partita]]
                    campionato._squadre[awayteam]._partite[hometeam] = [self._giornate[num_giornata]._partite[chiave_partita]]
                # try:
                #     data_partita_succ = campionato._sheet.cell_value(rowx=i+1, colx=1)
                #     giorno_partita_succ = xlrd.xldate_as_tuple(data_partita_succ,0)[2]
                # except IndexError:
                #     break
                # if(giorno_partita_succ == giorno_partita or giorno_partita_succ == giorno_partita + 1):
                #     giornata_succ = False
                # else:
                #     giornata_succ = True





    #INIT CAMPIONATI
    def __init__(self):
        self._campionati = {} # Mappa che ha come chiave il nome e valore un oggetto Campionato
        for i in range(book.nsheets):
            if(not avoided_divs.__contains__(i)):
                name = book.sheet_by_index(i).name
                sheet_campionato = book.sheet_by_index(i)
                #Usiamo il nome del campionato come chiave
                self._campionati[name] = self.Campionato(name,sheet_campionato)

    def __str__(self):
        str = ""
        for k in self._campionati:
            campionato =  self._campionati[k]
            stri = campionato.__str__()
            str += k + " : "+ stri + "\n"
        return str


    def __iter__(self):
        for i in self._campionati.keys():
            yield self._campionati[i]


    #Esercizio 1
    def stampa_squadre_div(self, div):
        try:
            campionato = self._campionati[div]
            print("Squadre Campionato " + (div)+".")
            print("Tot squadre: "+str(len(campionato._squadre)))
            print("Giornate: "+str(campionato._num_giornate))
            for squadra in campionato.squadre():
                pass
                print(squadra,end="\n")
            print("\n")
        except Exception:
            print("Campionato {0} non trovato".format(div))

    def __len__(self):
        return len(self._campionati)


campionati = Campionati()
for c in campionati:
    #if c._name == "I1":
    print(bcolors.OKBLUE + "Campionato {0}".format(c._name) + bcolors.ENDC)
    print("Giornate: {0}".format(len(c._giornate)))
    for g in c.giornate():
        print(bcolors.FAIL + "Giornata {0}. Num partite {1}".format(g._num_giornata,len(g._partite)) + bcolors.ENDC)
        for p in g.partite():
            print(p)
for campionato in campionati.campionati():
    print(campionato)
    campionati.stampa_squadre_div(campionato._name)
