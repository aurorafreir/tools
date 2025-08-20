"""
Trans Rights are Human Rights :3c
"""

# SYSTEM IMPORTS
from importlib import reload

# STANDARD LIBRARY IMPORTS
import pymel.core as pm
from pymel.core import nt

# LOCAL APPLICATION IMPORTS
from rigging.rig_on_skeleton import rig_on_skeleton as ros
reload(ros)


# EXAMPLE CODE
"""
from rigging.rig_on_skeleton import metahuman
from importlib import reload
reload(metahuman)
metahuman.run()
"""

def run():

    # FIRST SETUP #
    rig = ros.Rig()
    rig.main_grp = "metahuman"
    rig.ensure_setup_is_correct()

    driver = "DRIVER"

    # ROOT CONTROLS #
    global_ctl = ros.CtrlSet(ctl_name="global", ctl_shape="square_with_point", shape_size=25, parent=rig.ctls_grp, colour=ros.white)
    global_ctl.create_ctl()

    global_off_ctl = ros.CtrlSet(ctl_name="global_off", ctl_shape="square", shape_size=20, parent=global_ctl.ctl, colour=ros.white)
    global_off_ctl.create_ctl()

    root_ctl = ros.CtrlSet(ctl_name="root", ctl_shape="box", offset=True, spaceswitch=True, shape_size=2, parent=rig.ctls_grp)
    root_ctl.create_ctl()

    # HIP CONTROLS #
    hip_ctl = ros.CtrlSet(ctl_name="hip", ctl_shape="box", offset=True, spaceswitch=True, shape_size=[40, 10, 30], parent=global_off_ctl.ctl)
    hip_ctl.create_ctl()
    pm.xform(hip_ctl.main_grp, translation=pm.xform("pelvis_drv", translation=True, query=True, worldSpace=True), worldSpace=True)

    # constraints #
    pm.parentConstraint(root_ctl.ctl, "root_drv", maintainOffset=True)
    pm.parentConstraint(hip_ctl.ctl, "pelvis_drv", maintainOffset=True)


    # SHOULDERS
    scap_l = ros.CtrlSet(ctl_name="shoulder_l", ctl_shape="box", offset=True, spaceswitch=True,
                         shape_size=[15, 10, 20], transform_shape=[10,2,0], parent=rig.ctls_grp, colour=ros.left_col,
                         mirror=True) # mirror is unused, but makes for a cleaner end result
    scap_l.create_ctl()
    pm.xform(scap_l.main_grp, t=pm.xform("clavicle_l_drv", t=True, query=True, worldSpace=True), worldSpace=True)
    scap_r = ros.CtrlSet(ctl_name="shoulder_r", ctl_shape="box", offset=True, spaceswitch=True,
                         shape_size=[15, 10, 20], transform_shape=[10,2,0], parent=rig.ctls_grp, colour=ros.right_col,
                         mirror=True)
    scap_r.create_ctl()
    pm.xform(scap_r.main_grp, t=pm.xform("clavicle_l_drv", t=True, query=True, worldSpace=True), worldSpace=True)
    scap_r.do_mirror()

    pm.parentConstraint(scap_l.ctl, "clavicle_l_drv", maintainOffset=True)
    pm.parentConstraint(scap_r.ctl, "clavicle_r_drv", maintainOffset=True)


    # L HAND SETUP
    arm_l = ros.ThreeBoneLimb()
    arm_l.limb_name = "arm_l"
    arm_l.input_joints = ["upperarm_l_drv", "lowerarm_l_drv", "hand_l_drv"]
    arm_l.ikfk_suffix_replace = "_drv"
    arm_l.driver_object = driver
    arm_l.rig_parent = rig.rig_setup_grp
    arm_l.ctl_parent = rig.ctls_grp
    arm_l.rig_upper_obj = scap_l.ctl
    arm_l.create_limb_setup()
    # CONTROLS #
    # driver
    hand_l_drv_ctl = ros.CtrlSet(ctl_name="hand_l_driver", ctl_shape="star", offset=True, spaceswitch=True, shape_size=2, transform_shape=[5,-5,0], parent=arm_l.rig_ctls_grp, colour=ros.driver_col)
    hand_l_drv_ctl.create_ctl()
    pm.xform(hand_l_drv_ctl.main_grp, matrix=pm.xform("hand_l_drv", matrix=True, query=True, worldSpace=True), worldSpace=True)
    # ik
    hand_l_ik_ctl = ros.CtrlSet(ctl_name="hand_l_ik", ctl_shape="box", offset=True, spaceswitch=True, shape_size=7, parent=arm_l.rig_ctls_grp, colour=ros.left_col)
    hand_l_ik_ctl.create_ctl()
    pm.xform(hand_l_ik_ctl.main_grp, matrix=pm.xform("hand_l_drv", matrix=True, query=True, worldSpace=True), worldSpace=True)
    # pv
    hand_l_pv_ctl = ros.CtrlSet(ctl_name="hand_l_pv", ctl_shape="star", offset=True, spaceswitch=True, shape_size=3, parent=arm_l.rig_ctls_grp, colour=ros.left_col)
    hand_l_pv_ctl.create_ctl()
    pm.xform(hand_l_pv_ctl.main_grp, matrix=pm.xform("l_arm_position_loc", matrix=True, query=True, worldSpace=True), worldSpace=True)
    #upperarm_l_fk
    upperarm_l_fk_ctl = ros.CtrlSet(ctl_name="upperarm_l_fk", ctl_shape="box", offset=True, spaceswitch=True, shape_size=7, parent=arm_l.rig_ctls_grp, colour=ros.left_col)
    upperarm_l_fk_ctl.create_ctl()
    pm.xform(upperarm_l_fk_ctl.main_grp, matrix=pm.xform("upperarm_l_drv", matrix=True, query=True, worldSpace=True), worldSpace=True)
    #lowerarm_l_fk
    lowerarm_l_fk_ctl = ros.CtrlSet(ctl_name="lowerarm_l_fk", ctl_shape="box", offset=True, spaceswitch=True, shape_size=7, parent=upperarm_l_fk_ctl.ctl, colour=ros.left_col)
    lowerarm_l_fk_ctl.create_ctl()
    pm.xform(lowerarm_l_fk_ctl.main_grp, matrix=pm.xform("lowerarm_l_drv", matrix=True, query=True, worldSpace=True), worldSpace=True)
    #hand_l_fk
    hand_l_fk_ctl = ros.CtrlSet(ctl_name="hand_l_fk", ctl_shape="box", offset=True, spaceswitch=True, shape_size=5, parent=lowerarm_l_fk_ctl.ctl, colour=ros.left_col)
    hand_l_fk_ctl.create_ctl()
    pm.xform(hand_l_fk_ctl.main_grp, matrix=pm.xform("hand_l_drv", matrix=True, query=True, worldSpace=True), worldSpace=True)

    arm_l.ik_ctl = hand_l_ik_ctl
    arm_l.ik_pv_ctl = hand_l_pv_ctl
    arm_l.fk_ctls = [upperarm_l_fk_ctl, lowerarm_l_fk_ctl, hand_l_fk_ctl]
    arm_l.driver_ctl = hand_l_drv_ctl.ctl
    arm_l.create_three_bone_limb()

    pm.parentConstraint(arm_l.skin_joints[2], hand_l_drv_ctl.main_grp)

    pm.parentConstraint(arm_l.skin_joints[0], "upperarm_l_drv")
    pm.parentConstraint(arm_l.skin_joints[1], "lowerarm_l_drv")
    pm.parentConstraint(arm_l.skin_joints[2], "hand_l_drv")

    pm.parentConstraint(scap_l.ctl, upperarm_l_fk_ctl.main_grp, maintainOffset=True)

    # R HAND SETUP
    arm_r = ros.ThreeBoneLimb()
    arm_r.limb_name = "arm_r"
    arm_r.input_joints = ["upperarm_r_drv", "lowerarm_r_drv", "hand_r_drv"]
    arm_r.ikfk_suffix_replace = "_drv"
    arm_r.driver_object = driver
    arm_r.rig_parent = rig.rig_setup_grp
    arm_r.ctl_parent = rig.ctls_grp
    arm_r.rig_upper_obj = scap_r.ctl
    arm_r.create_limb_setup()
    # CONTROLS #
    # driver
    hand_r_drv_ctl = ros.CtrlSet(ctl_name="hand_r_driver", ctl_shape="star", offset=True, spaceswitch=True, shape_size=2, transform_shape=[-5,5,0], parent=arm_r.rig_ctls_grp, colour=ros.driver_col)
    hand_r_drv_ctl.create_ctl()
    pm.xform(hand_r_drv_ctl.main_grp, matrix=pm.xform("hand_r_drv", matrix=True, query=True, worldSpace=True), worldSpace=True)
    # ik
    hand_r_ik_ctl = ros.CtrlSet(ctl_name="hand_r_ik", ctl_shape="box", offset=True, spaceswitch=True, shape_size=7, parent=arm_r.rig_ctls_grp, colour=ros.right_col)
    hand_r_ik_ctl.create_ctl()
    pm.xform(hand_r_ik_ctl.main_grp, matrix=pm.xform("hand_r_drv", matrix=True, query=True, worldSpace=True), worldSpace=True)
    # pv
    hand_r_pv_ctl = ros.CtrlSet(ctl_name="hand_r_pv", ctl_shape="star", offset=True, spaceswitch=True, shape_size=3, parent=arm_r.rig_ctls_grp, colour=ros.right_col)
    hand_r_pv_ctl.create_ctl()
    pm.xform(hand_r_pv_ctl.main_grp, matrix=pm.xform("r_arm_position_loc", matrix=True, query=True, worldSpace=True), worldSpace=True)
    #upperarm_r_fk
    upperarm_r_fk_ctl = ros.CtrlSet(ctl_name="upperarm_r_fk", ctl_shape="box", offset=True, spaceswitch=True, shape_size=7, parent=arm_r.rig_ctls_grp, colour=ros.right_col)
    upperarm_r_fk_ctl.create_ctl()
    pm.xform(upperarm_r_fk_ctl.main_grp, matrix=pm.xform("upperarm_r_drv", matrix=True, query=True, worldSpace=True), worldSpace=True)
    #lowerarm_r_fk
    lowerarm_r_fk_ctl = ros.CtrlSet(ctl_name="lowerarm_r_fk", ctl_shape="box", offset=True, spaceswitch=True, shape_size=7, parent=upperarm_r_fk_ctl.ctl, colour=ros.right_col)
    lowerarm_r_fk_ctl.create_ctl()
    pm.xform(lowerarm_r_fk_ctl.main_grp, matrix=pm.xform("lowerarm_r_drv", matrix=True, query=True, worldSpace=True), worldSpace=True)
    #hand_r_fk
    hand_r_fk_ctl = ros.CtrlSet(ctl_name="hand_r_fk", ctl_shape="box", offset=True, spaceswitch=True, shape_size=5, parent=lowerarm_r_fk_ctl.ctl, colour=ros.right_col)
    hand_r_fk_ctl.create_ctl()
    pm.xform(hand_r_fk_ctl.main_grp, matrix=pm.xform("hand_r_drv", matrix=True, query=True, worldSpace=True), worldSpace=True)

    arm_r.ik_ctl = hand_r_ik_ctl
    arm_r.ik_pv_ctl = hand_r_pv_ctl
    arm_r.fk_ctls = [upperarm_r_fk_ctl, lowerarm_r_fk_ctl, hand_r_fk_ctl]
    arm_r.driver_ctl = hand_r_drv_ctl.ctl
    arm_r.create_three_bone_limb()

    pm.parentConstraint(arm_r.skin_joints[2], hand_r_drv_ctl.main_grp)

    pm.parentConstraint(arm_r.skin_joints[0], "upperarm_r_drv")
    pm.parentConstraint(arm_r.skin_joints[1], "lowerarm_r_drv")
    pm.parentConstraint(arm_r.skin_joints[2], "hand_r_drv")

    pm.parentConstraint(scap_r.ctl, upperarm_r_fk_ctl.main_grp, maintainOffset=True)

    # Arms attribute locking
    for i in [upperarm_l_fk_ctl.ctl, lowerarm_l_fk_ctl.ctl, hand_l_fk_ctl.ctl,
              upperarm_r_fk_ctl.ctl, lowerarm_r_fk_ctl.ctl, hand_r_fk_ctl.ctl]:
        ros.lock_hide_default_attrs(i, rotate=False)