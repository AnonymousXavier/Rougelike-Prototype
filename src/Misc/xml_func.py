import os
import xml.etree.ElementTree as ET
from src.Globals import settings
from src.Misc.Save_Data import SaveData, reset

def load(path: str):
    if not os.path.exists(path):
        # Create a default save if it doesn't exist
        reset() # Reset Save Data
        save(path)
        print(f"No save found. Created default save at {path}")

    try:
        tree = ET.parse(path)
        root = tree.getroot()
        
        if root.tag != settings.ROOT_NAME:
            return "Error: File format isn't supported"
        return root

    except ET.ParseError:
        return "Error: Failed to parse save file"
    
def update(root: ET.Element):
    for child in root:
        if child.tag == settings.PLAYER_DATA_ROOT_NAME:
            SaveData.damage = int(child.find("damage").text)  
            SaveData.seed = int(child.find("seed").text) or 0 
            SaveData.floor = int(child.find("floor").text) or 0   
            SaveData.health = int(child.find("health").text) or 0   
            SaveData.kills = int(child.find("kills").text) or 0 

def save(path: str):
    root = ET.Element(settings.ROOT_NAME)
    
    child = ET.SubElement(root, settings.PLAYER_DATA_ROOT_NAME)
    ET.SubElement(child, "kills").text = str(int(SaveData.kills))
    ET.SubElement(child, "level").text = str(int(SaveData.level))
    ET.SubElement(child, "floor").text = str(int(SaveData.floor))
    ET.SubElement(child, "health").text = str(int(SaveData.health))
    ET.SubElement(child, "damage").text = str(int(SaveData.damage))
    ET.SubElement(child, "seed").text = str(int(SaveData.seed))


    tree = ET.ElementTree(root)
    tree.write(path, xml_declaration=True)
