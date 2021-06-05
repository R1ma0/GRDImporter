### MODULES

import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator
from struct import unpack # Method for unpacking data

### ADD-ON INFORMATION

bl_info = {
    "name": ".GRD Importer",
    "author": "Abdrazackov Damir",
    "description": "Import Format Files .GRD",
    "version": (1, 3, 0),
    "blender": (2, 91, 2),
    "location": "File > Import > Surfer 6 Binary (.grd)", 
    "category": "Import-Export",
    "support": "COMMUNITY",
}

### OPERATORS

class ImportGRDFile(Operator, ImportHelper):
    """ Opens The BlenderFileView """
    # Name for executing the operator
    bl_idname = "import_file.import_grd_file"
    bl_label = "Surfer 6 Binary (.grd)"
    
    # File format for import
    filename_ext = ".grd"

    filter_glob: StringProperty(
        default = "*.grd",
        options = {'HIDDEN'},
        maxlen = 255
    )
    
    def execute(self, context):
        data = self.read_file(self.filepath)
        self.create_mesh(data, "GRD_DATA_OBJ")
        return {'FINISHED'}

    def read_file(self, fileName):
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
            # Number of columns and rows
            rowsColumnsHeaderProperties = ['sNx', 'sNy']
            for property in rowsColumnsHeaderProperties:
                data[property] = self.read_and_unpuck(file, 2)
            # Minimum and maximum values of X, Y, Z coordinates
            xyzHeaderProperties = ['xMin', 'xMax', 'yMin', 'yMax', 'zMin', 'zMax']
            for property in xyzHeaderProperties:
                data[property] = self.read_and_unpuck(file, 8)
            # Total number of grid elements
            N = data['sNx'] * data['sNy']
            # Reading data
            Z = [ [0] * 3 for i in range(N) ]
            xCoord = 1
            yCoord = 0
            for i in range(N):
                zCoord = self.read_and_unpuck(file, 4)
                zCoord = round(zCoord, 6)
                Z[i] = [xCoord, yCoord, zCoord]
                if xCoord < data['sNx']:
                    xCoord += 1
                else:
                    xCoord = 1
                    yCoord += 1
            data['Z'] = Z
        return data

    def read_and_unpuck(self, file, size):
        """ Reading And Unpacking Binary Data """
        element = file.read(size)
        if size == 8: # Double
            element = unpack('d', element)[0]
        elif size == 2: # Short
            element = unpack('h', element)[0]
        elif size == 4: # Float
            element = unpack('f', element)[0]
        return element
    
    def create_mesh(self, data, objhName):
        """ Creating A Grid Based On Data """
        # Mesh data
        vertices = data['Z']
        faces    = self.merge_vertexes_into_polygons(data)
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

    def merge_vertexes_into_polygons(self, data):
        """ Connecting Vertexes To Polygons """
        faces = []
        for row in range(1, data['sNy'], 1):
            for column in range(data['sNx'] - 1):
                previousRow = row -1 
                face = (
                    column + previousRow * data['sNx'], 
                    column + previousRow * data['sNx'] + 1, 
                    column + row * data['sNx'] + 1, 
                    column + row * data['sNx']
                )
                faces.append(face)
        return faces

### UI

def set_ui(self, context):
    """ Implements The Addon Interface """
    self.layout.operator(ImportGRDFile.bl_idname, text="Surfer 6 Binary (.grd)")

### REG- & UNREGISTRATION

def register():
    """ Registering Add-on Classes """
    bpy.utils.register_class(ImportGRDFile)
    bpy.types.TOPBAR_MT_file_import.append(set_ui)
    
def unregister():
    """ Unregistering Add-on Classes """
    bpy.utils.unregister_class(ImportGRDFile)
    bpy.types.TOPBAR_MT_file_import.remove(set_ui)

### ADD-ON EXIT POINT

if __name__ == "__main__":
    register()
