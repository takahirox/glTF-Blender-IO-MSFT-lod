import bpy
from io_scene_gltf2.blender.exp import gltf2_blender_gather_nodes
from io_scene_gltf2.blender.imp.gltf2_blender_node import BlenderNode

bl_info = {
    "name" : "glTF MSFT_lod IO",
    "author" : "Takahiro Aoyagi",
    "description" : "Addon for glTF MSFT_lod extension",
    "blender" : (3, 3, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "wiki_url": "https://github.com/takahirox/glTF-Blender-IO-MSFT-lod",
    "tracker_url": "https://github.com/takahirox/glTF-Blender-IO-MSFT-lod/issues",
    "support": "COMMUNITY",
    "warning" : "",
    "category" : "Generic"
}

glTF_extension_name = "MSFT_lod"
MSFT_lod_screencoverage_name = "MSFT_screencoverage"

# Properties

class LevelProperties(bpy.types.PropertyGroup):
    object: bpy.props.PointerProperty(
        name="object",
        description="LOD object",
        type=bpy.types.Object
    )
    coverage: bpy.props.FloatProperty(
        name="coverage",
        soft_max=1.0,
        soft_min=0.0
    )

class LevelArrayProperty(bpy.types.PropertyGroup):
    value: bpy.props.CollectionProperty(name="value", type=LevelProperties)

# Operators

class AddLevel(bpy.types.Operator):
    bl_idname = "wm.add_level"
    bl_label = "Add Level"

    def execute(self, context):
        props = context.object.LevelArrayProperty.value
        props.add()
        return {"FINISHED"}

class RemoveLevel(bpy.types.Operator):
    bl_idname = "wm.remove_level"
    bl_label = "Remove Level"

    # Set by NodePanel
    index: bpy.props.IntProperty(name="index")

    def execute(self, context):
        props = context.object.LevelArrayProperty.value
        props.remove(self.index)
        return {"FINISHED"}

# Panel

class NodePanel(bpy.types.Panel):
    bl_label = "Level Of Details"
    bl_idname = "NODE_PT_LOD"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        props = context.object.LevelArrayProperty.value
        for i, prop in enumerate(props):
            row = layout.row()
            row.label(text="LOD" + str(i + 1))

            remove_operator = row.operator(
                "wm.remove_level",
                text="",
                icon="X"
            )
            remove_operator.index = i

            layout.prop(prop, "object")

            row = layout.row()
            row.label(text="coverage")
            row.prop(prop, "coverage", text="")

            layout.separator()

        layout.operator(
            "wm.add_level",
            text="Add Level",
            icon="ADD"
        )

# Register/Unregister

def register():
    bpy.utils.register_class(NodePanel)
    bpy.utils.register_class(LevelProperties)
    bpy.utils.register_class(LevelArrayProperty)
    bpy.utils.register_class(AddLevel)
    bpy.utils.register_class(RemoveLevel)
    bpy.types.Object.LevelArrayProperty = bpy.props.PointerProperty(type=LevelArrayProperty)

def unregister():
    bpy.utils.unregister_class(NodePanel)
    bpy.utils.unregister_class(LevelProperties)
    bpy.utils.unregister_class(LevelArrayProperty)
    bpy.utils.unregister_class(AddLevel)
    bpy.utils.unregister_class(RemoveLevel)
    del bpy.types.Object.LevelArrayProperty

# Import

class glTF2ImportUserExtension:
    def gather_import_node_after_hook(self, vnode, gltf_node, blender_object, import_settings):
        # See below.
        if hasattr(vnode, "levels"):
            for level in vnode.levels:
                level.object = blender_object
            delattr(vnode, "levels")

        if gltf_node.extensions is None or glTF_extension_name not in gltf_node.extensions:
            return

        extension = gltf_node.extensions[glTF_extension_name]
        ids = extension["ids"]

        coverages = []
        if gltf_node.extras is not None and MSFT_lod_screencoverage_name in gltf_node.extras:
            coverages = gltf_node.extras[MSFT_lod_screencoverage_name]

        levels = blender_object.LevelArrayProperty.value
        for i, id in enumerate(ids):
            level = levels.add()

            if i < len(coverages):
                level.coverage = coverages[i]
            else:
                level.coverage = 0.0

            # Set object if blender_object is already initialized.
            # Otherwise save level and set object when it's initialized.
            vnode = import_settings.vnodes[id]
            if hasattr(vnode, "blender_object"):
                level.object = vnode.blender_object
            else:
                if not hasattr(vnode, "levels"):
                    vnode.levels = []
                vnode.levels.append(level)

# Export

def findNodeIndex(nodes, name):
    for i, node in enumerate(nodes):
        if node.name == name:
            return i
    raise RuntimeError("glTF MSFT_lod addon: node whose name is %s not found" % name)

class glTF2ExportUserExtension:
    def __init__(self):
        from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
        self.Extension = Extension

    def gather_node_hook(self, gltf_node, blender_object, export_settings):
        # Just in case
        if blender_object.LevelArrayProperty is None:
            return

        levels = blender_object.LevelArrayProperty.value
        if len(levels) == 0:
            return

        names = []
        coverages = []
        for level in levels:
            if level.object is None:
                raise RuntimeError("glTF MSFT_lod addon: LOD object must be specified")
            names.append(level.object.name)
            coverages.append(level.coverage)

        coverages.append(0.0)

        if gltf_node.extensions is None:
            gltf_node.extensions = {}
        gltf_node.extensions[glTF_extension_name] = self.Extension(
            name=glTF_extension_name,
            extension={"names": names}, # Replace with node indices as ids in gather_gltf_extensions_hook
            required=False
        )

        if gltf_node.extras is None:
            gltf_node.extras = {}
        gltf_node.extras[MSFT_lod_screencoverage_name] = coverages

    def gather_gltf_extensions_hook(self, gltf_root, export_settings):
        nodes = gltf_root.nodes
        low_level_ids = {}

        # Find node indices from object(node) names.
        # Assuming that objects have unique names.
        # @TODO: It's inefficient. Any better and more efficient way?

        for node in nodes:
            ids = []
            if node.extensions is None or glTF_extension_name not in node.extensions:
                continue
            extension = node.extensions[glTF_extension_name]
            names = extension["names"]
            del extension["names"]
            for name in names:
                index = findNodeIndex(nodes, name)
                ids.append(index)
                low_level_ids[index] = True
            extension["ids"] = ids

        # Remove references from scene.nodes and node.children
        # to nodes that are lower levels of a certain object
        # @TODO: Add a property indicating whether they should
        #        be removed or not?

        for scene in gltf_root.scenes:
            if scene.nodes is None:
                continue
            for key in low_level_ids.keys():
                if key in scene.nodes:
                    scene.nodes.remove(key)

        for node in nodes:
            if node.children is None:
                continue
            for key in low_level_ids.keys():
                if key in node.children:
                    node.children.remove(key)
