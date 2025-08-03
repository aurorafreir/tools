"""
Trans Rights are Human Rights :3c
"""

# SYSTEM IMPORTS
import time

# STANDARD LIBRARY IMPORTS
import pymel.core as pm
from pymel.core import nt

# LOCAL APPLICATION IMPORTS


"""
import pymel.core as pm
from rigging import rig_on_skeleton as ros
from importlib import reload
reload(ros)
rig = ros.Rig()
rig.main_grp = "$Character_Name"
rig.ensure_setup_is_correct()

dummy_attr = ros.Attr(main_object=pm.PyNode("global_grp"), driver_prefix="global", attr_name="ik_controls", nice_name="IK CONTROLS", dummy_attr=True)
dummy_attr.create_attr()

att = ros.Attr(main_object=pm.PyNode("global_grp"), driver_prefix="global", attr_name="fkik", nice_name="FKIK", attr_type="float", float_min=0, float_max=1)
att.create_attr()

"""


blue = (.1, .1, 1)
red = (1, .1, .1)
yellow = (.9, .9, .2)

driver_outliner_yellow = (1, .8, 0)


def get_top_joint(joints:list):
    """

    :return:
    """

    for jnt in joints:
        if not jnt.getParent():
            return jnt

    return None

def lock_hide_default_attrs(obj:pm.nt.Transform,
                            translate=True,
                            rotate=True,
                            scale=True,
                            visibility=True,
                            custom=None,
                            lock=True,
                            hide=True):
    """

    :param obj:
    :param translate:
    :param rotate:
    :param scale:
    :param visibility:
    :param custom:
    :param lock:
    :param hide:
    :return:
    """
    attrs = custom if custom else []
    if not custom:
        if translate:
            attrs.extend(["tx", "ty", "tz"])
        if rotate:
            attrs.extend(["rx", "ry", "rz"])
        if scale:
            attrs.extend(["sx", "sy", "sz"])
        if visibility:
            attrs.extend(["v"])

    for attr in attrs:
        pm.setAttr(f"{obj}.{attr}", lock=lock, keyable=not hide)
    return None

class Attr:
    def __init__(self, main_object:pm.nt.Transform,
                attr_name:"",
                driver_prefix:"",
                nice_name="",
                short_name="",
                long_name="",
                attr_type="",
                dummy_attr = False,

                float_min = None,
                float_max = None,

                proxy_objects=None):

        self.main_object = main_object
        self.attr_name = attr_name
        self.driver_prefix = driver_prefix
        self.nice_name = nice_name
        self.short_name = short_name if short_name else attr_name.lower().replace(" ", "")
        self.long_name = long_name if long_name else attr_name.replace(" ", "_")
        self.attr_type = attr_type if attr_type else "float"

        self.dummy_attr = dummy_attr

        self.float_min = float_min
        self.float_max = float_max

        self.proxy_objects = proxy_objects if proxy_objects else []

    def create_attr(self):
        """

        :return:
        """
        kwargs = {}
        if self.attr_type == "float":
            kwargs = {"attributeType": "float", "minValue": self.float_min, "maxValue": self.float_max}
        if self.dummy_attr:
            kwargs = {"attributeType": "enum", "enumName": "-----:"}

        name_kwargs = {"ln": self.attr_name, "nn": self.nice_name, "sn": self.short_name}

        if not pm.attributeQuery(self.attr_name, node=self.main_object, exists=True):
            pm.addAttr(self.main_object, **name_kwargs, **kwargs)

        # Dummy attributes should be visible but locked
        if self.dummy_attr:
            lock_hide_default_attrs(obj=self.main_object, custom=[self.attr_name], lock=True, hide=False)
        else:  # and normal attributes to be visible and editable
            lock_hide_default_attrs(obj=self.main_object, custom=[self.attr_name], lock=False, hide=False)

        # Create proxy attr on DRIVER node
        sanitized_nice_name = self.nice_name.replace(" ", "_")
        driver_name_kwargs = {"ln": f"{self.driver_prefix}_{sanitized_nice_name}",
                              "nn": f"{self.driver_prefix}_{self.nice_name}",
                              "sn": f"{self.driver_prefix}_{self.short_name}"}
        pm.addAttr("DRIVER", **driver_name_kwargs, proxy=f"{self.main_object}.{self.attr_name}")


