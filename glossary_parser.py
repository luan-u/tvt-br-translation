import sys
from datetime import datetime

TROPES_FILE = 'BrAdministrivia.CorrespondenciaEntreTroposENBR.txt'

def count_uppercase(text: str):
    'Conta quantas maiúsculas há em uma linha de texto.'
    return sum(1 for c in text if c.isupper())

def count_lowercase(text: str):
    'Conta quantas minúsculas há em uma linha de texto.'
    return sum(1 for c in text if c.islower())

def partition_tropes(trope_pairs: list) -> dict:
    'Com base em uma lista de tropos, devolve um dicionário de 26 posições, cada uma delas sendo uma letra.'
    trope_dict = {}
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        # need to initialize so i can append later
        trope_dict[letter] = []

    for pair in trope_pairs:
        first_letter = pair[0][0]
        trope_dict[first_letter].append(pair)

    return trope_dict

def generate_tropes_file(trope_groups: dict):
    'Gera uma página com a correspondência de itens e na sintaxe wiki do TV Tropes.'

    outtext = '''%%This page has a list of English-Portuguese trope matches.
Nesta página listaremos as correspondências propostas ou já utilizadas \
entre tropos originais (em inglês) e tropos em português (já traduzidos ou não).

Um problema que emerge da quantidade crescente de tropos é fazer a correspondência entre os \
títulos originais e os traduzidos. No processo de tradução eu utilizo o [=OmegaT=], uma ferramenta \
de tradução assistida por computador que possui uma função de glossário. \
Assim sendo, eu elaborei um \'\'script\'\' em Python que lê o arquivo do glossário -- você pode \
[[https://github.com/luan-u/tvt-br-translation/blob/main/glossary/glossary.txt consultar o arquivo aqui]], \
caso queira -- e gera uma página índice compatível com a formatação do TV Tropes.

Caso você queira sugerir um nome traduzido ou discutir uma tradução proposta, peço que se dirija à \
[[https://tvtropes.org/pmwiki/posts.php?discussion=13084395760A01420100 discussão do projeto de tradução br]] -- \
isso facilita o controle e manutenção do glossário.

Caso você queira traduzir um dos tropos, fique à vontade -- basta clicar e editar.

O índice é ordenado conforme a letra inicial do nome em inglês. Para achar rapidamente um tropo, \
utilize Ctrl-F (ou Command-F em um Mac).

Note que alguns tropos possuem mais de uma tradução possível e, por isso, aparecerão repetidos, \
mesmo que as traduções alternativas sejam apenas um redirecionamento.
'''

    outtext += '\n----\n\n'
    today = datetime.today().strftime("%d-%m-%Y")
    outtext += f'A listagem abaixo foi gerada em {today} (DD-MM-YYYY).\n\n'

    outtext += '[[foldercontrol]]\n\n'

    for letter in trope_groups:
        outtext += f'[[folder:\'\'\'{letter}\'\'\']]\n'
        trope_list = trope_groups[letter]
        print(f'Quantidade na letra {letter}: {len(trope_list)}.')
        for trope_pair in trope_list:
            trope_en, trope_br = trope_pair
            if count_uppercase(trope_en) == 1 or count_lowercase(trope_en) == 0:
                # for cases such as Anaphora or BFG
                trope_en = f'{{{{{trope_en}}}}}'
            outtext += f'* {trope_en} -- {trope_br}\n'
        outtext += '[[/folder]]\n\n'

    outtext += '----'

    with open(TROPES_FILE, 'w', encoding='utf-8') as outfile:
        outfile.write(outtext)

    print('Arquivo gerado com êxito.')


if __name__ == '__main__':
    print("Olá!")
    glossary_file = 'glossary.txt'
    if len(sys.argv) > 1:
        glossary_file = sys.argv[1]
    print(f'Usando arquivo {glossary_file} para gerar página.')

    tropes_list = []

    # reserved for the future
    administrivia_list = []
    film_list = []
    literature_list = []

    try:
        with open(glossary_file, 'r', encoding='utf-8') as glossary:
            for line in glossary:
                if line[0] == '#': line = glossary.readline()

                split_line = line.strip().split('\t')

                if len(split_line) > 1 and 'Br/' in split_line[1]:
                    # right now we will disconsider subspaces other than Br/
                    tropes_list.append([split_line[0], split_line[1]])
    except FileNotFoundError:
        print('Arquivo não encontrado.')
        if len(sys.argv) == 1:
            print('Verifique se o arquivo de glossário está na mesma pasta de execução.')
        else:
            print('Verifique se o caminho para o arquivo está correto.')
        sys.exit(1)

    tropes_list.sort()
    grouped_tropes = partition_tropes(tropes_list)
    generate_tropes_file(grouped_tropes)
