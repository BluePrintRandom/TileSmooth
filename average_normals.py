import bge, bpy, mathutils

cont = bge.logic.getCurrentController()
own = cont.owner
Tile = own
own = own.scene.objects['Cube']


if Tile['Tile']==2:
    object1 = bpy.data.objects[Tile.name]
    Normals = {}
    vertFaces = {}
    for poly in object1.data.polygons:
        normal = None
        verts = []
        for vert in poly.vertices:
            verts.append(object1.data.vertices[vert].co)
            if vert not in vertFaces:
                vertFaces[vert] = [poly.index]
            else:    
                vertFaces[vert].append(poly.index)
                
        normal = mathutils.geometry.normal(verts)     
        
            
            
        Normals[poly.index] = normal
    
    for vertex in object1.data.vertices:
        avg = None
        for vertFace in vertFaces[vertex.index]:
            normal = Normals[vertFace]
            if avg ==None:
                avg = normal
            else:
                avg = ((normal+avg)*.5).normalized()    
        vertex.normal = avg
            
    #print('set normals')   
    Tile['Tile']-=1  
    
        
if Tile['Tile']==1:
    
    depsgraph = bpy.context.evaluated_depsgraph_get()
    close = Tile['close'] # kd.findRange(tile location, scale)
    entry = Tile['entry'] # Tile index own['SpawnedTile][entry]

    #print(close)

    

    object1 = bpy.data.objects[Tile.name]
    overlaps = {}         
    bvhtreeOwn = mathutils.bvhtree.BVHTree.FromObject(object1, depsgraph)

    for entry2 in close:
        if entry2[1] in own['SpawnedTiles'] and entry[1]!=entry2[1]:
             object2 = bpy.data.objects[own['SpawnedTiles'][entry2[1]][2].name]
             
             bvhtreeOther = mathutils.bvhtree.BVHTree.FromObject(object2, depsgraph)
             overlaping = bvhtreeOwn.overlap(bvhtreeOther)
             #print(overlaping)
             for overlap in overlaping:
                 #print(overlap)
                 if overlap[0] not in overlaps:
                     overlaps[overlap[0]] =[ ( own['SpawnedTiles'][entry2[1]][2].name , overlap[1] , object2.matrix_world) ]
                 else:
                      overlaps[overlap[0]].append(  ( own['SpawnedTiles'][entry2[1]][2].name , overlap[1],object2.matrix_world ) )

    #print(overlaps)
    for index in overlaps:
        average = object1.matrix_world @ object1.data.vertices[index].normal
        for entry3 in overlaps[index]:
            normal = entry3[2] @ bpy.data.objects[entry3[0]].data.vertices[entry3[1]].normal
            if average==None:
                average = normal
            else:
                average = ((normal+average)*.5).normalized()
        for entry3 in overlaps[index]:
           bpy.data.objects[entry3[0]].data.vertices[entry3[1]].normal = entry3[2].inverted() @ average.normalized() 
            
        object1.data.vertices[index].normal = object1.matrix_world.inverted() @ average.normalized()      
    
    #print('averaged normals')    
    Tile['Tile']-=1       
