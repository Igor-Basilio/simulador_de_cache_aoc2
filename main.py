# ===================================================================================
#                             Simulador de Cache
# ===================================================================================
#                        __====-_  _-====
#                  _--^^^#####//      \\#####^^^--_
#               _-^##########// (    ) \\##########^-_
#              -############//  |\^^/|  \\############-
#            _/############//   (@::@)   \\############\_
#           /#############((     \\//     ))#############\
#          -###############\\    (oo)    //###############-
#         -#################\\  / `' \  //#################-
#        -###################\\/  (|)  \//###################-
#       _#/|##########/\######(   / | \   )######/\##########|\#_
#       |/ |#/\#/\#/\/  \#/\#/\ (  | |  ) /\#/\#/\  \/\/\#/\| \|
#       |/  |/  \|/  |/     |/  |/  |/   |/     |/  |/  |/  |/  \|/
#
# Authors: Igor Basilio & Lucas Bayer
# ===================================================================================

import sys
import math
import random

nsets = 0
bsize = 0
assoc = 0
subs = None
flag_saida = False


class Algoritmo:
    R = 1
    LRU = 2
    FIFO = 3


hits = 0
acessos = 0
misses_conflito = 0
misses_compulsorios = 0
misses_capacidade = 0

def main():

    global nsets, bsize, assoc, subs, flag_saida, acessos
    global hits,  acessos, misses, misses_compulsorios
    global misses_conflito, misses_capacidade

    args = sys.argv[1:]
    if len(args) != 6:
        print("Uso :\nsimulador_cache <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada")
        sys.exit(1)

    try:
        nsets = int(args[0])
    except ValueError:
        print("Número de conjuntos inválido.")
        sys.exit(1)

    try:
        bsize = int(args[1])
    except ValueError:
        print("Tamanho do bloco inválido.")
        sys.exit(1)

    try:
        assoc = int(args[2])
    except ValueError:
        print("Associatividade inválida.")
        sys.exit(1)

    if args[3] == "R":
        subs = Algoritmo.R
    elif args[3] == "LRU":
        subs = Algoritmo.LRU
    elif args[3] == "FIFO":
        subs = Algoritmo.FIFO
    else:
        print("Algortimo de substituição inválido.")
        sys.exit(1)

    try:
        temp = int(args[4])
    except ValueError:
        print("Flag de saída deve ser 0 ou 1.")
        sys.exit(1)

    if temp == 0:
        flag_saida = False
    elif temp == 1:
        flag_saida = True
    else:
        print("Flag de saída deve ser 0 ou 1.")
        sys.exit(1)

    #class partition():

    #   def __init__(self, assoc):
    #       self.assoc = assoc
    #        self.tag = [0] * assoc
    #        self.val = [0] * assoc

    #cache_ = [partition(assoc) for _ in range(nsets)]

    cache_val = [0] * (nsets * assoc)
    cache_tag = [0] * (nsets * assoc)

    n_bits_offset = int(math.log(bsize, 2))
    n_bits_indice = int(math.log(nsets, 2))

    try:

        with open(args[5], "rb") as file:
            address_bytes = bytearray(4)
            while True:
                bytes_read = file.readinto(address_bytes)
                if bytes_read == 0:
                    break

                address = (address_bytes[0] << 24) | (address_bytes[1] << 16) | (address_bytes[2] << 8) | address_bytes[3]
                tag = address >> (n_bits_offset + n_bits_indice)
                indice = (address >> n_bits_offset) & ((2 ** n_bits_indice) - 1)

                print(f"address: {address}, tag: {tag}, indice: {indice}")
                print(f"cache_tag[indice]: {cache_tag[indice]}, cache_val[indice]: {cache_val[indice]}")

                if assoc == 1:
                    if cache_val[indice] == 0:
                        misses_compulsorios += 1
                        cache_val[indice] = 1
                        cache_tag[indice] = tag
                    else:
                        if cache_tag[indice] == tag:
                            hits += 1
                        else:
                            misses_conflito += 1
                            cache_tag[indice] = tag
               # else:
               #    if cache_val[indice] == 0:

               #    else:
                       #
                   # found = False
                   # for part in cache_:
                   #     for i in range(assoc):
                   #         if part.tag[i] == tag:
                   #             if part.val[i] == 1:
                   #                 found = True
                   #                 hits += 1
                   #                 break

                   # if not found:
                   #     empty_found = False
                   #     for p in cache_:
                   #         for i in range(assoc):
                   #             if p.val[i] == 0:
                   #                 p.val[i] = 1
                   #                 p.tag[i] = tag
                   #                 empty_found = True
                   #                 misses_compulsorios += 1
                   #                 break
                   #         if empty_found:
                   #             break

                   #     if not empty_found:
                   #         part = random.choice(cache_)
                   #         idx = random.randint(0, assoc - 1)
                   #         part.val[idx] = 1
                   #         part.tag[idx] = tag
                   #         misses_conflito += 1

                acessos += 1

        if flag_saida == 1:
            print(
                str(acessos) + " " +
                str(hits/acessos) + " " +
                str((misses_capacidade + misses_conflito + misses_compulsorios)/acessos) + " " +
                str(misses_compulsorios/(misses_capacidade + misses_conflito + misses_compulsorios)) + " " +
                str(misses_capacidade/(misses_capacidade + misses_conflito + misses_compulsorios)) + " " +
                str(misses_conflito/(misses_capacidade + misses_conflito + misses_compulsorios))
            )
        else:
            print(" idk ")

    except FileNotFoundError:
        print("Não foi possível ler o arquivo de entrada.")
        sys.exit(1)


if __name__ == "__main__":
    main()
