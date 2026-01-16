from src import compare

def get_results(champ, opps):

    comp = compare.Compare(champ, opps)
    item_counters = comp.compare()

    return(item_counters)