class CtrlSet:
    def __init__(self, ctl_name="", offset=False, spaceswitch=False, ctl_shape="", shape_size=1, parent=None):
        self.ctl_name = ctl_name
        self.spaceswitch = spaceswitch
        self.offset = offset
        self.ctl_shape = ctl_shape
        self.shape_size = shape_size
        self.parent = parent

        self.main_grp = None
        self.ctl = None
        self.offset_grp = None
        self.spaceswitch_grp = None

        self.grp_suffix = "grp"
        self.ctl_suffix = "ctl"
        self.off_grp_suffix = "off_grp"
        self.spaceswitch_grp_suffix = "spaceswitch_grp"

        self.box = [
            (-0.5, -0.5, .5),
            (-0.5, .5, .5),
            (.5, .5, .5),
            (.5, -0.5, .5),
            (.5, -0.5, -0.5),
            (.5, .5, -0.5),
            (-0.5, .5, -0.5),
            (-0.5, -0.5, -0.5),
            (.5, -0.5, -0.5),
            (.5, .5, -0.5),
            (.5, .5, .5),
            (-0.5, .5, .5),
            (-0.5, .5, -0.5),
            (-0.5, -0.5, -0.5),
            (-0.5, -0.5, .5),
            (.5, -0.5, .5),
        ]

        self.square_with_point = [
            (-1, 0, 1),
            (-1, 0, -1),
            (1, 0, -1),
            (1, 0, 1),
            (.2, 0, 1),
            (0, 0, 1.2),
            (-.2, 0, 1),
            (-1, 0, 1),

        ]

    def scale_shape_list(self, shape_list):
        """

        :param shape_list:
        :return:
        """
        return [[x * self.shape_size, y * self.shape_size, z * self.shape_size] for x, y, z in shape_list]

    def create_ctl(self):
        """

        :return: None
        """
        obj_order = []

        self.main_grp = pm.group(name=f"{self.ctl_name}_{self.grp_suffix}", empty=True)
        obj_order.append(self.main_grp)

        if self.spaceswitch:
            self.spaceswitch_grp = pm.group(name=f"{self.ctl_name}_{self.spaceswitch_grp_suffix}", empty=True)
            obj_order.append(self.spaceswitch_grp)

        if self.offset:
            self.offset_grp = pm.group(name=f"{self.ctl_name}_{self.off_grp_suffix}", empty=True)
            obj_order.append(self.offset_grp)

        # Control stuff :3c
        ctl_kwargs = {}
        if not self.ctl_shape or self.ctl_shape == "box":
            ctl_kwargs = {"degree": 1, "point": self.scale_shape_list(shape_list=self.box)}
        if self.ctl_shape == "square_with_point":
            ctl_kwargs = {"degree": 1, "point": self.scale_shape_list(shape_list=self.square_with_point)}

        self.ctl = pm.curve(n=f'{self.ctl_name}_{self.ctl_suffix}', **ctl_kwargs)
        obj_order.append(self.ctl)

        for index, obj in enumerate(obj_order):
            if index == 0:
                continue
            pm.parent(obj, obj_order[index-1])

        if self.parent:
            pm.parent(self.main_grp, self.parent)

        pm.select(d=True)

        return None

    def space_switch(self):
        """

        :return:
        """

        return None

