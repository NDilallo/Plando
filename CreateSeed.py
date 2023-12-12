import json
from index_mapping import enter, exits, boss_enter, boss_exits

def create_seed(user_choices: dict):
    # Open the json file titled 'seed.json' in 'read-write' mode
    with open("seed.json", "r+") as file:
        jsonData = json.load(file)
        entrances = jsonData.get("entrances")
        
        for key, val in user_choices.items():  # Use .items() to access keys and values
            key_enter = enter[key]
            key_exit = exits[key]
            val_enter = enter[val]
            val_exit = exits[val]

            for entrance_dict in entrances:
                if entrance_dict["index"] == key_enter:
                    entrance_dict["override"] = val_enter
                if entrance_dict["index"] == val_exit:
                    entrance_dict["override"] = key_exit
            
        # Move to the beginning of the file to rewrite it with updated jsonData
        file.seek(0)
        json.dump(jsonData, file, indent=4)
        file.truncate()  # Remove any remaining content if new content is smaller


def create_seed_bosses(user_choices: dict):
    # Open the json file titled 'seed.json' in 'read-write' mode
    print("yo")
    with open("seed.json", "r+") as file:
        jsonData = json.load(file)
        entrances = jsonData.get("entrances")
        
        for key, val in user_choices.items():  # Use .items() to access keys and values
            print("in here")
            print(key, val)
            key_enter = boss_enter[key]
            key_exit = boss_exits[key]
            val_enter = boss_enter[val]
            val_exit = boss_exits[val]
            print("Past declaraitons")

            for entrance_dict in entrances:
                print("In seoncd loop")
                print(entrance_dict)
                if entrance_dict["index"] == key_enter:
                    entrance_dict["override"] = val_enter
                if entrance_dict["index"] == val_exit:
                    entrance_dict["override"] = key_exit
                print("Through")
            
        # Move to the beginning of the file to rewrite it with updated jsonData
        file.seek(0)
        json.dump(jsonData, file, indent=4)
        file.truncate()  # Remove any remaining content if new content is smaller
