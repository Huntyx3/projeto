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

    def getRelevantAbilities(self):
        self.abilities = [abilityList[abilityNames.index(a)] for a in self.abilities if a in abilityNames]

class Type:
    def __init__(self, id: int, name: str, superEffective: list, notVeryEffective: list, ineffective: list):
        self.id = id
        self.name = name
        self.superEffective = superEffective
        self.notVeryEffective = notVeryEffective
        self.ineffective = ineffective

    def calcEffectiveness(self, targetTypes: list[Type], attackerAbility = None, targetAbility = None) -> float:
        multiplier = 1
        ineffective = self.ineffective
        superEffective = self.superEffective
        notVeryEffective = self.notVeryEffective
        for type in targetTypes:
            if attackerAbility:
                for t in attackerAbility.offensive.get("typeEffs", None):
                    if t[0] == type.name:
                        if t[1] == 0:
                            ineffective = t[2]
                        elif t[1] == 2:
                            superEffective = t[2]
                        elif t[1] == 0.5:
                            notVeryEffective = t[2]
                if targetAbility:
                    if not attackerAbility.ignores or not targetAbility.ignorable:
                        for t in self.defensive.get("TypeEffs", None):
                            if t[0] == type.name:
                                if t[1] == 0:
                                    ineffective = t[2]
                                elif t[1] == 2:
                                    superEffective = t[2]
                                elif t[1] == 0.5:
                                    notVeryEffective = t[2]
            if type in ineffective:
                multiplier *= 0
            if type in superEffective:
                multiplier *= 2
            if type in notVeryEffective:
                multiplier *= 0.5
        return multiplier

class Ability: # partial implementation, in progress
    def __init__(self, id: int, name: str, defensive: dict, offensive: dict, weather: int, terrain: int, ignores: bool, ignorable: bool):
        self.id = id
        self.name = name
        self.defensive = defensive
        self.offensive = offensive
        self.weather = weather
        self.terrain = terrain
        self.ignores = ignores
        self.ignorable = ignorable

    def abilitiesMod(self, attackType: Type, effectiveness: float, attackerAbility: Ability):
        multiplier = effectiveness
        if attackerAbility.ignore and self.ignorable == True:
            return multiplier
        for mult in self.defensive["typeMults"]:
            if attackType.name == mult[0]:
                multiplier *= mult[1]
        for x in self.defensive["effMults"]:
            for mult in x:
                if mult[0] == effectiveness:
                    multiplier *= mult[1]

class Weather: # Not implemented
    def __init__(self, id: int, name: str, typeMults: list, priority: int):
        self.id = id
        self.name = name
        self.typeMults = typeMults
        self.priority = priority

class Terrain: # Not implemented
    def __init__(self, id: int, name: str, typeMults: list):
        self.id = id
        self.name = name
        self.typeMults = typeMults

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

def isFloat(toCheck) -> bool:
    try:
        float(toCheck)
        return True
    except ValueError:
        return False

def printTypeEffectivenessFrequency(movesetTypes: list[int], attackerAbility = None) -> tuple[int]:
    effCounts = {}
    for pokemon in pokemonList:
        eff = [type.calcEffectiveness(pokemon.types, attackerAbility, pokemon.abilities) for type in movesetTypes]
        maxEff = max(eff)
        effCounts[maxEff] = effCounts.get(maxEff, 0) + 1
    effCounts = dict(sorted(effCounts.items()))
    print("Fator\tFrequência Relativa")
    for mult, count in effCounts.items():
        print(f"{mult}\t{count} / {formCount} = {count / formCount * 100:.1f}%")

