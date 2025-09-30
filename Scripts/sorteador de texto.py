import random

def sorteadorTexto(num_caracteres):
    texto_gerado = ""
    vetor_caracteres = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','1', '2', '3', '4', '5', '6', '7', '8', '9','0']
    for a in range(num_caracteres):
        pos_aleatoria = random.randint(0,len(vetor_caracteres) - 1)
        texto_gerado += vetor_caracteres[pos_aleatoria]
    return texto_gerado


  
print(sorteadorTexto(150))
