import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
# Модуль для работы с двоичными данными 
from struct import unpack # Метод для распаковки данных
# Модуль для создания массива
import numpy as np



class ImportGRDFileDialog(Operator, ImportHelper):
    """ Opens the BlenderFileView """
    # Name for executing the operator
    bl_idname = "import_file.import_grd_file_dialog"
    bl_label = "Import"
    
    # File format for import
    filename_ext = ".grd"
    
    def execute(self, context):
        data = ReadFile(self.filepath)

        print("Format: " + data['fId'])

        return {'FINISHED'}

def ReadFile(fileName):
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
            Z = np.zeros(N)
            for index in range(N):
                z = file.read(4)
                z = unpack("f", z)[0]
                Z[index] = z
            
            data['Z'] = Z

        return data


def register():
    """ Registering add-on classes """
    bpy.utils.register_class(ImportGRDFileDialog)
    
def unregister():
    """ Unregistering add-on classes """
    bpy.utils.unregister_class(ImportGRDFileDialog)

if __name__ == "__main__":
    register()