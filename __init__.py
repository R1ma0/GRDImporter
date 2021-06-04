### ADD-ON INFORMATION

bl_info = {
    "name": "GRD File Importer",
    "author": "Abdrazackov Damir",
    "description": "Import Format Files .GRD",
    "version": (1, 1, 0),
    "blender": (2, 91, 2),
    "location": "View3D > Sidebar > GRD File Importer", 
    "category": "Import-Export",
    "support": "COMMUNITY",
}

### IMPORTS

if "bpy" in locals():
    import importlib
    importlib.reload(ui)
    importlib.reload(grd_import)
else:
    import bpy
    from . import ui
    from . import grd_import

### REG- & UNREGISTRATION 

def register():
    ui.register()
    grd_import.register()

def unregister():
    ui.unregister()
    grd_import.unregister()

### LAUNCH POINT

if __name__ == "__main__":
    try:
        unregister()
    except Exception as e:
        print("Exception: " + e)
        pass

    register()