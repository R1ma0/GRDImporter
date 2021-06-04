### ADD-ON INFORMATION

bl_info = {
    "name": "GRD File Importer",
    "author": "Abdrazackov Damir",
    "description": "Import Format Files .GRD",
    "version": (1, 0, 0),
    "blender": (2, 91, 2),
    "location": "View3D > Sidebar > GRD File Importer", 
    "category": "Object",
    "support": "COMMUNITY"
}

### IMPORTS

if "bpy" in locals():
    import importlib
    importlib.reload(grd_importer-ui)
    importlib.reload(grd_importer-main)
else:
    import bpy
    from . import grd_importer-ui
    from . import grd_importer-main

### REG- & UNREGISTRATION 

def register():
    grd_importer-ui.register()
    grd_importer-main.register()

def unregister():
    grd_importer-ui.unregister()
    grd_importer-main.unregister()

### LAUNCH POINT

if __name__ == "__main__":
    try:
        unregister()
    except Exception as e:
        print(e)
        pass

    register()