class Rig:
    def __init__(self):
        self.main_grp = ""
        self.rig_setup_grp = "rig_setup"
        self.ctls_grp = "ctls"
        self.extracted_ctls_grp = "extracted_ctls"
        self.extracted_control_suffix = "extracted"

        self.driver_main_node = "DRIVER"

        self.name = ""
        self.limbs = []
        self.components = []
        self.drv_skeleton = []
        self.skin_skeleton = []

        self.drv = "drv"
        self.loc = "loc"
        self.floatmath = "fma"
        self.remap = "rmp"

    def ensure_setup_is_correct(self):
        """
        To run at the start of the script, makes sure that any required groups are created nicely.
            Can also be re-run at any point.
        :return: None
        """
        func_start_time = time.time()
        print(f"{time.perf_counter()}: started ensure_setup_is_correct().")
        # Main rig group
        if pm.objExists(self.main_grp):
            self.main_grp = pm.PyNode(self.main_grp)
        else:
            self.main_grp = pm.group(name=self.main_grp, empty=True)

        # Rig setup group
        if pm.objExists(self.rig_setup_grp):
            self.rig_setup_grp = pm.PyNode(self.rig_setup_grp)
        else:
            self.rig_setup_grp = pm.group(name=self.rig_setup_grp, empty=True)
        pm.parent(self.rig_setup_grp, self.main_grp)

        # Ctls group
        if pm.objExists(self.ctls_grp):
            self.ctls_grp = pm.PyNode(self.ctls_grp)
        else:
            self.ctls_grp = pm.group(name=self.ctls_grp, empty=True)
        pm.parent(self.ctls_grp, self.main_grp)

        # Driver node
        if pm.objExists(self.driver_main_node):
            self.driver_main_node = pm.PyNode(self.driver_main_node)
        else:
            self.driver_main_node = pm.createNode(pm.nt.Transform, name=self.driver_main_node)
        pm.parent(self.driver_main_node, self.rig_setup_grp)
        self.driver_main_node.useOutlinerColor.set(1)
        self.driver_main_node.outlinerColor.set(driver_outliner_yellow)

        lock_hide_default_attrs(obj=self.main_grp)
        lock_hide_default_attrs(obj=self.rig_setup_grp)
        lock_hide_default_attrs(obj=self.ctls_grp)
        lock_hide_default_attrs(obj=self.driver_main_node)

        print(f"{time.perf_counter()}: finished ensure_setup_is_correct().")

        return None

    # def duplicate_skin_skel_to_drv(self):
    #     """
    #
    #     :return:
    #     """
    #     # TODO AFOX
    #     top_joint = get_top_joint(joints=self.skin_skeleton)
    #     dup_top_joint = pm.duplicate(top_joint)
    #
    #     return None
    #
    # def connect_drv_to_skin(self):
    #     """
    #
    #     :return:
    #     """
    #     # TODO AFOX
    #     if not self.drv_skeleton or not self.skin_skeleton:
    #         return None
    #
    #     return None

    def extract_ctls(self):
        """
        Takes the currently selected controls and duplicates them to a seperate group to use for rebuilding the rig
        :return: Newly extracted control names as pm.nt.Transforms
        """
        selected = pm.selected(type=pm.nt.Transform)
        extracted_ctls = []
        if not pm.objExists(self.extracted_ctls_grp):
            pm.group(name=self.extracted_ctls_grp, empty=True)
        for ctl in selected:
            extracted_ctl = f"{ctl}_{self.extracted_control_suffix}"
            if pm.objExists(extracted_ctl):
                pm.delete(extracted_ctl)
            dup = pm.duplicate(ctl, name=extracted_ctl)
            for attr in ["t", "r", "s"]:
                for xyz in ["x", "y", "z"]:
                    pm.setAttr(f"{extracted_ctl}.{attr}{xyz}", lock=False, keyable=True)
            pm.delete(dup[0].listRelatives(type=pm.nt.Transform))
            pm.parent(dup, self.extracted_ctls_grp)
            dup[0].t.set(0, 0, 0)
            dup[0].r.set(0, 0, 0)
            extracted_ctls.append(dup[0])

        return extracted_ctls


class Limb:
    def __init__(self):
        self.limb_name = ""
        self.parent = None
        self.limb_rig_setup_grp = ""
        self.rig_ctls_grp = ""
        self.components = None


class ThreeBoneLimb(Limb):
    def __init__(self):
        Limb.__init__(self)
        self.driven_joints = []




