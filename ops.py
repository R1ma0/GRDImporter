import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator
# Модуль для работы с двоичными данными 
from struct import unpack # Метод для распаковки данных
# Модуль для создания массива
import numpy as np



# OPERATORS

class ImportGRDFile(Operator, ImportHelper):
    """ Opens the BlenderFileView """
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
        with open("D:\\VolSU\\3 курс\\2 семестр\\НИР\\GRDImporter\\data.txt", "w") as file:
            for item in data:
                file.write(str(data.get(item)) + '\n')
        self.createMesh(data, "GRD_DATA_OBJ")

        return {'FINISHED'}

    def readFile(self, fileName):
            # Словарь для хранения считанных значений
            data = dict()

            # Открытие файла для чтения в двоичном режиме  
            with open(fileName, 'rb') as file:
                # Чтение и распоковка заголовков 
                # Идентификатор файла
                fId = file.read(4)
                fId = fId.decode('utf-8')
                data['fId'] = fId

                # Число колонок сетки
                sNx = file.read(2)
                sNx = unpack('h', sNx)[0]
                data['sNx'] = sNx

                # Число строк сетки
                sNy = file.read(2)
                sNy = unpack('h', sNy)[0]
                data['sNy'] = sNy

                # Минимальное значение Х на сетке 
                xMin = file.read(8)
                xMin = unpack('d', xMin)[0]
                data['xMin'] = xMin

                # Максимальное значение Х на сетке
                xMax = file.read(8)
                xMax = unpack('d', xMax)[0]
                data['xMax'] = xMax

                # Минимальное значение У на сетке 
                yMin = file.read(8)
                yMin = unpack('d', yMin)[0]
                data['yMin'] = yMin

                # Максимальное значение У на сетке
                yMax = file.read(8)
                yMax = unpack('d', yMax)[0]
                data['yMax'] = yMax

                # Минимальное значение Z на сетке 
                zMin = file.read(8)
                zMin = unpack('d', zMin)[0]
                data['zMin'] = zMin

                # Максимальное значение Z на сетке
                zMax = file.read(8)
                zMax = unpack('d', zMax)[0]
                data['zMax'] = zMax
                
                # Общее число элементов сетки
                N = sNx * sNy

                # Чтение основных данных
                Z = [ [0] * 3 for i in range(N) ]

                xCoord = 1
                yCoord = 0

                for i in range(N):
                    zCoord = file.read(4)
                    zCoord = unpack('f', zCoord)[0]
                    zCoord = round(zCoord, 3)

                    Z[i] = [xCoord, yCoord, zCoord]
                    
                    if xCoord < sNx:
                        xCoord += 1
                    else:
                        xCoord = 1
                        yCoord += 1

                data['Z'] = Z

            return data

    def createMesh(self, data, objhName):
        # Mesh data
        vertices = data['Z']
        edges    = []
        faces    = self.mergeVertexesIntoPolygons(data)

        # Create mesh
        mesh = bpy.data.meshes.new(objhName)
        # Generate mesh data
        mesh.from_pydata(vertices, edges, faces)
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
        faces = []
        rowMaxLength = data['sNx']

        for row in range(1, data['sNy'] - 1, 1): # TODO: Должно быть без -1. Последняя строка крашит
            for column in range(data['sNx'] - 1):
                previousRow = row -1 
                face = (
                    column + previousRow * rowMaxLength, 
                    column + previousRow * rowMaxLength + 1, 
                    column + row * rowMaxLength + 1, 
                    column + row * rowMaxLength
                )
                faces.append(face)

        return faces



def register():
    """ Registering add-on classes """
    bpy.utils.register_class(ImportGRDFile)
    
def unregister():
    """ Unregistering add-on classes """
    bpy.utils.unregister_class(ImportGRDFile)

if __name__ == "__main__":
    register()