#from bin_wise.store import VectorStore
from bin_wise import separate
from bin_wise import material_checker

def ask(text):
    target, municipalities = separate.separate(text)  
    material = material_checker.get_material_info(target)
    #result = VectorStore.search_item(municipalities, material)
    return result
