import json


# Takes a list of index pairs and connects each pair - 2 Way entrances only - i.e. going through a zone then going back takes you back where you were
def updateSeed(indexMaps: list) -> None:
    with open("seed.json", "r+") as file:
        jsonData = json.load(file)
        entrances = jsonData.get("entrances")
        
        for index1Enter, index1Exit, index2Enter, index2Exit in indexMaps:
            found = False
            for entrance_dict in entrances:
                if entrance_dict.get("index") == index1Enter:
                    entrance_dict["override"] = index2Enter
                    found = True
                if entrance_dict.get("index") == index2Exit:
                    entrance_dict["override"] = index1Exit
            if not found:
                custom_entrance = {
                    "index": index1Enter,
                    "destination": 936, #Doesnt matter?
                    "blueWarp": 0,#Doesnt matter?
                    "override": index2Enter,
                    "overrideDestination": 578#Doesnt matter?
                }
                custom_exit = {
                    "index": index2Exit,
                    "destination": 936, #Doesnt matter?
                    "blueWarp": 0,#Doesnt matter?
                    "override": index1Exit,
                    "overrideDestination": 578#Doesnt matter?
                }
                entrances.append(custom_entrance)
                entrances.append(custom_exit)
        
        # Move to the beginning of the file to rewrite it with updated jsonData
        file.seek(0)
        json.dump(jsonData, file, indent=4)
        file.truncate()  # Remove any remaining content if new content is smaller

