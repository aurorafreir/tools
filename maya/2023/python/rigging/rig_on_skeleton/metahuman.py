"""
Trans Rights are Human Rights :3c

This is an example of a rig created for a default Metahuman character
"""

# SYSTEM IMPORTS
from importlib import reload
import time

# STANDARD LIBRARY IMPORTS
import pymel.core as pm

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

    print_errors = True

    # FIRST SETUP #
    rig = ros.Rig()
    rig.main_grp = "metahuman"
    rig.ensure_setup_is_correct()

    driver = "DRIVER"

    # ROOT CONTROLS #
    root_limb = ros.Limb()
    root_limb.limb_name = "root"
    root_limb.rig_parent = rig.rig_setup_grp
    root_limb.ctl_parent = rig.ctls_grp
    global_ctl = ros.CtrlSet(
        ctl_name="global",
        ctl_shape="square_with_point",
        shape_size=25,
        parent=rig.ctls_grp,
        colour=ros.white,
    )
    global_ctl.create_ctl()

    global_off_ctl = ros.CtrlSet(
        ctl_name="global_off",
        ctl_shape="square",
        shape_size=20,
        parent=global_ctl.ctl,
        colour=ros.white,
    )
    global_off_ctl.create_ctl()

    root_ctl = ros.CtrlSet(
        ctl_name="root",
        ctl_shape="box",
        offset=True,
        spaceswitch=True,
        shape_size=2,
        parent=rig.ctls_grp,
    )
    root_ctl.create_ctl()

    # add ctls to root_limb.ctl attribute, and append root_limb to rig.limbs
    root_limb.ctls.extend([global_ctl, global_off_ctl, root_ctl])
    rig.limbs.append(root_limb)

    # HIP CONTROLS #
    hip_limb = ros.Limb()
    hip_limb.limb_name = "hip"
    hip_limb.rig_parent = rig.rig_setup_grp
    hip_limb.ctl_parent = rig.ctls_grp

    hip_ctl = ros.CtrlSet(
        ctl_name="hip",
        ctl_shape="box",
        offset=True,
        spaceswitch=True,
        shape_size=[40, 10, 30],
        parent=global_off_ctl.ctl,
    )
    hip_ctl.create_ctl()
    pm.xform(
        hip_ctl.main_grp,
        translation=pm.xform(
            "pelvis_drv", translation=True, query=True, worldSpace=True
        ),
        worldSpace=True,
    )

    # constraints #
    pm.parentConstraint(root_ctl.ctl, "root_drv", maintainOffset=True)
    pm.parentConstraint(hip_ctl.ctl, "pelvis_drv", maintainOffset=True)

    # add ctls to hip_limb.ctl attribute, and append hip_limb to rig.limbs
    hip_limb.ctls.extend([hip_ctl])
    rig.limbs.append(hip_limb)

    # NECK AND HEAD
    neck_and_head_limb = ros.Limb()
    neck_and_head_limb.limb_name = "neck_and_head"
    neck_and_head_limb.rig_parent = rig.rig_setup_grp
    neck_and_head_limb.ctl_parent = rig.ctls_grp
    neck_01 = ros.CtrlSet(
        ctl_name="neck_01",
        ctl_shape="box",
        offset=True,
        spaceswitch=True,
        shape_size=[3, 12, 12],
        transform_shape=[3, 0, 0],
        parent=rig.ctls_grp,
        colour=ros.centre_col,
    )
    neck_01.create_ctl()
    pm.xform(
        neck_01.main_grp,
        matrix=pm.xform("neck_01_drv", matrix=True, query=True, worldSpace=True),
        worldSpace=True,
    )
    neck_02 = ros.CtrlSet(
        ctl_name="neck_01",
        ctl_shape="box",
        offset=True,
        spaceswitch=True,
        shape_size=[3, 12, 12],
        parent=neck_01.ctl,
        colour=ros.centre_col,
    )
    neck_02.create_ctl()
    pm.xform(
        neck_02.main_grp,
        matrix=pm.xform("neck_02_drv", matrix=True, query=True, worldSpace=True),
        worldSpace=True,
    )

    head = ros.CtrlSet(
        ctl_name="head",
        ctl_shape="box",
        offset=True,
        spaceswitch=True,
        shape_size=[15, 20, 15],
        transform_shape=[3, -2, 0],
        parent=neck_02.ctl,
        colour=ros.centre_col,
    )
    head.create_ctl()
    pm.xform(
        head.main_grp,
        matrix=pm.xform("head_drv", matrix=True, query=True, worldSpace=True),
        worldSpace=True,
    )

    # NECK AND HEAD FINALISING
    pm.parentConstraint(hip_ctl.ctl, neck_01.main_grp, maintainOffset=True)
    pm.parentConstraint(neck_01.ctl, "neck_01_drv")
    pm.parentConstraint(neck_02.ctl, "neck_02_drv")
    pm.parentConstraint(head.ctl, "head_drv")

    ros.lock_hide_default_attrs(neck_01.ctl, rotate=False)
    ros.lock_hide_default_attrs(neck_02.ctl, rotate=False)
    ros.lock_hide_default_attrs(head.ctl, rotate=False)

    # add ctls to neck_and_head_limb.ctl attribute, and append neck_and_head_limb to rig.limbs
    neck_and_head_limb.ctls.extend([neck_01, neck_02, head])
    rig.limbs.append(neck_and_head_limb)

    # SHOULDERS
    shoulder_l = ros.Limb()
    shoulder_l.limb_name = "shoulder_l"
    shoulder_l.rig_parent = rig.rig_setup_grp
    shoulder_l.ctl_parent = rig.ctls_grp
    scap_l = ros.CtrlSet(
        ctl_name="shoulder_l",
        ctl_shape="box",
        offset=True,
        spaceswitch=True,
        shape_size=[15, 10, 20],
        transform_shape=[10, 2, 0],
        parent=rig.ctls_grp,
        colour=ros.left_col,
        mirror=True,
    )  # mirror is unused, but makes for a cleaner end result
    scap_l.create_ctl()
    pm.xform(
        scap_l.main_grp,
        t=pm.xform("clavicle_l_drv", t=True, query=True, worldSpace=True),
        worldSpace=True,
    )

    shoulder_l.ctls.append(scap_l)
    rig.limbs.append(shoulder_l)

    shoulder_r = ros.Limb()
    shoulder_r.limb_name = "shoulder_r"
    shoulder_r.rig_parent = rig.rig_setup_grp
    shoulder_r.ctl_parent = rig.ctls_grp
    scap_r = ros.CtrlSet(
        ctl_name="shoulder_r",
        ctl_shape="box",
        offset=True,
        spaceswitch=True,
        shape_size=[15, 10, 20],
        transform_shape=[10, 2, 0],
        parent=rig.ctls_grp,
        colour=ros.right_col,
        mirror=True,
    )
    scap_r.create_ctl()
    pm.xform(
        scap_r.main_grp,
        t=pm.xform("clavicle_l_drv", t=True, query=True, worldSpace=True),
        worldSpace=True,
    )
    scap_r.do_mirror()

    shoulder_r.ctls.append(scap_r)
    rig.limbs.append(shoulder_r)

    # SHOULDERS FINALIZING
    pm.parentConstraint(scap_l.ctl, "clavicle_l_drv", maintainOffset=True)
    pm.parentConstraint(scap_r.ctl, "clavicle_r_drv", maintainOffset=True)

    ros.lock_hide_default_attrs(scap_l.ctl, rotate=False)
    ros.lock_hide_default_attrs(scap_r.ctl, rotate=False)

    # L HAND SETUP
    pv_l_main_grp, _, pv_l_placer = ros.place_temp_pv_locators(
        name="l_arm",
        upper_joint=pm.PyNode("upperarm_l_drv"),
        middle_joint=pm.PyNode("lowerarm_l_drv"),
        lower_joint=pm.PyNode("hand_l_drv"),
    )

    arm_l = ros.ThreeBoneLimb()
    arm_l.limb_name = "arm_l"
    arm_l.input_joints = ["upperarm_l_drv", "lowerarm_l_drv", "hand_l_drv"]
    arm_l.ikfk_suffix_replace = "_drv"
    arm_l.driver_object = driver
    arm_l.rig_parent = rig.rig_setup_grp
    arm_l.ctl_parent = rig.ctls_grp
    arm_l.rig_upper_obj = scap_l.ctl
    arm_l.verbose = print_errors
    arm_l.create_limb_setup()
    # CONTROLS #
    # driver
    hand_l_drv_ctl = ros.CtrlSet(
        ctl_name="hand_l_driver",
        ctl_shape="star",
        offset=True,
        spaceswitch=True,
        shape_size=2,
        transform_shape=[5, -5, 0],
        parent=arm_l.rig_ctls_grp,
        colour=ros.driver_col,
    )
    hand_l_drv_ctl.create_ctl()
    pm.xform(
        hand_l_drv_ctl.main_grp,
        matrix=pm.xform("hand_l_drv", matrix=True, query=True, worldSpace=True),
        worldSpace=True,
    )
    # ik
    hand_l_ik_ctl = ros.CtrlSet(
        ctl_name="hand_l_ik",
        ctl_shape="box",
        offset=True,
        spaceswitch=True,
        shape_size=7,
        parent=arm_l.rig_ctls_grp,
        colour=ros.left_col,
    )
    hand_l_ik_ctl.create_ctl()
    pm.xform(
        hand_l_ik_ctl.main_grp,
        matrix=pm.xform("hand_l_drv", matrix=True, query=True, worldSpace=True),
        worldSpace=True,
    )
    # pv
    hand_l_pv_ctl = ros.CtrlSet(
        ctl_name="hand_l_pv",
        ctl_shape="star",
        offset=True,
        spaceswitch=True,
        shape_size=3,
        parent=arm_l.rig_ctls_grp,
        colour=ros.left_col,
        mirror=True,
    )
    hand_l_pv_ctl.create_ctl()
    pm.xform(
        hand_l_pv_ctl.main_grp,
        matrix=pm.xform(pv_l_placer, matrix=True, query=True, worldSpace=True),
        worldSpace=True,
    )
    # upperarm_l_fk
    upperarm_l_fk_ctl = ros.CtrlSet(
        ctl_name="upperarm_l_fk",
        ctl_shape="box",
        offset=True,
        spaceswitch=True,
        shape_size=7,
        parent=arm_l.rig_ctls_grp,
        colour=ros.left_col,
    )
    upperarm_l_fk_ctl.create_ctl()
    pm.xform(
        upperarm_l_fk_ctl.main_grp,
        matrix=pm.xform("upperarm_l_drv", matrix=True, query=True, worldSpace=True),
        worldSpace=True,
    )
    # lowerarm_l_fk
    lowerarm_l_fk_ctl = ros.CtrlSet(
        ctl_name="lowerarm_l_fk",
        ctl_shape="box",
        offset=True,
        spaceswitch=True,
        shape_size=7,
        parent=upperarm_l_fk_ctl.ctl,
        colour=ros.left_col,
    )
    lowerarm_l_fk_ctl.create_ctl()
    pm.xform(
        lowerarm_l_fk_ctl.main_grp,
        matrix=pm.xform("lowerarm_l_drv", matrix=True, query=True, worldSpace=True),
        worldSpace=True,
    )
    # hand_l_fk
    hand_l_fk_ctl = ros.CtrlSet(
        ctl_name="hand_l_fk",
        ctl_shape="box",
        offset=True,
        spaceswitch=True,
        shape_size=5,
        parent=lowerarm_l_fk_ctl.ctl,
        colour=ros.left_col,
    )
    hand_l_fk_ctl.create_ctl()
    pm.xform(
        hand_l_fk_ctl.main_grp,
        matrix=pm.xform("hand_l_drv", matrix=True, query=True, worldSpace=True),
        worldSpace=True,
    )

    arm_l.pole_vec_obj = hand_l_pv_ctl.ctl
    arm_l.ik_ctl = hand_l_ik_ctl
    arm_l.ik_pv_ctl = hand_l_pv_ctl
    arm_l.fk_ctls = [upperarm_l_fk_ctl, lowerarm_l_fk_ctl, hand_l_fk_ctl]
    arm_l.driver_ctl = hand_l_drv_ctl.ctl
    arm_l.create_three_bone_limb()

    pm.parentConstraint(arm_l.skin_joints[2], hand_l_drv_ctl.main_grp)

    pm.parentConstraint(arm_l.pole_pin_upper_jnt, "upperarm_l_drv")
    pm.parentConstraint(arm_l.pole_pin_lower_jnt, "lowerarm_l_drv")
    pm.parentConstraint(arm_l.skin_joints[2], "hand_l_drv")

    pm.parentConstraint(scap_l.ctl, upperarm_l_fk_ctl.main_grp, maintainOffset=True)

    # l arm twist
    ros.delete_if_exists("upperarm_twist_01_l_orientConstraint1_drv")
    ros.delete_if_exists("upperarm_twist_02_l_orientConstraint1_drv")

    upperarm_twist_01_oc = pm.orientConstraint(
        arm_l.noroll_upper_joint,
        arm_l.pole_pin_lower_jnt,
        "upperarm_twist_01_l_drv",
        skip=["y", "z"],
        maintainOffset=True,
    )
    upperarm_twist_01_oc.interpType.set(2)
    upperarm_twist_01_oc.attr(f"{arm_l.noroll_upper_joint}W0").set(0.8)
    upperarm_twist_01_oc.attr(f"{arm_l.pole_pin_lower_jnt}W1").set(0.2)
    upperarm_twist_02_oc = pm.orientConstraint(
        arm_l.noroll_upper_joint,
        arm_l.pole_pin_lower_jnt,
        "upperarm_twist_02_l_drv",
        skip=["y", "z"],
        maintainOffset=True,
    )
    upperarm_twist_02_oc.interpType.set(2)
    upperarm_twist_02_oc.attr(f"{arm_l.noroll_upper_joint}W0").set(0.4)
    upperarm_twist_02_oc.attr(f"{arm_l.pole_pin_lower_jnt}W1").set(0.6)

    shoulder_l_orient_const = pm.orientConstraint(
        arm_l.dup_parent_joint,
        arm_l.pole_pin_upper_jnt,
        pm.PyNode("upperarm_correctiveRootCor_l_drv"),
        maintainOffset=True,
    )
    shoulder_l_orient_const.interpType.set(2)

    # add ctls to arm_l.ctl attribute, and append arm_l to rig.limbs
    arm_l.ctls.extend(
        [
            hand_l_drv_ctl,
            hand_l_ik_ctl,
            hand_l_pv_ctl,
            upperarm_l_fk_ctl,
            lowerarm_l_fk_ctl,
            hand_l_fk_ctl,
        ]
    )
    rig.limbs.append(arm_l)

    # R HAND SETUP
    pv_r_main_grp, _, pv_r_placer = ros.place_temp_pv_locators(
        name="r_arm",
        upper_joint=pm.PyNode("upperarm_l_drv"),
        middle_joint=pm.PyNode("lowerarm_l_drv"),
        lower_joint=pm.PyNode("hand_l_drv"),
    )

    arm_r = ros.ThreeBoneLimb()
    arm_r.limb_name = "arm_r"
    arm_r.input_joints = ["upperarm_r_drv", "lowerarm_r_drv", "hand_r_drv"]
    arm_r.ikfk_suffix_replace = "_drv"
    arm_r.driver_object = driver
    arm_r.rig_parent = rig.rig_setup_grp
    arm_r.ctl_parent = rig.ctls_grp
    arm_r.rig_upper_obj = scap_r.ctl
    arm_r.verbose = print_errors
    arm_r.create_limb_setup()
    # CONTROLS #
    # driver
    hand_r_drv_ctl = ros.CtrlSet(
        ctl_name="hand_r_driver",
        ctl_shape="star",
        offset=True,
        spaceswitch=True,
        shape_size=2,
        transform_shape=[-5, 5, 0],
        parent=arm_r.rig_ctls_grp,
        colour=ros.driver_col,
    )
    hand_r_drv_ctl.create_ctl()
    pm.xform(
        hand_r_drv_ctl.main_grp,
        matrix=pm.xform("hand_r_drv", matrix=True, query=True, worldSpace=True),
        worldSpace=True,
    )
    # ik
    hand_r_ik_ctl = ros.CtrlSet(
        ctl_name="hand_r_ik",
        ctl_shape="box",
        offset=True,
        spaceswitch=True,
        shape_size=7,
        parent=arm_r.rig_ctls_grp,
        colour=ros.right_col,
        mirror=True,
    )
    hand_r_ik_ctl.create_ctl()
    pm.xform(
        hand_r_ik_ctl.main_grp,
        matrix=pm.xform("hand_l_drv", matrix=True, query=True, worldSpace=True),
        worldSpace=True,
    )
    # pv
    hand_r_pv_ctl = ros.CtrlSet(
        ctl_name="hand_r_pv",
        ctl_shape="star",
        offset=True,
        spaceswitch=True,
        shape_size=3,
        parent=arm_r.rig_ctls_grp,
        colour=ros.right_col,
        mirror=True,
    )
    hand_r_pv_ctl.create_ctl()
    pm.xform(
        hand_r_pv_ctl.main_grp,
        matrix=pm.xform(pv_r_placer, matrix=True, query=True, worldSpace=True),
        worldSpace=True,
    )
    # upperarm_r_fk
    upperarm_r_fk_ctl = ros.CtrlSet(
        ctl_name="upperarm_r_fk",
        ctl_shape="box",
        offset=True,
        spaceswitch=True,
        shape_size=7,
        parent=arm_r.rig_ctls_grp,
        colour=ros.right_col,
        mirror=True,
    )
    upperarm_r_fk_ctl.create_ctl()
    pm.xform(
        upperarm_r_fk_ctl.main_grp,
        matrix=pm.xform("upperarm_l_drv", matrix=True, query=True, worldSpace=True),
        worldSpace=True,
    )
    # lowerarm_r_fk
    lowerarm_r_fk_ctl = ros.CtrlSet(
        ctl_name="lowerarm_r_fk",
        ctl_shape="box",
        offset=True,
        spaceswitch=True,
        shape_size=7,
        parent=upperarm_r_fk_ctl.ctl,
        colour=ros.right_col,
    )
    lowerarm_r_fk_ctl.create_ctl()
    pm.xform(
        lowerarm_r_fk_ctl.main_grp,
        matrix=pm.xform("lowerarm_l_drv", matrix=True, query=True, worldSpace=True),
        worldSpace=True,
    )
    # hand_r_fk
    hand_r_fk_ctl = ros.CtrlSet(
        ctl_name="hand_r_fk",
        ctl_shape="box",
        offset=True,
        spaceswitch=True,
        shape_size=5,
        parent=lowerarm_r_fk_ctl.ctl,
        colour=ros.right_col,
    )
    hand_r_fk_ctl.create_ctl()
    pm.xform(
        hand_r_fk_ctl.main_grp,
        matrix=pm.xform("hand_l_drv", matrix=True, query=True, worldSpace=True),
        worldSpace=True,
    )
    # mirror stuff :3
    hand_r_ik_ctl.do_mirror()
    hand_r_pv_ctl.do_mirror()
    upperarm_r_fk_ctl.do_mirror()

    arm_r.pole_vec_obj = hand_r_pv_ctl.ctl
    arm_r.ik_ctl = hand_r_ik_ctl
    arm_r.ik_pv_ctl = hand_r_pv_ctl
    arm_r.fk_ctls = [upperarm_r_fk_ctl, lowerarm_r_fk_ctl, hand_r_fk_ctl]
    arm_r.driver_ctl = hand_r_drv_ctl.ctl
    arm_r.mirror = True
    arm_r.create_three_bone_limb()

    pm.parentConstraint(arm_r.skin_joints[2], hand_r_drv_ctl.main_grp)

    pm.parentConstraint(arm_r.pole_pin_upper_jnt, "upperarm_r_drv")
    pm.parentConstraint(arm_r.pole_pin_lower_jnt, "lowerarm_r_drv")
    pm.parentConstraint(arm_r.skin_joints[2], "hand_r_drv")

    pm.parentConstraint(scap_r.ctl, upperarm_r_fk_ctl.main_grp, maintainOffset=True)

    # r arm twist
    ros.delete_if_exists("upperarm_twist_01_r_orientConstraint1_drv")
    ros.delete_if_exists("upperarm_twist_02_r_orientConstraint1_drv")

    upperarm_twist_01_oc = pm.orientConstraint(
        arm_r.noroll_upper_joint,
        arm_r.pole_pin_lower_jnt,
        "upperarm_twist_01_r_drv",
        skip=["y", "z"],
        maintainOffset=True,
    )
    upperarm_twist_01_oc.interpType.set(2)
    upperarm_twist_01_oc.attr(f"{arm_r.noroll_upper_joint}W0").set(0.8)
    upperarm_twist_01_oc.attr(f"{arm_r.pole_pin_lower_jnt}W1").set(0.2)
    upperarm_twist_02_oc = pm.orientConstraint(
        arm_r.noroll_upper_joint,
        arm_r.pole_pin_lower_jnt,
        "upperarm_twist_02_r_drv",
        skip=["y", "z"],
        maintainOffset=True,
    )
    upperarm_twist_02_oc.interpType.set(2)
    upperarm_twist_02_oc.attr(f"{arm_r.noroll_upper_joint}W0").set(0.4)
    upperarm_twist_02_oc.attr(f"{arm_r.pole_pin_lower_jnt}W1").set(0.6)

    shoulder_r_orient_const = pm.orientConstraint(
        arm_r.dup_parent_joint,
        arm_r.pole_pin_upper_jnt,
        pm.PyNode("upperarm_correctiveRootCor_r_drv"),
        maintainOffset=True,
    )
    shoulder_r_orient_const.interpType.set(2)

    # add ctls to arm_r.ctl attribute, and append arm_r to rig.limbs
    arm_r.ctls.extend(
        [
            hand_r_drv_ctl,
            hand_r_ik_ctl,
            hand_r_pv_ctl,
            upperarm_r_fk_ctl,
            lowerarm_r_fk_ctl,
            hand_r_fk_ctl,
        ]
    )
    rig.limbs.append(arm_r)

    # Arms attribute locking
    for i in [
        upperarm_l_fk_ctl.ctl,
        lowerarm_l_fk_ctl.ctl,
        hand_l_fk_ctl.ctl,
        upperarm_r_fk_ctl.ctl,
        lowerarm_r_fk_ctl.ctl,
        hand_r_fk_ctl.ctl,
    ]:
        ros.lock_hide_default_attrs(i, rotate=False)
    for i in [hand_l_pv_ctl.ctl, hand_r_pv_ctl.ctl]:
        ros.lock_hide_default_attrs(i, rotate=False, translate=False)
    for i in [hand_l_ik_ctl.ctl, hand_r_ik_ctl.ctl]:
        ros.lock_hide_default_attrs(i, rotate=False, translate=False)
    for i in [hand_l_drv_ctl.ctl, hand_r_drv_ctl.ctl]:
        ros.lock_hide_default_attrs(i)

    pm.parentConstraint(hip_ctl.ctl, scap_l.main_grp, maintainOffset=True)
    pm.parentConstraint(hip_ctl.ctl, scap_r.main_grp, maintainOffset=True)

    # FINALISING
    pm.delete(pv_l_main_grp, pv_r_main_grp)

    print(f"{time.perf_counter():.2f}: Finished building '{rig.main_grp}'")

    print(f"limbs: {[i.limb_name for i in rig.limbs]}")
    print(f"limb ctls: {[[y.ctl_name for y in i.ctls] for i in rig.limbs]}")

    return rig
