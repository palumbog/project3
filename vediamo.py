import xlrd
from TdP_collections.map.avl_tree import AVLTreeMap
from TdP_collections.hash_table.unsorted_table_map import UnsortedTableMap
from TdP_collections.hash_table.probe_hash_map import ProbeHashMap
from enum import Enum
from array import array

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
    if(i != 18):
        avoided_divs.append(i)
max_squadre = 24 #max num di squadre in un campionato quindi 24 rappresenta 2 giornate in ipotesi di partita rinviata

class Campionati():

    class Campionato():
        #Giornata
        class Giornata():
            def __init__(self, num_giornata, campionato):
                self._num_giornata = num_giornata
                self._partite = []
                self._campionato = campionato
                self._date = []

            def stampa_partite(self):
                for p in self._partite:
                    print(p)

        #Giornata

            def __str__(self):
                str = "Num giornata " + str(self._num_giornata)

                return str

            def partite(self):
                for p in self._partite:
                    yield p

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

            def __eq__(self, other):
                return self._data == other._data and self._hometeam == other._hometeam and self._awayteam == other._awayteam

            def __str__(self):
                return self._hometeam._nome + "-" + self._awayteam._nome

        # SQUADRA
        class Squadra():
            def __init__(self, nome, campionato):
                self._nome = nome
                self._campionato = campionato
                self._partite = ProbeHashMap() #chiave la data e valore la partita

            def __eq__(self, other):
                return self._nome == other._nome

            def __gt__(self, other):
                return self._nome > other._nome

            def __str__(self):
                return self._nome
        # SQUADRA

        #CAMPIONATO
        def __init__(self, name, sheet):
            self._name = name
            self._sheet = sheet
            self._squadre = self._trova_squadre()

            #self.stampa_squadre()

            self._num_partite = sheet.nrows - 1
            self._num_partite_giornata = int(len(self._squadre) / 2)
            self._num_giornate = int(self._num_partite / self._num_partite_giornata)
            self._giornate = []
            #self._trova_giornate()
            self.riempi_giornate_di_blocchi()
            # for g in self._giornate:
            #     print("Giornata {0}".format(g._num_giornata))
            #     for p in g.partite():
            #         print(p)


        def _trova_squadre(self):
            squadre = ProbeHashMap()
            for i in range(1, max_squadre): #(sheet.nrows - 1)
                squadra_locale = self.Squadra(self._sheet.cell_value(rowx=i, colx=2), self)
                squadra_ospite = self.Squadra(self._sheet.cell_value(rowx=i, colx=3), self)
                if(not squadre.__contains__(squadra_locale._nome)):
                    #squadre.append(squadra_locale)
                    squadre[squadra_locale._nome] = squadra_locale
                if (not squadre.__contains__(squadra_ospite._nome)):
                    #squadre.append(squadra_ospite)
                    squadre[squadra_ospite._nome] = squadra_ospite
            return squadre

        def _trova_giornate(self):
            giornate = self._giornate
            giocato = []
            mancano = self._init_mancano()
            dict_mancano = {}
            num_giornata = 1

            blocco = []
            num_partite_blocco = 0

            giornate.append(self.Giornata(num_giornata, self))
            for i in range(1, self._num_partite + 1):
                squadra_locale = self._squadre[self._sheet.cell_value(rowx=i, colx=2)]
                squadra_ospite = self._squadre[self._sheet.cell_value(rowx=i, colx=3)]

                fthg = self._sheet.cell_value(rowx=i, colx=4)
                ftag = self._sheet.cell_value(rowx=i, colx=5)
                ftr = self._sheet.cell_value(rowx=i, colx=6)
                hthg = self._sheet.cell_value(rowx=i, colx=7)
                htag = self._sheet.cell_value(rowx=i, colx=8)
                htr = self._sheet.cell_value(rowx=i, colx=9)
                chiave_partita = i - 1

                data_partita = self._sheet.cell_value(rowx=i, colx=1)




                if(giocato.__contains__(squadra_locale) or giocato.__contains__(squadra_ospite)): #prox giornata
                    num_giornata += 1

                    if(len(mancano) != 0):
                        dict_mancano[num_giornata] = mancano.copy()
                else:

                    giocato.append(squadra_ospite)
                    giocato.append(squadra_locale)
                    mancano.remove(squadra_ospite)
                    mancano.remove(squadra_locale)
                    partita = self.Partita(giornate[num_giornata],data_partita,squadra_locale,squadra_ospite,fthg,ftag,ftr,hthg,htag,htr)
                    giornate[num_giornata]._partite.append(partita)
                    if(not giornate[num_giornata]._date.__contains__(data_partita)):
                        giornate[num_giornata]._date.append(data_partita)

                    self._squadre[squadra_ospite._nome]._partite[data_partita] = partita
                    self._squadre[squadra_locale._nome]._partite[data_partita] = partita

        def riempi_giornate_di_blocchi(self):
            giornate = self._giornate
            partite_da_inserire = []
            num_giornata = 0
            blocco = []
            #num_blocco = 0
            data = self._sheet.cell_value(rowx=1, colx=1)
            for i in range(self._num_giornate):
                giornate.append(self.Giornata(i + 1, self))

            #giornate.append(self.Giornata(39, self))

            for i in range(1, self._num_partite + 1):
                data_partita = self._sheet.cell_value(rowx=i, colx=1)

                squadra_locale = self._squadre[self._sheet.cell_value(rowx=i, colx=2)]
                squadra_ospite = self._squadre[self._sheet.cell_value(rowx=i, colx=3)]

                fthg = self._sheet.cell_value(rowx=i, colx=4)
                ftag = self._sheet.cell_value(rowx=i, colx=5)
                ftr = self._sheet.cell_value(rowx=i, colx=6)
                hthg = self._sheet.cell_value(rowx=i, colx=7)
                htag = self._sheet.cell_value(rowx=i, colx=8)
                htr = self._sheet.cell_value(rowx=i, colx=9)
                partita = self.Partita(giornate[num_giornata], data_partita, squadra_locale, squadra_ospite, fthg, ftag,ftr, hthg, htag, htr)

                if(data_partita >= data + 2):

                    if(len(blocco) > self._num_partite_giornata/2):
                        #giornate.append(self.Giornata(num_giornata + 1, self))
                        for p in blocco:
                            self._giornate[num_giornata]._partite.append(p)


                        num_giornata += 1

                        blocco.clear()
                        blocco.append(partita)

                    else:
                        for p in blocco:
                            partite_da_inserire.append(p)
                        blocco.clear()
                else:
                    blocco.append(partita)

                if (i == self._num_partite):

                    if (len(blocco) > self._num_partite_giornata / 2):

                        for p in blocco:
                            self._giornate[num_giornata]._partite.append(p)
                    else:
                        for p in blocco:
                            partite_da_inserire.append(p)

                data = data_partita


        def _init_mancano(self):
            mancano = []
            for s in self.squadre():
                mancano.append(s)
            return mancano


        def stampa_partite_campionato(self):
            for g in self.giornate():
                print("Giornata {0}".format(g._num_giornata))
                g.stampa_partite()

        def squadre(self):
            for s in self._squadre:
                yield self._squadre[s]

        def giornate(self):
            for g in self._giornate:
                yield g



        def stampa_squadre(self):
            print("Squadre Campionato {0}".format(self._name))
            squadre = ""
            for s in self.squadre():
                squadre += s._nome
                squadre += " "
            print(squadre)

    def __init__(self):
        self._campionati_map = self._trova_campionati(book)

    def _trova_campionati(self, book):
        campionati = ProbeHashMap()  # Mappa che ha come chiave il nome e valore un oggetto Campionato
        for i in range(book.nsheets):
            if (not avoided_divs.__contains__(i)):
                name = book.sheet_by_index(i).name
                sheet_campionato = book.sheet_by_index(i)
                # Usiamo il nome del campionato come chiave
                campionati[name] = self.Campionato(name, sheet_campionato)
        return campionati

    def stampa_squadre_campionato(self,campionato):
        self._campionati[campionato].stampa_squadre()

campionati = Campionati()
for c in campionati._campionati_map:
    campionati._campionati_map[c].stampa_partite_campionato()