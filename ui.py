import bpy
from bpy.types import Panel



class GRDUIPanelTemplate(Panel):
    """ Template for add-on panels """
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GRD File Importer"

class GRDImporterPanel(GRDUIPanelTemplate):
    """ Add-on panel for import a .grd files """ 
    bl_label = "Import"
    
    def draw(self, context):
        """ Panel rendering """
        layout = self.layout
        layout.operator("import_file.import_grd_file")
    
    
        
def register():
    """ Registering add-on classes """
    bpy.utils.register_class(GRDImporterPanel)
    
def unregister():
    """ Unregistering add-on classes """
    bpy.utils.unregister_class(GRDImporterPanel)

if __name__ == "__main__":
    register()