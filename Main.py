import os
import re
from datetime import date
from pollini import polliniList


def print_pollini():
    for p in polliniList:
        if p.tot > 0:
            print(f'Famiglia: {p.famiglia}, Nome: {p.nome}, Lettera: {p.lettera}, Tot: {p.tot}')


def set_tot_pollini(input_val):
    for i in input_val:
        for polline in polliniList:
            if polline.lettera == i:
                polline.tot += 1


def is_valid_chars(input_val):
    if not re.match('[a-zA-Z]', input_val):
        print("Errore caratteri non consentiti")
        input("Premi invio per continuare ...")
        return False
    return True


def write_to_file():
    path = os.environ['USERPROFILE'] + ("/Desktop/")
    filename = date.today().strftime("%Y%m%d") + "_pollini_save.txt"
    f = open(os.path.join(path, filename), "a")
    for p in polliniList:
        if p.tot != 0:
            f.writelines(f'{p.famiglia}, Tot: {p.tot}\n')
    f.close()


if __name__ == '__main__':
    while True:
        os.system('cls')
        user_input = input("Inserisci la stringa da valutare (\"exit\" per uscire dal programma):\n")
        if user_input == "exit":
            break
        if not is_valid_chars(user_input):
            continue
        set_tot_pollini(user_input)
        print_pollini()
        write_to_file()
        input("Premi invio per continuare...")

print('Arrivederci!')
