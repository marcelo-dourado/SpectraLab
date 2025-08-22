def deletar_chaves(dicionario, chave):
    dicionario.pop(chave, None)

if __name__ == "__main__":
    dicionario = {'a': 1}
    print(dicionario)
    deletar_chaves(dicionario, 'a')
    print(dicionario)