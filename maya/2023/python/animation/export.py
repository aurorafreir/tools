"""
Trans Rights are Human Rights

"""
# SYSTEM IMPORTS
import pathlib

# STANDARD LIBRARY IMPORTS
import pymel.core as pm

# LOCAL APPLICATION IMPORTS
from core import files


def export_anim_per_ref():
    """
    Exports an fbx per imported reference
    """
    full_path, file_name, raw_name, extension = files.current_paths()

    namespaces = [i for i in pm.namespaceInfo(":", listOnlyNamespaces=True, recurse=True) if i not in ["UI", "shared"]]
    for ns in namespaces:
        ns_joints = pm.ls(f"{ns}:*", type=pm.nt.Joint)
        root = None
        for i in ns_joints:
            if "root" in i.name():
                root = i
            # TODO add a way to check the highest joint

        if root:
            dup_root = pm.duplicate(root)
            pm.parent(dup_root, world=True)
            dup_joints = dup_root[0].listRelatives(ad=True)
            dup_joints.append(dup_root[0])
            constraints = []
            for jnt in dup_joints:
                for attr in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]:
                    pm.setAttr(jnt.attr(attr), keyable=True)
                pc = pm.parentConstraint(f"{ns}:{jnt.name()}", jnt)
                constraints.append(pc)

            pm.bakeResults(dup_joints, t=(0, 120), simulation=True)  # update to only bake when there's animations

            pm.delete(constraints)

            export_path = pathlib.Path(full_path.parent, "animations", raw_name, f"{ns}.fbx")
            export_path.parent.mkdir(parents=True, exist_ok=True)

            pm.exportSelected(exportPath=export_path)

            pm.delete(dup_root)

    return None
