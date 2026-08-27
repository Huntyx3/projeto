import json

class Pokemon:
    def __init__ (self, id: int, name: str, formId: float, formName: str, types: list, abilities: list, bases: list, weight: float):
        self.id = id
        self.name = name
        self.formId = formId
        self.formName = formName
        self.types = types
        self.abilities = abilities
        self.bases = bases
        self.weight = weight
        self.fullName = self.name + self.formName

class Type:
    def __init__ (self, id: int, name: str, superEffective: list, notVeryEffective: list, ineffective: list):
        self.id = id
        self.name = name
        self.superEffective = superEffective
        self.notVeryEffective = notVeryEffective
        self.ineffective = ineffective

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

def calcTypeEffectiveness(movesetTypes: list[int], targetTypes: list[int], attackerAbility = None, defenderAbilities = None) -> dict:
    multipliers = {}
    for attackType in movesetTypes:
        multiplier = 1.0
        for effectiveness, types in typeRaw[attackType]["damage dealt"].items():
            for type in types:
                if type in targetTypes:
                    multiplier *= float(effectiveness)
        multipliers[attackType] = multiplier
    return multipliers

def printTypeEffectivenessFrequency(movesetTypes: list[int], attackerAbility = None):
    ineffective = mostlyIneffective = notVeryEffective = neutral = superEffective = extremelyEffective = 0
    for pokemon in pokemonDict.values():
        eff = calcTypeEffectiveness(movesetTypes, pokemon.types, attackerAbility)
        maxEff = max(eff.values())
        if maxEff == 0:
            ineffective += 1
        elif maxEff <= 0.25:
            mostlyIneffective += 1
        elif maxEff == 0.5:
            notVeryEffective += 1
        elif maxEff == 1:
            neutral += 1
        elif maxEff == 2:
            superEffective += 1
        elif maxEff >= 4:
            extremelyEffective += 1
    print("Fator\tFrequência Relativa")
    print(f"0x\t{ineffective} / {formCount} = {ineffective / formCount * 100:.1f}%")
    print(f"0.25x\t{mostlyIneffective} / {formCount} = {mostlyIneffective / formCount * 100:.1f}%")
    print(f"0.5x\t{notVeryEffective} / {formCount} = {notVeryEffective / formCount * 100:.1f}%")
    print(f"1x\t{neutral} / {formCount} = {neutral / formCount * 100:.1f}%")
    print(f"2x\t{superEffective} / {formCount} = {superEffective / formCount * 100:.1f}%")
    print(f"4x\t{extremelyEffective} / {formCount} = {extremelyEffective / formCount * 100:.1f}%")

