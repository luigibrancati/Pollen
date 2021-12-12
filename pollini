class Pollini:
    def __init__(self, famiglia, nome, lettera, tot):
        self.famiglia = famiglia
        self.nome = nome
        self.lettera = lettera
        self.tot = tot

polliniList=[]

alfabeto = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','ñ','á','é','í','ó','ú']

pollen_list = {"Aceraceae":0, "Cannabbaceae": 0, "Betulaceae":[{"Alnus":0, "Betula":0}], \
"Chenopodiaceae/Amaranthaceae":0 ,"Compositae":[{"Ambrosia": 0, "Artemisia": 0}], "Corylaceae":[{"Carpinus" : 0, "Coryllus avellana":0}],\
"Cupressaceae/Taxaceae":0, "Fagaceae": [{"Castanea sativa":0, "Fagus sylvatica":0, "Quercus":0}], "Graminae":0, "Oleaceae":[{"Fraxinus":0, "Olea":0}],\
"Pinaceae":0, "Plantaginaceae":0, "Platanaceae":0, "Polygonaceae":0, "Salicaceae":[{"Populus":0, "Salix": 0}], "Ulmaceae":0, "Uritcaceae":0, "Alternaria":0}

def generate_obj_pollen(pollen_list):
    for key in pollen_list:
        polliniList.append(Pollini(key,"", " ", 0))
        if type(pollen_list[key]) == list:
           for x in pollen_list[key]:
               for i in x:
                   polliniList.append(Pollini(i, " ", " ", 0))
    return polliniList

generate_obj_pollen(pollen_list)

def assign_letterToPollen(polliniList):
    for p in range(len(polliniList)):
        polliniList[p].lettera = alfabeto[p]
    return polliniList

assign_letterToPollen(polliniList)
