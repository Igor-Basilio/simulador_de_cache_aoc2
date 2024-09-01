
// ===================================================================================
//                             Simulador de Cache                                     
// ===================================================================================
//                        __====-_  _-====__                  
//                  _--^^^#####//      \\#####^^^--_          
//               _-^##########// (    ) \\##########^-_       
//              -############//  |\^^/|  \\############-      
//            _/############//   (@::@)   \\############\_    
//           /#############((     \\//     ))#############\   
//          -###############\\    (oo)    //###############-  
//         -#################\\  / `' \  //#################- 
//        -###################\\/  (|)  \//###################-
//       _#/|##########/\######(   / | \   )######/\##########|\#_
//       |/ |#/\#/\#/\/  \#/\#/\ (  | |  ) /\#/\#/\  \/\/\#/\| \|
//       |/  |/  \|/  |/     |/  |/  |/   |/     |/  |/  |/  |/  \|/
//
// Authors: Igor Basilio & Lucas Bayer                                            
// ===================================================================================

package main

import "core:os"
import "core:fmt"
import "core:strconv"

nsets      : i64
bsize      : i64
assoc      : i64
subs       : algoritmo
flag_saida : bool 

algoritmo :: enum { 
    R,
    LRU,
    FIFO,
}

hits                : i64
acessos             : i64
misses              : i64
misses_compulsorios : i64

main :: proc() 
{
    args := os.args[1:];
    if len(args) != 6 {
        fmt.println("Uso :\nsimulador_cache <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada");
        os.exit(1);
    }

    ok : bool
    nsets, ok = strconv.parse_i64(args[0]);
    if !ok { 
        fmt.println("Número de conjuntos inválido.");
        os.exit(1);
    }
    bsize, ok = strconv.parse_i64(args[1]);
    if !ok { 
        fmt.println("Tamanho do bloco inválido.");
        os.exit(1);
    }
    assoc, ok = strconv.parse_i64(args[2]);
    if !ok { 
        fmt.println("Associatividade inválida.");
        os.exit(1);
    }
    
    switch args[3] {
        case "R": subs = algoritmo.R;
        case "LRU": subs = algoritmo.LRU;
        case "FIFO": subs = algoritmo.FIFO;
        case : {
            fmt.println("Algortimo de substituição inválido.")
            os.exit(1)
        }
    }
    
    temp : i64
    temp, ok = strconv.parse_i64(args[4]);
    if !ok { 
        fmt.println("Flag de saída deve ser 0 ou 1.");
        os.exit(1);
    }

    if temp == 0 {
        flag_saida = false
    }else if temp == 1 {
        flag_saida = true
    }else {
        fmt.println("Flag de saída deve ser 0 ou 1.")
        os.exit(1)
    }

    file, err := os.open(args[5]);
    if err != os.ERROR_NONE {
        fmt.println("Não foi possível ler o arquivo de entrada.");
        os.exit(1);
    }
    defer os.close(file);

    address : [4] u8
    for { 
        bytes_read, read_err := os.read(file, address[:]);
        if read_err != os.ERROR_NONE {
           fmt.println("Erro ao ler arquivo.");
           os.exit(1);
        }

        // Lógica da cache
        fmt.println(address);

        if bytes_read == 0 { break; }
        acessos+=1;
    }
    
    fmt.println(acessos);

}