def printTypeEffectivenessTable(movesetTypes: list[int], attackerAbility = None, filter = [0, 0.25, 0.5, 1, 2, 4]):
    print("Target\t\t\t| Target Types\t\t\t| Ability\t\t| Mult\t| Attack Type")
    for pokemon in pokemonDict.values():
        eff = calcTypeEffectiveness(movesetTypes, pokemon.types, attackerAbility)
        maxEff = max(eff.values())
        maxEffTypes = [typeNames[k] for k, v in eff.items() if v == maxEff]
        if maxEff in filter:
            print(f"{pokemon.fullName}" + "\t" * (3 - len(f"{pokemon.fullName}") // 8), end="")
            print(f"| {pokemon.types}" +  "\t" * (4 - len(f"| {pokemon.types}") // 8), end="")
            print("| Any" + "\t" * (3 - len("| Any") // 8), end="")
            print(f"| {maxEff:.2f}"+"\t" * (1 - len(f"| {maxEff:.2f}") // 8), end="")
            print(f"| {maxEffTypes}")
                

def buildPokemon():
    for pokemon in pokemonRaw:
        for form in pokemon["forms"]:
            form["types"] = form.get("types", pokemon["forms"][0]["types"])
            form["abilities"] = form.get("abilities", pokemon["forms"][0]["abilities"])
            form["bases"]["HP"] = form["bases"].get("HP", pokemon["forms"][0]["bases"]["HP"])
            form["bases"]["Atk"] = form["bases"].get("Atk", pokemon["forms"][0]["bases"]["Atk"])
            form["bases"]["Def"] = form["bases"].get("Def", pokemon["forms"][0]["bases"]["Def"])
            form["bases"]["SpA"] = form["bases"].get("SpA", pokemon["forms"][0]["bases"]["SpA"])
            form["bases"]["SpD"] = form["bases"].get("SpD", pokemon["forms"][0]["bases"]["SpD"])
            form["bases"]["Spd"] = form["bases"].get("Spd", pokemon["forms"][0]["bases"]["Spd"])
            form["weight"] = form.get("weight", pokemon["forms"][0]["weight"])
            pokemonDict[pokemon["id"] + form["formId"]] = Pokemon(pokemon["id"], pokemon["name"], form, form.get("name", ""), form["types"], form["abilities"], form["bases"], form["weight"])

def buildTypes():
    for type in typeRaw:
        typeDict[type["typeId"]] = Type(type["typeId"], type["typeName"], set(type["damage dealt"]["2"]), set(type["damage dealt"]["0.5"]), set(type["damage dealt"]["0"]))



MENU = """==== Pokémon Coverage Calculator ===
1. Check type Effectiveness | 2. Check final power | 0. Sair"""
yesTuple = ("y", "s", "yes", "sim", "1")
noTuple = ("n", "no", "nao", "não", "0")
quitTuple = ("q", "quit", "exit", "close", "sair")
pokemonRaw = {}
pokemonDict = {}
typeRaw = {}
typeNames = []
typeIds = []
typeDict = {}
filterEff = []
exit = False

with open("pokemon_data.json") as f:
    pokemonRaw = json.load(f)

with open("type_data.json") as f:
    typeRaw = json.load(f)

for type in typeRaw:
    typeIds.append(type["typeId"])
    typeNames.append(type["typeName"])
if len(typeIds) != len(set(typeIds)):
    raise ValueError("Erro em type_data.json: Tipos com mesmo ID")
if len(typeNames) != len(set(typeNames)):
    raise ValueError("Erro em type_data.json: Tipos com o mesmo nome")
for pokemon in pokemonRaw:
    if not pokemon.get("name", ""):
        raise ValueError("Erro em pokemon_data.json: Existem Pokemon sem nome")
    if not pokemon.get("id", ""):
        raise ValueError("Erro em pokemon_data.json: Existem Pokemon sem ID")
buildPokemon()
buildTypes()
for pokemon in pokemonDict.values():
    for type in pokemon.types:
        if type not in typeNames:
            raise ValueError("Erro em JSON: Existem tipos em pokemon_data.json que não existem em type_data.json")
formCount = len(pokemonDict)
typesValid = typeNames + typeIds

print(typeDict[1].name)

while True:
    print(MENU)
    option = getInput("Opção: ")
    match option:
        case "0":
            break
        case "1":
            while True:
                print(f"Entradas válidas: {typesValid}")
                attackTypes = getInput("Introduza os tipos dos moves do atacante (separados por \" \". \"q\" para sair): ")
                if attackTypes in quitTuple:
                    break
                attackTypes = attackTypes.title().split(" ")
                exit = True
                for i in range(0, len(attackTypes)):
                    if isInt(attackTypes[i]):
                        attackTypes[i] = int(attackTypes[i])
                    if attackTypes[i] in typeNames:
                        attackTypes[i] = typeNames.index(attackTypes[i])
                    if attackTypes[i] not in typeIds:
                        print("Pelo menos um dos tipos não é válido; verifique.")
                        exit = False
                        break
                print(attackTypes)
                if exit: break
            printTypeEffectivenessFrequency(attackTypes)
            if confirm("Imprimir tabela?"):
                print("1 - Neutrally effective (1x) | 2. Super Effective (2x) | 3. Not very effective (0.5x)", end="")
                print(" | 4. Extremely effective (4x) | 5. Mostly ineffective (0.25x)", end="")
                print(" | 6. Completely ineffective (0x) | 7. Imprimir todos")
                filter = getInput("Opção (separar por \" \" para selecionar vários): ")
                filter = filter.split(" ")
                for i in range(0, len(filter)):
                    if filter[i] in ("6", "0x", "0"):
                        filterEff.append(0)
                    elif filter[i] in ("5", "0.25x", "0.25"):
                        filterEff.append(0.25)
                        filterEff.append(0.125)
                    elif filter[i] in ("3", "0.5x", "0.5"):
                        filterEff.append(0.5)
                    elif filter[i] in ("1", "1x"):
                        filterEff.append(1)
                    elif filter[i] in ("2", "2x"):
                        filterEff.append(2)
                    elif filter[i] in ("4", "4x"):
                        filterEff.append(4)
                        filterEff.append(8)
                    else:
                        filterEff = [0, 0.125, 0.25, 0.5, 1, 2, 4, 8]
                printTypeEffectivenessTable(attackTypes, filter=filterEff)
                filterEff = []




        case _:
            print("Erro: Opção inválida")

