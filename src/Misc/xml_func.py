import xml.etree.ElementTree as ET
from src.Globals import settings
from src.Misc.Save_Data import SaveData, display_data

def load(path: str):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        
        if root.tag != settings.ROOT_NAME:
            return "Error: File format isn't supported"
        return root

    except FileNotFoundError:
        return f"Error: No such file or Directory: {path}"
    
def update(root: ET.Element):
    for child in root:
        if child.tag == settings.PLAYER_DATA_ROOT_NAME:
            SaveData.damage = int(child.find("damage").text)  
            SaveData.seed = int(child.find("seed").text) or 0 
            SaveData.floor = int(child.find("floor").text) or 0   
            SaveData.health = int(child.find("health").text) or 0   
            SaveData.kills = int(child.find("kills").text) or 0 
            print("Updated") 
            display_data() 

def save(path: str):
    root = ET.Element(settings.ROOT_NAME)
    
    child = ET.SubElement(root, settings.PLAYER_DATA_ROOT_NAME)
    ET.SubElement(child, "kills").text = str(SaveData.kills)
    ET.SubElement(child, "level").text = str(SaveData.level)
    ET.SubElement(child, "floor").text = str(SaveData.floor)
    ET.SubElement(child, "health").text = str(SaveData.health)
    ET.SubElement(child, "damage").text = str(SaveData.damage)
    ET.SubElement(child, "seed").text = str(int(SaveData.seed))

    print("Saved") 
    display_data() 

    tree = ET.ElementTree(root)
    tree.write(path, xml_declaration=True)
