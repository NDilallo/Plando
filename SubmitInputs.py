from index_mapping import entrances, exits


#Creates a list of tuples holding input pairs
def submit_inputs(inputs: dict) -> list:
    print(f"here {inputs}")
    index_pairs = []
    for item1, item2 in inputs.items():
        print(item1, item2)
        index_pairs.append( ( entrances.get(item1), exits.get(item1), entrances.get(item2), exits.get(item2) ) )
    print("DONE")
    return index_pairs