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
                else:
                    # Não é necessário a parte de mapeamento direto
                    # acima mas como eu já tinha feito vou deixar assim
                    # essa segunda parte engloba o mapeamento direto.
                    hit = False
                    for i in range(assoc):
                        idx = indice + i * nsets
                        if cache_val[idx] == 1:
                            if cache_tag[idx] == tag:
                                hits += 1
                                hit = True
                                break

                    if not hit:
                        if subs == Algoritmo.R:

                            idx = random.randint(0, assoc - 1)

                            count = 0
                            for i in range(assoc):
                                count += cache_val[indice + i*nsets]

                            if cache_val[indice + idx * nsets] == 0:
                                misses_compulsorios += 1
                            elif count == assoc:
                                misses_capacidade += 1
                            else:
                                misses_conflito += 1

                            cache_val[indice + idx * nsets] = 1
                            cache_tag[indice + idx * nsets] = tag

                        ## fazer os outros algoritmos
                        ## elif subs == Algoritmo.LRU ... 
                        ## else ... Algoritmo.FIFO

                acessos += 1

        if flag_saida == 1:
            print(
                str(acessos) + " " +
                format(hits/acessos, '.4f') + " " +
                format((misses_capacidade + misses_conflito + misses_compulsorios)/acessos, '.4f') + " " +
                format(misses_compulsorios/(misses_capacidade + misses_conflito + misses_compulsorios), '.4f') + " " +
                format(misses_capacidade/(misses_capacidade + misses_conflito + misses_compulsorios), '.4f') + " " +
                format(misses_conflito/(misses_capacidade + misses_conflito + misses_compulsorios), '.4f') + " "
                )
        else:
            print("""
# ===================================================================================
#                             Simulador de Cache
# ===================================================================================
#                        __====-_  _-====
#                  _--^^^#####//      \\\\#####^^^--_
#               _-^##########// (    ) \\\\##########^-_
#              -############//  |\\^^/|  \\\\############-
#            _/############//   (@::@)   \\\\############\\_
#           /#############((     \\\\//     ))#############\\
#          -###############\\\\    (oo)    //###############-
#         -#################\\\\  / `' \\  //#################-
#        -###################\\\\/  (|)  \\\\//###################-
#       _#/|##########/\\######(   / | \\   )######/\\##########|\\#_
#       |/ |#/\\#/\\#/\\/  \\#/\\#/\\ (  | |  ) /\\#/\\#/\\  \\/\\/\\#/\\| \\|
#       |/  |/  \\|/  |/     |/  |/  |/   |/     |/  |/  |/  |/  \\|/
#
# Authors: Igor Basilio & Lucas Bayer
# ===================================================================================
            """)
            print(
                "Acessos : " + str(acessos) + "\n" +
                "Taxa de hit : " + format(hits/acessos, '.4f') + "\n" +
                "Taxa de misses : " + format((misses_capacidade + misses_conflito + misses_compulsorios)/acessos, '.4f') + "\n" +
                "Taxa de misses compulsorios : " + format(misses_compulsorios/(misses_capacidade + misses_conflito + misses_compulsorios), '.4f') + "\n" +
                "Taxa de misses de capacidade : " + format(misses_capacidade/(misses_capacidade + misses_conflito + misses_compulsorios), '.4f') + "\n" +
                "Taxa de misses de conflito : " + format(misses_conflito/(misses_capacidade + misses_conflito + misses_compulsorios), '.4f') + "\n"
                )
    except FileNotFoundError:
        print("Não foi possível ler o arquivo de entrada.")
        sys.exit(1)


if __name__ == "__main__":
    main()
