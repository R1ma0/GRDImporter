import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator
# Модуль для работы с двоичными данными 
from struct import unpack # Метод для распаковки данных
# Модуль для создания массива
import numpy as np



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
        self.createMesh(data, "My_Object")

        return {'FINISHED'}

    def readFile(self, fileName):
            # Словарь для хранения считанных значений
            data = dict()

            # Открытие файла для чтения в двоичном режиме  
            with open(fileName, 'rb') as file:
                # Чтение и распоковка заголовков 
                # Идентификатор файла
                fId = file.read(4)
                data['fId'] = fId.decode('utf-8')

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
                data['xMin'] = unpack('d', xMin)[0]

                # Максимальное значение Х на сетке
                xMax = file.read(8)
                data['xMax'] = unpack('d', xMax)[0]

                # Минимальное значение У на сетке 
                yMin = file.read(8)
                data['yMin'] = unpack('d', yMin)[0]

                # Максимальное значение У на сетке
                yMax = file.read(8)
                data['yMax'] = unpack('d', yMax)[0]

                # Минимальное значение Z на сетке 
                zMin = file.read(8)
                data['zMin'] = unpack('d', zMin)[0]

                # Максимальное значение Z на сетке
                zMax = file.read(8)
                data['zMax'] = unpack('d', zMax)[0]
                
                # Общее число элементов сетки
                N = sNx * sNy
                data['N'] = N

                # Чтение основных данных
                Z = [ [0] * 3 for i in range(N) ]

                xCoord = 0
                yCoord = 0

                for i in range(N):
                    zCoord = file.read(4)
                    zCoord = unpack("f", zCoord)[0]

                    Z[i] = [xCoord, yCoord, zCoord]

                    if xCoord < sNx:
                        xCoord += 1
                    else:
                        xCoord = 0
                        yCoord += 1

                data['Z'] = Z

            return data

    def createMesh(self, data, objhName):
        # Mesh data
        vertices = data['Z']
        edges    = []
        faces    = []

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

        # Add object to scene
        bpy.context.scene.collection.objects.link(meshObj)

        return meshObj


def register():
    """ Registering add-on classes """
    bpy.utils.register_class(ImportGRDFile)
    
def unregister():
    """ Unregistering add-on classes """
    bpy.utils.unregister_class(ImportGRDFile)

if __name__ == "__main__":
    register()