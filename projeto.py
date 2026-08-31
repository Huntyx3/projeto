import json

class Pokemon:
    def __init__(self, id: int, name: str, formId: float, formName: str, types: list, abilities: list, bases: list, weight: float):
        self.id = id
        self.name = name
        self.formId = formId
        self.formName = formName
        self.types = types
        self.abilities = abilities
        self.bases = bases
        self.weight = weight
        self.fullName = self.name + self.formName
        self.fullId = self.id + self.formId

class Type:
    def __init__(self, id: int, name: str, superEffective: list, notVeryEffective: list, ineffective: list):
        self.id = id
        self.name = name
        self.superEffective = superEffective
        self.notVeryEffective = notVeryEffective
        self.ineffective = ineffective

    def calcEffectiveness(self, targetTypes: list[Type], attackerAbility = None, targetAbility = None) -> float:
        multiplier = 1
        for type in targetTypes:
            if type in self.ineffective:
                multiplier *= 0
            if type in self.superEffective:
                multiplier *= 2
            if type in self.notVeryEffective:
                multiplier *= 0.5
        return multiplier

class Ability:
    def __init__(self, id: int, name: str, defensive: dict, offensive: dict, weather: int, terrain: bool, ignorable: bool):
        self.id = id
        self.name = name
        self.defensive = defensive
        self.offensive = offensive
        self.weather = weather
        self.terrain = terrain
        self.ignorable = ignorable

def getInput(inputInstruction: str) -> str:
    while True:
        x = input(inputInstruction).strip().lower()
        if x:
            return x

def confirm(inputInstruction: str) -> bool:
    while (True):
        confirm = input(f"{inputInstruction} (y/n): ").strip().lower()
        if confirm in yesTuple:
            return True
        if confirm in noTuple:
            return False

def isInt(toCheck) -> bool:
    try:
        int(toCheck)
        return True
    except ValueError:
        return False

def printTypeEffectivenessFrequency(movesetTypes: list[int], attackerAbility = None) -> tuple[int]:
    effCounts = {}
    for pokemon in pokemonDict.values():
        eff = [type.calcEffectiveness(pokemon.types, attackerAbility, pokemon.abilities) for type in movesetTypes]
        maxEff = max(eff)
        effCounts[maxEff] = effCounts.get(maxEff, 0) + 1
    effCounts = dict(sorted(effCounts.items()))
    print("Fator\tFrequência Relativa")
    for mult, count in effCounts.items():
        print(f"{mult}\t{count} / {formCount} = {count / formCount * 100:.1f}%")

