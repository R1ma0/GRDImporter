### MODULES

import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator
# Modul for working with binary data
from struct import unpack # Method for unpacking data

### OPERATORS

class ImportGRDFile(Operator, ImportHelper):
    """ Opens The BlenderFileView """
    # Name for executing the operator
    bl_idname = "import_file.import_grd_file"
    bl_label = "Import"
    
    # File format for import
    filename_ext = ".grd"

    filter_glob: StringProperty(
        default = "*.grd",
        options = {'HIDDEN'},
        maxlen = 255
    )
    
    def execute(self, context):
        data = self.readFile(self.filepath)
        self.createMesh(data, "GRD_DATA_OBJ")
        return {'FINISHED'}

    def readFile(self, fileName):
        """ Reading A Binary File """
        # Dictionary for storing read values
        data = dict()
        # Opening a file for reading
        with open(fileName, 'rb') as file:
            # Reading and unpacking headers
            # File ID
            fId = file.read(4)
            fId = fId.decode('utf-8')
            data['fId'] = fId
            # Number of columns
            sNx = self.readAndUnpuck(file, 2)
            data['sNx'] = sNx
            # Number of rows
            sNy = self.readAndUnpuck(file, 2)
            data['sNy'] = sNy
            # Minimum value of X on the grid
            data['xMin'] = self.readAndUnpuck(file, 8)
            # Maximum value if X on the grid
            data['xMax'] = self.readAndUnpuck(file, 8)
            # Minimum value of Y on the grid
            data['yMin'] = self.readAndUnpuck(file, 8)
            # Maximum value if Y on the grid
            data['yMax'] = self.readAndUnpuck(file, 8)
            # Minimum value of Y on the grid 
            data['zMin'] = self.readAndUnpuck(file, 8)
            # Maximum value if Z on the grid
            data['zMax'] = self.readAndUnpuck(file, 8)
            # Total number of grid elements
            N = sNx * sNy
            # Reading data
            Z = [ [0] * 3 for i in range(N) ]
            xCoord = 1
            yCoord = 0
            for i in range(N):
                zCoord = self.readAndUnpuck(file, 4)
                zCoord = round(zCoord, 6)
                Z[i] = [xCoord, yCoord, zCoord]
                if xCoord < sNx:
                    xCoord += 1
                else:
                    xCoord = 1
                    yCoord += 1
            data['Z'] = Z
        return data

    def readAndUnpuck(self, file, size):
        """ Reading And Unpacking Binary Data """
        element = file.read(size)
        if size == 8:
            element = unpack('d', element)[0]
            return element
        elif size == 2:
            element = unpack('h', element)[0]
            return element
        elif size == 4:
            element = unpack('f', element)[0]
            return element
    
    def createMesh(self, data, objhName):
        """ Creating A Grid Based On Data """
        # Mesh data
        vertices = data['Z']
        faces    = self.mergeVertexesIntoPolygons(data)
        # Create mesh
        mesh = bpy.data.meshes.new(objhName)
        # Generate mesh data
        mesh.from_pydata(vertices, [], faces)
        # Update the mesh   
        mesh.update()
        # Create object
        meshObj = bpy.data.objects.new(mesh.name, mesh)
        # Set location
        meshObj.location.x = 0.0
        meshObj.location.y = 0.0
        meshObj.location.z = 0.0
        meshObj.scale = [0.1, 0.1, 0.1]
        # Add object to scene
        bpy.context.scene.collection.objects.link(meshObj)
        return meshObj

    def mergeVertexesIntoPolygons(self, data):
        """ Connecting Vertexes To Polygons """
        faces = []
        rowMaxLength = data['sNx']
        for row in range(1, data['sNy'], 1):
            for column in range(rowMaxLength - 1):
                previousRow = row -1 
                face = (
                    column + previousRow * rowMaxLength, 
                    column + previousRow * rowMaxLength + 1, 
                    column + row * rowMaxLength + 1, 
                    column + row * rowMaxLength
                )
                faces.append(face)
        return faces

### REG- & UNREGISTRATION

def register():
    """ Registering Add-on Classes """
    bpy.utils.register_class(ImportGRDFile)
    
def unregister():
    """ Unregistering Add-on Classes """
    bpy.utils.unregister_class(ImportGRDFile)