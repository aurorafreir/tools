"""
Trans Rights are Human Rights

"""
# SYSTEM IMPORTS

# STANDARD LIBRARY IMPORTS
import pymel.core as pm

# LOCAL APPLICATION IMPORTS

# TODO AFOX : Refactor, switch to PyMel


def extract_skeleton() -> None:
    """
    A script to extract skinned skeletons in the scene
    This script is really slow currently, but it does what I want it
        to do so I'm leaving it for now lol

    """
    world_objects = pm.ls(assemblies=True)
    scene_skinned_joints = []
    for sc in pm.ls(type="skinCluster"):
        skinned_joints = [x for x in pm.skinCluster(sc, influence=True, query=True)]
        new_skinned_joints = [i for i in skinned_joints if i not in scene_skinned_joints]
        scene_skinned_joints.extend(new_skinned_joints)

    # Fallback for if this is run in a guides scene without skinned joints
    if not scene_skinned_joints:
        scene_skinned_joints = [i for i in pm.listRelatives("rig", children=True, allDescendents=True, type="joint") if i.visibility.get()]

    for jnt in scene_skinned_joints:
        parent_is_joint = True if type(jnt.getParent()) == pm.nt.Joint else False
        incoming_attrs = jnt.listConnections(plugs=True, source=True)
        for attr in incoming_attrs:
            pm.disconnectAttr(attr)
        if not parent_is_joint:
            print(f"moving {jnt} to top level")
            pm.parent(jnt, world=True)

    return None


def make_offset_joint(joints: list[pm.nt.Joint] = None) -> None:
    """
    Creates a parent joint for each joint in $joints, or each selected joint, so that the selected joint has zeroed
        transforms and joint orients.
    :param joints: List of joints to make offset joints for.
    :return: None
    """
    if not joints:
        if not pm.selected():
            raise Exception("Nothing selected or set in $joints flag")
        joints = pm.selected(type=pm.nt.Joint)
        pm.select(deselect=True)

    for joint in joints:
        off_jnt = pm.joint(name=f"{joint.split('_jnt')[0]}_off_jnt")
        pm.parent(off_jnt, joint)
        pm.xform(off_jnt, translation=(0, 0, 0))
        pm.joint(off_jnt, orientJoint="none", edit=True)
        pm.parent(off_jnt, joint.getParent())
        pm.parent(joint, off_jnt)

        off_jnt.radius.set(joint.radius.get() / 2)

    return None
