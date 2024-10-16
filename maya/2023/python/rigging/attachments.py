"""
Trans Rights are Human Rights

A collection of functions to help with creating rigs using driver/proxy/dummy meshes as part of the rig
"""
# SYSTEM IMPORTS

# STANDARD LIBRARY IMPORTS
import pymel.core as pm


# LOCAL APPLICATION IMPORTS


def make_plane_per_drv_joint(selection: list = None):
    """

    :param selection:
    :return:
    """
    if not selection:
        selection = pm.selected(type=pm.nt.Joint)

    for joint in selection:
        new_mesh_name = f"{joint}_drvmesh"
        if pm.objExists(new_mesh_name):
            pm.delete(new_mesh_name)

        planemesh, _ = pm.polyPlane(subdivisionsX=1, subdivisionsY=1)
        pm.xform(planemesh, matrix=joint.worldMatrix.get(), worldSpace=True)
        planemesh.rename(new_mesh_name)

    return None


def make_locator_per_drv_joint(selection: list = None):
    """

    :param selection:
    :return:
    """
    if not selection:
        selection = pm.selected(type=pm.nt.Joint)

    for joint in selection:
        new_loc_name = f"{joint}_drv_loc"
        if pm.objExists(new_loc_name):
            pm.delete(new_loc_name)

        locator = pm.spaceLocator()
        pm.xform(locator, matrix=joint.worldMatrix.get(), worldSpace=True)
        locator.rename(new_loc_name)

    return None


def make_ctlset_per_drv_joint(selection: list = None, mirror_axis: str = "x", joint_target_axis="x"):
    """

    :param selection:
    :param mirror_axis:
    :param joint_target_axis:
    :return:
    """
    if not selection:
        selection = pm.selected(type=pm.nt.Joint)

    drv_ctls = pm.group(name="drv_ctls", empty=True)
    drv_ctls_l = pm.group(name="drv_ctls_l", empty=True)
    drv_ctls_c = pm.group(name="drv_ctls_c", empty=True)
    drv_ctls_r = pm.group(name="drv_ctls_r", empty=True)
    pm.parent(drv_ctls_l, drv_ctls_c, drv_ctls_r, drv_ctls)

    trans_mirror_axis = f"t{mirror_axis}"
    scale_mirror_axis = f"s{mirror_axis}"
    rot_target_axis = f"r{joint_target_axis}"

    for joint in selection:
        new_ctl_name = f"{joint}_ctl"
        new_grp_name = f"{joint}_grp"
        if pm.objExists(new_ctl_name):
            pm.delete(new_ctl_name)

        ctl = pm.curve(d=1, p=[(-0.5, -0.5, .5), (-0.5, .5, .5), (.5, .5, .5), (.5, -0.5, .5), (.5, -0.5, -0.5),
                               (.5, .5, -0.5), (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (.5, -0.5, -0.5), (.5, .5, -0.5),
                               (.5, .5, .5), (-0.5, .5, .5), (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, .5),
                               (.5, -0.5, .5)],
                       name=new_ctl_name)
        grp = pm.group(name=new_grp_name)
        pm.parent(ctl, grp)

        pm.xform(grp, matrix=joint.worldMatrix.get(), worldSpace=True)

        ctl.overrideEnabled.set(1)

        if "_r" in joint.name():
            grp.attr(trans_mirror_axis).set(grp.attr(trans_mirror_axis).get() * -1)
            grp.attr(rot_target_axis).set(grp.attr(rot_target_axis).get() + 180)  # TODO AFOX this needs fixing
            pm.parent(grp, drv_ctls_r)
            ctl.overrideColor.set(14)
        elif "_l" in joint.name():
            pm.parent(grp, drv_ctls_l)
            ctl.overrideColor.set(18)
        else:
            pm.parent(grp, drv_ctls_c)
            ctl.overrideColor.set(17)

    pm.refresh()
    drv_ctls_r.attr(scale_mirror_axis).set(-1)

    for joint in selection:
        loc_name = f"{joint}_drv_loc"
        grp_name = f"{joint}_grp"
        if pm.objExists(loc_name):
            pm.parentConstraint(loc_name, grp_name, maintainOffset=True)

    return None


def constrain_joints_per_ctlset(selection: list = None):
    """

    :param selection:
    :return:
    """

    if not selection:
        selection = pm.selected(type=pm.nt.Joint)

    for joint in selection:
        ctl_name = f"{joint}_ctl"
        pm.parentConstraint(ctl_name, joint, maintainOffset=True)

    return None


def copy_ws_jointorient(in_joint: pm.nt.Joint, out_joint: pm.nt.Joint):
    """

    :param in_joint:
    :param out_joint:
    :return: None
    """

    return None
