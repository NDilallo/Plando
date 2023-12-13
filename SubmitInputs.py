from index_mapping import entrances, exits, warp_songs


#Creates a list of tuples holding input pairs
def submit_inputs_dungeons_bosses(inputs: dict) -> list:
    index_pairs = []
    for item1, item2 in inputs.items():
        index_pairs.append( ( entrances.get(item1), exits.get(item1), entrances.get(item2), exits.get(item2) ) )
    return index_pairs


def submit_inputs_warp_songs(inputs: dict) -> list:
    index_pairs = []
    for song, destination in inputs.items():
        destination_decimal = int(destination, 16) #Converts destination input from hex to decimal
        index_pairs.append( (warp_songs.get(song), -1, destination_decimal, -1) )
    return index_pairs