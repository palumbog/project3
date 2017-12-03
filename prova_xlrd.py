import xlrd
book = xlrd.open_workbook("all-euro-data-2016-2017.xls")
print("The number of worksheets is {0}".format(book.nsheets))
sheet_names = book.sheet_names()
print(book.sheet_names())
map = {}
maprev = {}
for i in range(book.nsheets):
    map[book.sheet_names()[i]] = i
    maprev[i] = book.sheet_names()[i]
print(map)
print(maprev)
num_partite = 10
campionato_italiano = book.sheets()[map["I1"]]

giornate_map = {}

for i in range(1 , campionato_italiano.nrows):
    #print(campionato_italiano.row(i))
    try:
        count = giornate_map[campionato_italiano.cell_value(rowx=i, colx=1)]
        giornate_map[campionato_italiano.cell_value(rowx=i, colx=1)] = count + 1
    except KeyError:
        prev = giornate_map[campionato_italiano.cell_value(rowx=i, colx=1) - 1]
        nex = giornate_map[campionato_italiano.cell_value(rowx=i, colx=1) + 1]
        giornate_map[campionato_italiano.cell_value(rowx=i, colx=1)] = 1

    print("DATA: {0}".format(campionato_italiano.cell_value(rowx=i, colx=1)))

print("Worksheet name(s): {0}".format(book.sheet_names()))

# sh = book.sheet_by_index(0)
# print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
# print("Cell D1 is {0}".format(sh.cell_value(rowx=1, colx=3))) #VALORE CELLA
# for rx in range(sh.nrows):
#     print(sh.row(rx))