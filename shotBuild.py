import yaml
import os.path


m_YamlPath = '/homes/govindaluris/Documents/layerOrder.yaml'
m_nukeTemplatePath = '/homes/govindaluris/Documents/nuke/'

"Reading the yaml file"
def getLayersFromLayerOrder(m_YamlPath):
    with open(m_YamlPath,'r') as stream:
        layers = yaml.load(stream)
        return layers



def formatLayerNames(layers):
    formattedLayers = []
    for layer in layers:
        formattedLayers.append(layer.split('_')[-1])
    return formattedLayers


def shotCompBuild():
    orderedLayers = {}
    charLayers = []
    envirLayers = []
    fxLayers = []
    miscLayers = []

    layers =  getLayersFromLayerOrder(m_YamlPath)   

    for key in layers:
        if key.lower() == "char":
            layer = layers[key]
        elif key.lower() == "envir":
            layer = layers[key]
        elif key.lower() == "fx":
            layer = layers[key]
        else:
            layer = layers[key]

        createTemplates(layer,key.lower())
        

def createTemplates(layers,type):
    fLayers = formatLayerNames(layers)
    templateScriptPath = m_nukeTemplatePath + type.lower() + ".nk"
    curScript = nuke.toNode("root").name()
    if os.path.isfile(templateScriptPath):
        for layer in fLayers:
            print layer
            nuke.scriptReadFile(templateScriptPath)
            
            formatBackground(layer)
            nuke.scriptSave(curScript)
    else:
        nuke.message("No template for " %S,type)


 
def formatBackground(nodeName):
    nodes = nuke.selectedNodes()
    if nodes == []:
        nuke.message('Please Select a Backdrop')
        return None
    bd = nuke.selectedNodes("BackdropNode")
    templateName = nodeName
    for node in nodes:
        nodeLabel = node["name"].getValue()
        newName = nodeLabel + "_" + templateName.lower()
        node["name"].setValue(newName)

        
shotCompBuild()        

m_menu = nuke.menu('Nuke').addMenu('Format Background')
m_menu.addCommand('Rename Nodes','formatBackground()')

n = nuke.toNode("Read_envir")
n.setSelected(True)


print nuke.toNode("root").name()