class RigCreator:
    def __init__(self, main_grp_name=""):
        super().__init__()
        self.main_grp = main_grp_name
        self.rig_setup_grp = "rig_setup"
        self.ctls_grp = "ctrls"

        self.extracted_controller_grp = "ctls_extracted"
        self.extracted_control_suffix = "ctl_extracted"

        self.grp = "grp"
        self.ctl = "ctl"
        self.loc = "loc"
        self.ctl_grps = []

    def create_nurbs_cube(self, name=""):
        ctl = pm.curve(d=1,
                       p=[(-0.5, -0.5, .5), (-0.5, .5, .5), (.5, .5, .5), (.5, -0.5, .5),
                          (.5, -0.5, -0.5), (.5, .5, -0.5), (-0.5, .5, -0.5), (-0.5, -0.5, -0.5),
                          (.5, -0.5, -0.5), (.5, .5, -0.5), (.5, .5, .5), (-0.5, .5, .5),
                          (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, .5), (.5, -0.5, .5)],
                       n=f'{name}_ctl')
        return ctl


    def base_ctrls_create(self, joint_set=list):
        """

        :param joint_set: list of multiple pm.nt.Joint types to create a cube nurbs curve for
        :return:
        """

        self.ensure_setup_is_correct()

        for jnt in joint_set:
            jnt_parent = jnt.getParent() if jnt.getParent().exists() else None
            parent_ctl = f"{jnt_parent}_{self.grp}"
            parent_grp = f"{jnt_parent}_{self.grp}"
            grp = pm.group(name=f"{jnt}_{self.grp}", empty=True)
            if pm.objExists(f"{jnt}_{self.extracted_control_suffix}"):
                ctl = pm.duplicate(f"{jnt}_{self.extracted_control_suffix}", name=f"{jnt}_{self.grp}")
            else:
                ctl = self.create_nurbs_cube(name=jnt)
                ctl.getShape().overrideRGBColors.set(1)
                if "_l_" in ctl.name():
                    pm.color(ctl.getShape(), rgb=blue)
                elif "_r_" in ctl.name():
                    pm.color(ctl.getShape(), rgb=red)
                else:
                    pm.color(ctl.getShape(), rgb=yellow)

            pm.parent(ctl, grp)
            pm.xform(grp, matrix=pm.xform(jnt, q=True, matrix=True, ws=True), ws=True)
            if pm.objExists(f"{jnt_parent}_{self.grp}"):
                pm.parent(grp, parent_ctl)

        return None



    def fkik_setup(self, input_joints=[pm.nt.Joint, pm.nt.Joint, pm.nt.Joint], slerp_t_obj=pm.nt.Transform, slerp_t_attr=""):
        fk_joint_chain = pm.duplicate(input_joints, parentOnly=True, name="fk_joints_temp")
        ik_joint_chain = pm.duplicate(input_joints, parentOnly=True, name="ik_joints_temp")
        skin_joint_chain = pm.duplicate(input_joints, parentOnly=True, name="skin_joints_temp")

        for index, jnt in enumerate(input_joints):
            fk_jnt = fk_joint_chain[index]
            ik_jnt = ik_joint_chain[index]
            skin_jnt = skin_joint_chain[index]
            fk_jnt.rename(jnt.name().replace("_jnt", "_fk_jnt") if "jnt" in jnt.name() else f"{jnt.name()}_fk_jnt")
            ik_jnt.rename(jnt.name().replace("_jnt", "_ik_jnt") if "jnt" in jnt.name() else f"{jnt.name()}_ik_jnt")
            skin_jnt.rename(jnt.name().replace("_jnt", "_skin_jnt") if "jnt" in jnt.name() else f"{jnt.name()}_skin_jnt")

        for jnt in input_joints:
            fk_jnt = pm.PyNode(jnt.name().replace("_jnt", "_fk_jnt") if "jnt" in jnt.name() else f"{jnt.name()}_fk_jnt")
            ik_jnt = pm.PyNode(jnt.name().replace("_jnt", "_ik_jnt") if "jnt" in jnt.name() else f"{jnt.name()}_ik_jnt")
            skin_jnt = pm.PyNode(jnt.name().replace("_jnt", "_skin_jnt") if "jnt" in jnt.name() else f"{jnt.name()}_skin_jnt")
            self.fkik_quat_setup(name=jnt,
                                 input_obj_a=fk_jnt,
                                 input_obj_b=ik_jnt,
                                 output_obj=skin_jnt,
                                 slerp_t_obj=slerp_t_obj,
                                 slerp_t_attr=slerp_t_attr)

        self.ik_setup(jnt_a=ik_joint_chain[0], jnt_b=ik_joint_chain[1], jnt_c=ik_joint_chain[2])

        return fk_joint_chain, ik_joint_chain, skin_joint_chain

    def ik_setup(self, jnt_a, jnt_b, jnt_c):
        """

        :param jnt_a: IK joint chain top joint
        :param jnt_b: IK joint chain middle joint
        :param jnt_c: IK joint chain bottom joint
        :return:
        """
        loc_centre_jnt = pm.spaceLocator()
        loc_pv = pm.spaceLocator()
        pm.parent(loc_pv, loc_centre_jnt)

        point_const = pm.pointConstraint(jnt_a, jnt_c, loc_centre_jnt, maintainOffset=False)
        pm.delete(point_const)
        aim_const = pm.aimConstraint(jnt_b, loc_centre_jnt, maintainOffset=False)
        pm.delete(aim_const)

        loc_pv.tx.set(20)

        ik_handle = pm.ikHandle(startJoint=jnt_a, endEffector=jnt_c)
        pv_const = pm.poleVectorConstraint(loc_pv, ik_handle[0])
        return loc_centre_jnt, loc_pv, ik_handle, pv_const

    def fkik_quat_setup(self, name="",
                        input_obj_a=pm.nt.Transform,
                        input_obj_b=pm.nt.Transform,
                        output_obj=pm.nt.Transform,
                        slerp_t_obj=pm.nt.Transform,
                        slerp_t_attr=""):
        """
        :param name:
        :param input_obj_a:
        :param input_obj_b:
        :param output_obj:
        :param slerp_t_obj:
        :param slerp_t_attr:
        :return: Created nodes as pm.nt types, euler_to_quat_a, euler_to_quat_b, quat_slerp, quat_to_euler
        """
        if name:
            name = f"{name}_"
        euler_to_quat_a = pm.createNode("eulerToQuat", name=f"{name}eulerToQuat_a")
        euler_to_quat_b = pm.createNode("eulerToQuat", name=f"{name}eulerToQuat_b")
        quat_slerp = pm.createNode("quatSlerp", name=f"{name}quatSlerp")
        quat_to_euler = pm.createNode("quatToEuler", name=f"{name}quatToEuler")

        euler_to_quat_a.outputQuat >> quat_slerp.input1Quat
        euler_to_quat_b.outputQuat >> quat_slerp.input2Quat

        quat_slerp.outputQuat >> quat_to_euler.inputQuat

        if input_obj_a:
            input_obj_a.rotate >> euler_to_quat_a.inputRotate
        if input_obj_b:
            input_obj_b.rotate >> euler_to_quat_b.inputRotate
        if output_obj:
            quat_to_euler.outputRotate >> output_obj.rotate
        if slerp_t_attr:
            slerp_t_obj.attr(slerp_t_attr) >> quat_slerp.inputT

        return euler_to_quat_a, euler_to_quat_b, quat_slerp, quat_to_euler

    def bend_setup(self,
                   name="",
                   upper_joint=pm.nt.Joint,
                   mid_joint=pm.nt.Joint,
                   lower_joint=pm.nt.Joint,
                   upper_mid_twist_joints=list,
                   mid_lower_twist_joints=list):
        """

        :param upper_joint:
        :param name:
        :return:
        """

        self.ensure_setup_is_correct()

        bend_setup_grp = pm.group(name=f"{name}_bend_setup_grp", empty=True)
        pm.parent(bend_setup_grp, self.rig_setup_grp)

        joint_count = 2 + len(upper_mid_twist_joints) + len(mid_lower_twist_joints)
        pm.polyPlane()

        return None

    def mirror_control_shapes(self, controls=[]):

        if not controls:
            controls = pm.selected(type=pm.nt.Transform)

        for control in controls:
            if "_l_" in control.name():
                mirror_control = pm.PyNode(control.name().replace("_l_", "_r_"))
            else:
                mirror_control = pm.PyNode(control.name().replace("_r_", "_l_"))
            dup_control = pm.duplicate(control, rr=True)
            pm.delete(mirror_control.getShape(), shape=True)
            pm.parent(dup_control[0].getShape(), mirror_control, r=True, s=True)
            pm.delete(dup_control)

        return None

    def copy_control_shapes(self, controls=[]):

        if not controls:
            controls = pm.selected(type=pm.nt.Transform)

        dup_control = pm.duplicate(controls[0], rr=True)
        pm.delete(controls[1].getShape(), shape=True)
        pm.parent(dup_control[0].getShape(), controls[1], r=True, s=True)
        pm.delete(dup_control)

        return None
