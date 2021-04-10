# Add-on information
bl_info = {
    "name": "GRD File Importer",
    "author": "Abdrazackov Damir",
    "description": "Import Format Files .grd",
    "version": (0, 5, 0),
    "blender": (2, 91, 2),
    "location": "View3D > Sidebar > GRD File Importer", 
    "category": "Object",
    "support": "COMMUNITY"
}



# Imports
if "bpy" in locals():
    import importlib
    importlib.reload(ui)
    importlib.reload(import_dialog)
else:
    import bpy
    from . import ui
    from . import import_dialog



# Registering modules
def register():
    ui.register()
    import_dialog.register()

# Unregistering modules
def unregister():
    ui.unregister()
    import_dialog.unregister()



if __name__ == "__main__":
    try:
        unregister()
    except Exception as e:
        print(e)
        pass

    register()