def printTypeEffectivenessTable(movesetTypes: list[int], attackerAbility = None, filter = [0, 0.25, 0.5, 1, 2, 4]):
    print("Target\t\t\t| Target Types\t\t\t| Ability\t\t| Mult\t| Attack Type")
    for pokemon in pokemonDict.values():
        eff = [type.calcEffectiveness(pokemon.types, attackerAbility, pokemon.abilities) for type in movesetTypes]
        maxEff = max(eff)
        maxEffTypeNames = [movesetTypes[x].name for x in range(len(eff)) if eff[x] == maxEff]
        if maxEff in filter:
            print(f"{pokemon.fullName}" + "\t" * (3 - len(f"{pokemon.fullName}") // 8), end="")
            print(f"| {pokemon.types}" +  "\t" * (4 - len(f"| {pokemon.types}") // 8), end="")
            print("| Any" + "\t" * (3 - len("| Any") // 8), end="")
            print(f"| {maxEff:.2f}"+"\t" * (1 - len(f"| {maxEff:.2f}") // 8), end="")
            print(f"| {maxEffTypeNames}")

def buildPokemon():
    for pokemon in pokemonRaw:
        id = pokemon.get("id", None)
        if id is None:
            raise ValueError("Erro em pokemon_data.json: Pokémon sem ID.")
        name = pokemon.get("name", None)
        if name is None:
            raise ValueError("Erro em pokemon_data.json: Pokémon sem Nome.")
        for form in pokemon["forms"]:
            formName = form.get("formName", "")
            formId = float("0." + str(form.get("formId", None)))
            if formId is None:
                raise ValueError("Erro em pokemon_data.json: Pokémon Form sem ID.")
            types = form.get("types", pokemon["forms"][0].get("types", []))
            for type in types:
                if type in typeNames:
                    type = typeDict[typeIds[typeNames.index(type)]]
                else:
                    raise ValueError("Erro em JSON: Existem tipos em pokemon_data.json que não existem em type_data.json")
            abilities = form.get("abilities", pokemon["forms"][0].get("abilities", []))
            bases = []
            bases.append(form["bases"].get("HP", pokemon["forms"][0]["bases"].get("HP", 1)))
            bases.append(form["bases"].get("Atk", pokemon["forms"][0]["bases"].get("Atk", 1)))
            bases.append(form["bases"].get("Def", pokemon["forms"][0]["bases"].get("Def", 1)))
            bases.append(form["bases"].get("SpA", pokemon["forms"][0]["bases"].get("SpA", 1)))
            bases.append(form["bases"].get("SpD", pokemon["forms"][0]["bases"].get("SpD", 1)))
            bases.append(form["bases"].get("Spe", pokemon["forms"][0]["bases"].get("Spe", 1)))
            weight = form.get("weight", pokemon["forms"][0].get("weight", 0.1))
            pokemonDict[id + formId] = Pokemon(id, name, formId, formName, types, abilities, bases, weight)
            pokemonIds.append(id + formId)
            pokemonNames.append(pokemonDict[id + formId].fullName)
    if len(pokemonNames) != len(set(pokemonNames)):
        raise ValueError("Erro em pokemon_data.json: Múltiplas formas do mesmo Pokémon com o mesmo nome.")

def buildTypes():
    for type in typeRaw:
        if type.get("typeName", None) is None:
            raise ValueError("Erro em type_data.json: Existem Tipos sem nome")
        if type.get("typeId", None) is None:
            raise ValueError("Erro em type_data.json: Existem Tipos sem ID")
        typeDict[type["typeId"]] = Type(type["typeId"], type["typeName"], set(type["damage dealt"]["2"]), set(type["damage dealt"]["0.5"]), set(type["damage dealt"]["0"]))
        typeNames.append(type["typeName"])
        typeIds.append(type["typeId"])
    if len(set(typeNames)) != len(typeNames):
        raise ValueError("Erro em type_data.json: Tipos com o mesmo nome")
    if len(set(typeIds)) != len(typeIds):
        raise ValueError("Erro em type_data.json: Tipos com o mesmo ID.")

def buildAbilities():
    for ability in abilityRaw:
        id = ability.get("id", None)
        if id is None:
            raise ValueError("Erro em ability_data.json: Existem Abilities sem ID")
        name = ability.get("name", None)
        if id is None:
            raise ValueError("Erro em ability_data.json: Existem Abilities sem nome")
        offensive = ability.get("offensive", None)
        defensive = ability.get("defensive", None)
        weather = ability.get("weather", 0)
        terrain = ability.get("terrain", False)
        ignorable = ability.get("ignorable", True)
        abilityDict[id] = Ability(id, name, defensive, offensive, weather, terrain, ignorable)
        abilityNames.append(name)
        abilityIds.append(id)
    if len(set(abilityNames)) != len(abilityNames):
        raise ValueError("Erro em ability_data.json: Abilities com o mesmo nome")
    if len(set(abilityIds)) != len(abilityIds):
        raise ValueError("Erro em ability_data.json: Abilities com o mesmo ID.")


MENU = """==== Pokémon Coverage Calculator ===
1. Check type Effectiveness | 2. Check final power | 0. Sair"""
yesTuple = ("y", "s", "yes", "sim", "1")
noTuple = ("n", "no", "nao", "não", "0")
quitTuple = ("q", "quit", "exit", "close", "sair")
pokemonRaw = {}
pokemonDict = {}
pokemonNames = []
pokemonIds = []
typeRaw = {}
typeNames = []
typeIds = []
typeDict = {}
abilityRaw = {}
abilityNames = []
abilityIds = []
abilityDict = {}
filterEff = []
exit = False
cont = False

with open("pokemon_data.json") as f:
    pokemonRaw = json.load(f)

with open("type_data.json") as f:
    typeRaw = json.load(f)

with open("ability_data.json") as f:
    abilityRaw = json.load(f)

buildTypes()
buildPokemon()
formCount = len(pokemonDict)

while True:
    print(MENU)
    option = getInput("Opção: ")
    match option:
        case "0":
            break
        case "1":
            while True:
                print(", ".join(f"{key}: {value.name}" for key, value in typeDict.items()))
                attackTypes = getInput("Introduza os tipos dos moves do atacante (separados por \" \". \"q\" para sair): ").replace(",", " ")
                if attackTypes in quitTuple:
                    cont = True
                    break
                attackTypes = attackTypes.title().split(" ")
                exit = True
                for i in range(0, len(attackTypes)):
                    if isInt(attackTypes[i]):
                        attackTypes[i] = int(attackTypes[i])
                        if attackTypes[i] in typeIds:
                            attackTypes[i] = typeDict[attackTypes[i]]
                    elif attackTypes[i] in typeNames:
                        attackTypes[i] = typeDict[typeIds[typeNames.index(attackTypes[i])]]
                    if not isinstance(attackTypes[i], Type):
                        print(f"{attackTypes[i]} não é um tipo válido. Tente novamente.")
                        exit = False
                        break
                if exit:
                    exit = False
                    break
            if cont: 
                cont = False
                continue
            printTypeEffectivenessFrequency(attackTypes)
            if confirm("Imprimir tabela?"):
                print("1 - Neutrally effective (1x) | 2. Super Effective (2x) | 3. Not very effective (0.5x)", end="")
                print(" | 4. Extremely effective (4x) | 5. Mostly ineffective (0.25x)")
                print("6. Completely ineffective (0x) | 7. Imprimir todos")
                filter = getInput("Opção (separar por \" \" para selecionar vários): ").replace(",", " ")
                filter = filter.split(" ")
                for i in range(0, len(filter)):
                    if filter[i] in ("6", "0x", "0"):
                        filterEff.append(0)
                    elif filter[i] in ("5", "0.25x", "0.25"):
                        filterEff.append(0.25)
                    elif filter[i] in ("3", "0.5x", "0.5"):
                        filterEff.append(0.5)
                    elif filter[i] in ("1", "1x"):
                        filterEff.append(1)
                    elif filter[i] in ("2", "2x"):
                        filterEff.append(2)
                    elif filter[i] in ("4", "4x"):
                        filterEff.append(4)
                    else:
                        filterEff = [0, 0.25, 0.5, 1, 2, 4]
                printTypeEffectivenessTable(attackTypes, filter=filterEff)
                filterEff = []




        case _:
            print("Erro: Opção inválida")

