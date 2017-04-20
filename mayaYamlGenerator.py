import maya.cmds as cmds
import pymel.core as pm

def getCamDistancePerFrame(shotCam,asset):
    cam = pm.PyNode(shotCam)
    cam_normal =  cam.getAttr('worldMatrix').transpose() * pm.dt.Vector([0,0,-1])
    cam_normal.normalize()
    cam_position = cam.getAttr('worldMatrix').translate   
    distance_object = pm.PyNode(asset)
    object_vector = distance_object.getAttr('parentMatrix').translate + distance_object.getAttr('center') - cam_position
    #print object_vector.dot(cam_normal)
    return object_vector.dot(cam_normal)

def getMinimumCamDistance(shotCam,asset):
    playbackStartTime  = int(cmds.playbackOptions(query=True, min=True)) 
    playbackEndTime    = int(cmds.playbackOptions(query=True, max=True))
    curTime = playbackStartTime
    distanceList = []
    for i in range(playbackStartTime,playbackEndTime):
        curTime = cmds.currentTime( curTime+1, edit=True )
        distanceList.append(getCamDistancePerFrame(shotCam,asset))
    return min(distanceList)
    
def getLayerOrder():
    layerOrder = {}
    shotCam = 'shotCam'
    renderLayers = getRenderLayers()
    renderLayers.remove('defaultRenderLayer')
    for renderLayer in renderLayers:
        objectsInLayer = getRenderLayerObjects(renderLayer)
        minDistance = []
        for object in objectsInLayer:
            if 'Light' not in cmds.nodeType( object ):
                print object
                minDistance.append(getMinimumCamDistance(shotCam,object))
        minDistanceOfLayer = min(minDistance)
        layerOrder[renderLayer] = minDistanceOfLayer
    print layerOrder
                                 
def getFrameRange():
    frameRange = [cmds.getAttr('defaultRenderGlobals.startFrame'),cmds.getAttr('defaultRenderGlobals.endFrame')]
    return frameRange
    
def getRenderLayers():
    renderLayers = cmds.ls( type='renderLayer')
    return renderLayers
    
def getRenderLayerObjects(renderLayer):
    objectsInLayer = cmds.editRenderLayerMembers( renderLayer, q = True)
    return objectsInLayer
    
getLayerOrder()