def printTypeEffectivenessTable(movesetTypes: list[int], filter: list[float], attackerAbility = None):
    print("Target\t\t\t| Target Types\t\t\t| Ability\t\t| Mult\t| Attack Types")
    with open("resultado.csv", "w", encoding="UTF-8") as f:
        f.write("sep=;\nTarget;Target Types;Ability;Mult;Attack Types\n")
        for pokemon in pokemonList:
            eff = [type.calcEffectiveness(pokemon.types, attackerAbility, pokemon.abilities) for type in movesetTypes]
            maxEff = max(eff)
            maxEffTypeNames = [movesetTypes[x].name for x in range(len(eff)) if eff[x] == maxEff]
            if maxEff in filter or not filter:
                print(f"{pokemon.fullName}" + "\t" * (3 - len(f"{pokemon.fullName}") // 8), end="")
                print(f"| {pokemon.types}" +  "\t" * (4 - len(f"| {pokemon.types}") // 8), end="")
                print("| Any" + "\t" * (3 - len("| Any") // 8), end="")
                print(f"| {maxEff:.2f}"+"\t" * (1 - len(f"| {maxEff:.2f}") // 8), end="")
                print(f"| {maxEffTypeNames}")
            f.write(f"{pokemon.fullName};{pokemon.types};Any;{maxEff:.2f};{maxEffTypeNames}\n")

def buildPokemon():
    for pokemon in pokemonRaw:
        id = pokemon.get("id", None)
        name = pokemon.get("name", "")
        if id is None:
            raise ValueError(f"Erro em pokemon_data.json: Pokémon sem ID. Nome: {name}")
        if not name:
            raise ValueError(f"Erro em pokemon_data.json: Pokémon sem Nome. ID: {id}")
        for form in pokemon["forms"]:
            formName = form.get("formName", "")
            formId = float("." + str(form.get("formId", None)))
            if id + formId in pokemonIds:
                raise ValueError(f"Erro em pokemon_data.json: Pokémon com várias formas com o mesmo ID. Pokémon: {name} {id}")
            fullName = name + formName
            if fullName in pokemonNames:
                raise ValueError(f"Erro em pokemon_data.json: Múltiplas formas do mesmo Pokémon com o mesmo nome. Pokémon: ({fullName} {id})")
            types = form.get("types", pokemon["forms"][0].get("types", []))
            for type in types:
                if type in typeNames:
                    type = typeList[typeNames.index(type)]
                else:
                    raise ValueError(f"Erro em JSON: Existe tipo ({type}) em pokemon_data.json que não existem em type_data.json")
            abilities = form.get("abilities", pokemon["forms"][0].get("abilities", []))
            bases = []
            bases.append(form["bases"].get("HP", pokemon["forms"][0]["bases"].get("HP", 1)))
            bases.append(form["bases"].get("Atk", pokemon["forms"][0]["bases"].get("Atk", 1)))
            bases.append(form["bases"].get("Def", pokemon["forms"][0]["bases"].get("Def", 1)))
            bases.append(form["bases"].get("SpA", pokemon["forms"][0]["bases"].get("SpA", 1)))
            bases.append(form["bases"].get("SpD", pokemon["forms"][0]["bases"].get("SpD", 1)))
            bases.append(form["bases"].get("Spe", pokemon["forms"][0]["bases"].get("Spe", 1)))
            weight = form.get("weight", pokemon["forms"][0].get("weight", 0.1))
            pokemonList.append(Pokemon(id, name, formId, formName, types, abilities, bases, weight))
            pokemonList[-1].getRelevantAbilities()
            pokemonIds.append(id + formId)
            pokemonNames.append(pokemonList[-1].fullName)
        

def buildTypes():
    for type in typeRaw:
        name = type.get("typeName", "")
        id = type.get("typeId", None)
        if id is None:
            raise ValueError(f"Erro em type_data.json: Existe Tipo sem ID. Nome: {name}")
        if not name:
            raise ValueError(f"Erro em type_data.json: Existe Tipo sem nome. ID: {id}")
        if id in typeIds:
            raise ValueError(f"Erro em type_data.json: Existe Tipo com ID repetido. Nome: {name} ID: {id}")
        if name in typeNames:
            raise ValueError(f"Erro em type_data.json: Existe Tipo com nome repetido. Nome: {name} ID: {id}")
        effs = type.get("damage dealt", {})
        veryEffective = effs.get("2", [])
        notVeryEffective = effs.get("0.5", [])
        ineffective = effs.get("0", [])
        typeList.append(Type(id, name, list(set(veryEffective)), list(set(notVeryEffective)), list(set(ineffective))))
        typeNames.append(name)
        typeIds.append(id)

def buildAbilities():
    for ability in abilityRaw:
        id = ability.get("id", None)
        name = ability.get("name", "")
        if id is None:
            raise ValueError(f"Erro em ability_data.json: Existe Ability sem ID. Nome: {name} ")
        if not name:
            raise ValueError(f"Erro em ability_data.json: Existe Ability sem nome. ID: {id}")
        if id in abilityIds:
            raise ValueError(f"Erro em ability_data.json: Existe Ability com ID repetido. Nome: {name} ID: {id}")
        if name in abilityNames:
            raise ValueError(f"Erro em ability_data.json: Existe Ability com nome repetido. Nome: {name} ID: {id}")
        offensive = ability.get("offensive", {})
        defensive = ability.get("defensive", {})
        weather = ability.get("weather", None)
        terrain = ability.get("terrain", None)
        ignores = ability.get("ignores", False)
        ignorable = ability.get("ignorable", True)
        abilityList.append(Ability(id, name, defensive, offensive, weather, terrain, ignores, ignorable))
        abilityNames.append(name)
        abilityIds.append(id)


MENU = """==== Pokémon Coverage Calculator ===
1. Check type Effectiveness | 0. Sair"""
yesTuple = ("y", "s", "yes", "sim", "1")
noTuple = ("n", "no", "nao", "não", "0")
quitTuple = ("q", "quit", "exit", "close", "sair")
filterEff = []
exit = False
cont = False

while True:
    pokemonRaw = {}
    pokemonList = []
    pokemonNames = []
    pokemonIds = []
    typeRaw = {}
    typeNames = []
    typeIds = []
    typeList = []
    abilityRaw = {}
    abilityNames = []
    abilityIds = []
    abilityList = []
    try:
        with open("pokemon_data.json") as f:
            pokemonRaw = json.load(f)
        with open("type_data.json") as f:
            typeRaw = json.load(f)
        with open("ability_data.json") as f:
            abilityRaw = json.load(f)
        buildTypes()
        buildAbilities()
        buildPokemon()
    except ValueError as erro:
        print(erro)
        input("Altere o ficheiro JSON e tente novamente. Enter para continuar.")
        continue
    break

formCount = len(pokemonList)

while True:
    print(MENU)
    option = getInput("Opção: ")
    match option:
        case "0":
            break
        case "1":
            while True:
                print(", ".join(f"{t.id}: {t.name}" for t in typeList))
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
                            attackTypes[i] = typeList[typeIds.index(attackTypes[i])]
                    elif attackTypes[i] in typeNames:
                        attackTypes[i] = typeList[typeNames.index(attackTypes[i])]
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
            print("Criado \"resultado.csv\" com o resultado. Se pretender guardar, faça uma cópia; o ficheiro é substituído a cada execução.")
            if confirm("Imprimir tabela?"):
                filter = getInput("Introduza fatores a imprimir (separar por \" \" para selecionar vários, \"a\" para imprimir todos): ").replace(",", " ")
                filter = filter.split(" ")
                for i in range(0, len(filter)):
                    if isFloat(filter[i]):
                        filterEff.append(float(filter[i]))
                printTypeEffectivenessTable(attackTypes, filter=filterEff)
                filterEff = []
        case _:
            print("Erro: Opção inválida")

