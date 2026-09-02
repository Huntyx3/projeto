# Pokémon Type Coverage Calculator

Este é um script de python que executa no terminal e que, dado os ataques no moveset de um atacante, calcula o máximo multiplicador aplicável a cada Pokémon. Baseado em ficheiros JSON para permitir modificação dos dados.

## Indentificação do problema e público-alvo

Existem vários sites na web com esta funcionalidade básica, mas nenhum permite ter em conta as possíveis abilidades do alvo. Uma das extensões previstas é isso mesmo.

Também não existe nenhum que permita alterar as resistências/fraquezas de cada tipo ou adicionar novos tipos. Como este script funciona a partir de ficheiros JSON, é possível adicionar ou alterar tipos no JSON, e esses dados serão posteriormente utilizados pelo script.

O público-alvo será qualquer utilizador dos sites já existentes, particularmente os que apreciem a possibilidade de alterar os dados em que se baseia o script.

## Instruções de uso

A aplicação usa os dados nos ficheiros type_data.json, pokemon_data.json e ability_data.json para o seu funcionamento.

Os dados nos ficheiros JSON podem ser alterados pelo utilizador para funcionar em jogos de gerações diferentes, ou fangames que adicionem ou alterem os dados de Pokémon/tipos/abilidades.

A cada execução, o resultado é guardado em resultado.csv. Este ficheiro é substituído a cada execução. O utilizador deve fazer uma cópia do ficheiro se o pretender guardar.

## MVP e extensões

O MVP será a possibilidade de obter uma lista de multiplicadores contra todos os Pokémon existentes, tendo em conta apenas uma lista dos tipos de ataque no moveset do atacante e os tipos do alvo. Estes multiplicadores serão apresentados no formato de tabela dentro do terminal e num ficheiro .csv.

Extensões irão permitir ter em conta também outros fatores, como abilidades, terreno, tempo meteorológico, STAB, características específicas do ataques.

## Estrutura dos dados utilizados

Ficheiros JSON são lidos e convertidos em dicionários Python, que são posteriormente convertidos em instâncias da respetiva classe. (e.g. cada objeto em type_data.json é convertido numa instância da classe "Type").

Os resultados são apresentados como forma de tabela. O resultado pode ser visualizado no terminal, ou através do ficheiro .csv gerado.
