### MODULES

import bpy
from bpy.types import Panel

### UI

class GRDImporterPanel(Panel):
    """ Add-on Panel For Import A .GRD Files """ 
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GRD File Importer"
    bl_label = "Import"
    
    def draw(self, context):
        """ Panel Rendering """
        layout = self.layout
        layout.operator("import_file.import_grd_file")
    
### REG- & UNREGISTRATION
        
def register():
    """ Registering Add-on Classes """
    bpy.utils.register_class(GRDImporterPanel)
    
def unregister():
    """ Unregistering Add-on Classes """
    bpy.utils.unregister_class(GRDImporterPanel)