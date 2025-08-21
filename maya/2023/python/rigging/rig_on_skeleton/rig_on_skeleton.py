"""
Trans Rights are Human Rights :3c
"""

# SYSTEM IMPORTS
import time

# STANDARD LIBRARY IMPORTS
import pymel.core as pm
from pymel.core import nt

# LOCAL APPLICATION IMPORTS


blue = (.05, .05, 1)
red = (1, .1, .1)
yellow = (.9, .9, .2)
white = (1, 1, 1)

driver_outliner_yellow = (1, .8, 0)


right_col = red
left_col = blue
centre_col = yellow
driver_col = white


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

def set_up_space_switching(driver_obj:pm.nt.Transform, attr:str, driven_obj:pm.nt.Transform, space_objects:list):
    """

    :param driver_obj:
    :param attr:
    :param driven_obj:
    :param space_objects:
    :return:
    """

    # TODO AFOX

    return None

def fkik_quat_setup(name="",
                        input_obj_a=pm.nt.Transform,
                        input_obj_b=pm.nt.Transform,
                        output_obj=pm.nt.Transform,
                        slerp_t_obj=pm.nt.Transform,
                        slerp_t_attr_str="",
                        slerp_t_attr=None,
                        slerp_t_attr_flip=False,
                    ):
        """
        :param name:
        :param input_obj_a:
        :param input_obj_b:
        :param output_obj:
        :param slerp_t_obj:
        :param slerp_t_attr_str:
        :param slerp_t_attr:
        :return: Created nodes as pm.nt types, euler_to_quat_a, euler_to_quat_b, quat_slerp, quat_to_euler
        """
        # TODO AFOX add in reverse node as an option
        if slerp_t_attr_flip:
            flipper_node = pm.createNode("floatMath")
        if name:
            name = f"{name}" if name.endswith("_") else f"{name}_"
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
        if slerp_t_attr_str:
            slerp_t_obj.attr(slerp_t_attr_str) >> quat_slerp.inputT
        elif slerp_t_attr:
            slerp_t_attr >> quat_slerp.inputT

        return euler_to_quat_a, euler_to_quat_b, quat_slerp, quat_to_euler

class Attr:
    def __init__(self, main_object:pm.nt.Transform,
                attr_name:"",
                driver_prefix:"",
                nice_name="",
                short_name="",
                long_name="",
                attr_type="float",
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
        self.attr_type = attr_type

        self.dummy_attr = dummy_attr

        self.float_min = float_min
        self.float_max = float_max

        self.proxy_objects = proxy_objects if proxy_objects else []

        self.attr = None
        self.driver_attr = None
        self.driver_attr_str = None
        self.sanitized_nice_name = None

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

        # if not pm.attributeQuery(self.attr_name, node=self.main_object, exists=True):
        self.attr = pm.addAttr(self.main_object, **name_kwargs, **kwargs)

        # Dummy attributes should be visible but locked
        if self.dummy_attr:
            lock_hide_default_attrs(obj=self.main_object, custom=[self.attr_name], lock=True, hide=False)
        else:  # and normal attributes to be visible and editable
            lock_hide_default_attrs(obj=self.main_object, custom=[self.attr_name], lock=False, hide=False)

        # Create proxy attr on DRIVER node
        self.sanitized_nice_name = self.nice_name.replace(" ", "_")
        self.driver_attr_str = f"{self.driver_prefix}_{self.sanitized_nice_name}"
        driver_name_kwargs = {"ln": self.driver_attr_str,
                              "nn": f"{self.driver_prefix}_{self.nice_name}",
                              "sn": f"{self.driver_prefix}_{self.short_name}"}
        self.driver_attr = pm.addAttr("DRIVER", **driver_name_kwargs, proxy=f"{self.main_object}.{self.attr_name}")

        return None

class CtrlSet:
    def __init__(self,
                 ctl_name="",
                 offset=False,
                 spaceswitch=False,
                 mirror=False,
                 ctl_shape="",
                 shape_size:int or list=1,
                 transform_shape=[0, 0, 0],
                 colour=None,
                 parent=None,
                 spaces=None):
        self.ctl_name = ctl_name
        self.offset = offset
        self.spaceswitch = spaceswitch
        self.mirror = mirror
        self.ctl_shape = ctl_shape
        self.shape_size = shape_size if isinstance(shape_size, list) else [shape_size, shape_size, shape_size]
        self.transform_shape = transform_shape
        self.colour = colour
        self.parent = parent
        self.spaces:list = spaces

        self.main_grp = None
        self.ctl = None
        self.offset_grp = None
        self.spaceswitch_grp = None
        self.mirror_grp = None

        self.grp_suffix = "grp"
        self.ctl_suffix = "ctl"
        self.off_grp_suffix = "off_grp"
        self.spaceswitch_grp_suffix = "spaceswitch_grp"
        self.mirror_grp_suffix = "mirror_grp"

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
        self.square = [
            [1, 0, 1],
            [1, 0, -1],
            [-1, 0, -1],
            [-1, 0, 1],
            [1, 0, 1]
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
        self.star = [
            (.2, .2, 0),
            (0, 1, 0),
            (-.2, .2, 0),
            (-1, 0, 0),
            (-.2, -.2, 0),
            (0, -1, 0),
            (.2, -.2, 0),
            (1, 0, 0),
        ]

    def transform_shape_list(self, shape_list):
        """
        # TODO AFOX description
        :param shape_list: list of XYZ arrays to make a nurbs curve shape
        :return: list of modified XYZ arrays
        """
        return [[x * self.shape_size[0] + self.transform_shape[0],
                 y * self.shape_size[1] + self.transform_shape[1],
                 z * self.shape_size[2] + self.transform_shape[2]] for x, y, z in shape_list]

    def create_ctl(self):
        """
        # TODO AFOX description
        :return: None
        """
        obj_order = []

        if self.mirror:
            self.mirror_grp = pm.group(name=f"{self.ctl_name}_{self.mirror_grp_suffix}", empty=True)
            obj_order.append(self.mirror_grp)

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
            ctl_kwargs = {"degree": 1, "point": self.transform_shape_list(shape_list=self.box)}
        if self.ctl_shape == "square_with_point":
            ctl_kwargs = {"degree": 1, "point": self.transform_shape_list(shape_list=self.square_with_point)}
        if self.ctl_shape == "square":
            ctl_kwargs = {"degree": 1, "point": self.transform_shape_list(shape_list=self.square)}
        if self.ctl_shape == "star":
            ctl_kwargs = {"degree": 3, "point": self.transform_shape_list(shape_list=self.star)}

        self.ctl = pm.curve(n=f'{self.ctl_name}_{self.ctl_suffix}', **ctl_kwargs)
        if self.ctl_shape == "star":
            pm.closeCurve(self.ctl, preserveShape=0, replaceOriginal=True)
        obj_order.append(self.ctl)

        if self.colour:
            self.ctl.overrideEnabled.set(1)
            self.ctl.overrideRGBColors.set(1)
            self.ctl.overrideColorRGB.set(self.colour)

        for index, obj in enumerate(obj_order):
            if index == 0:
                continue
            pm.parent(obj, obj_order[index-1])

        if self.parent:
            pm.parent(self.main_grp if not self.mirror_grp else self.mirror_grp, self.parent)

        pm.select(d=True)

        print(f"{time.perf_counter()}: Created controller set {self.ctl_name} with objects {obj_order}")

        return None

    def set_up_space_switch(self):
        """
        # TODO AFOX description
        :return:
        """

        return None

    def do_mirror(self):
        """

        :return:
        """
        if not self.mirror:
            print(f"No mirror object for {self.ctl_name}, skipping :)")
        else:
            self.mirror_grp.sx.set(-1)

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

        # lock_hide_default_attrs(obj=self.main_grp)
        # lock_hide_default_attrs(obj=self.rig_setup_grp)
        # lock_hide_default_attrs(obj=self.ctls_grp)
        # lock_hide_default_attrs(obj=self.driver_main_node)

        print(f"{time.perf_counter()}: finished ensure_setup_is_correct().")

        return None

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
        self.rig_parent:pm.nt.Transform = None
        self.ctl_parent:pm.nt.Transform = None

        self.rig_setup_grp_name = None
        self.rig_ctls_grp_name = None

        self.rig_setup_grp = None
        self.rig_ctls_grp = None
        self.rig_upper_obj = None

        self.driver_object = None

        self.mirror = False

    def create_limb_setup(self):
        """

        :return:
        """
        if not self.rig_setup_grp:
            self.rig_setup_grp = f"{self.limb_name}_rig_setup"
        if pm.objExists(self.rig_setup_grp):
            self.rig_setup_grp = pm.PyNode(self.rig_setup_grp)
        else:
            self.rig_setup_grp = pm.group(name=self.rig_setup_grp, empty=True)

        pm.parent(self.rig_setup_grp, self.rig_parent)

        if not self.rig_ctls_grp:
            self.rig_ctls_grp = f"{self.limb_name}_ctls"
        if pm.objExists(self.rig_ctls_grp):
            self.rig_ctls_grp = pm.PyNode(self.rig_ctls_grp)
        else:
            self.rig_ctls_grp = pm.group(name=self.rig_ctls_grp, empty=True)

        pm.parent(self.rig_ctls_grp, self.ctl_parent)

        return None


class ThreeBoneLimb(Limb):
    def __init__(self,
                 input_joints:list=None,
                 # fkik:bool=True,  # assuming fkik is true tbh, who doesn't want fkik at the least :3
                 stretch:bool=True,
                 stretch_modifiers:bool=True,
                 pole_lock:bool=True,
                 pole_vec_obj:pm.nt.Transform=None,
                 bend_setup:bool=True,
                 ikfk_suffix_replace:str="_drv",
                 ik_ctl:pm.nt.Transform=None,
                 ik_pv_ctl:pm.nt.Transform=None,
                 fk_ctls:list=None,
                 driver_ctl:pm.nt.Transform=None,
                 elbow_ctl:pm.nt.Transform=None,):
        Limb.__init__(self)

        # TODO AFOX pole vec pin joints
        # TODO AFOX noroll upper joint

        self.input_joints = input_joints
        # self.fkik = fkik
        self.stretch = stretch
        self.stretch_modifiers = stretch_modifiers
        self.pole_lock = pole_lock
        self.pole_vec_obj = pole_vec_obj
        self.bend_setup = bend_setup
        self.ikfk_suffix_replace = ikfk_suffix_replace
        self.ik_ctl = ik_ctl
        self.ik_pv_ctl = ik_pv_ctl
        self.fk_ctls = fk_ctls
        self.driver_ctl = driver_ctl
        self.elbow_ctl = elbow_ctl

        self.ik_joints = None
        self.fk_joints = None
        self.skin_joints = None

        self.pole_pin_upper_jnt = None
        self.pole_pin_lower_jnt = None

    def create_three_bone_limb(self):
        """
        Creates a basic three joint limb, with FKIK, and options for stretch
        :return: None
        """

        self.rig_upper_obj = self.rig_upper_obj if self.rig_upper_obj else self.ctl_parent

        self.fk_joints = pm.duplicate(self.input_joints, parentOnly=True)
        for i in self.fk_joints:
            i.rename(i.replace(self.ikfk_suffix_replace, "_fk"))
        self.fk_joints[0].rename(self.fk_joints[0][:-1])
        self.ik_joints = pm.duplicate(self.input_joints, parentOnly=True)
        for i in self.ik_joints:
            i.rename(i.replace(self.ikfk_suffix_replace, "_ik"))
        self.ik_joints[0].rename(self.ik_joints[0][:-1])
        self.skin_joints = pm.duplicate(self.input_joints, parentOnly=True)
        for i in self.skin_joints:
            i.rename(i.replace(self.ikfk_suffix_replace, "_skin"))
        self.skin_joints[0].rename(self.skin_joints[0][:-1])

        # No Roll upper joint. Orient constrained to upper skin joint on Y and Z.
        noroll_upper_joint = pm.duplicate(self.input_joints[0], parentOnly=True)[0]
        noroll_upper_joint.rename(noroll_upper_joint.replace(self.ikfk_suffix_replace, "_noroll"))
        noroll_upper_joint.rename(noroll_upper_joint[:-1])
        pm.orientConstraint(self.skin_joints[0], noroll_upper_joint, skip="x")

        # Parenting to the rig's group
        pm.parent(self.fk_joints[0], self.rig_setup_grp)
        pm.parent(self.ik_joints[0], self.rig_setup_grp)
        pm.parent(self.skin_joints[0], self.rig_setup_grp)
        pm.parent(noroll_upper_joint, self.rig_setup_grp)

        # IK setup and constraint to ik control
        ik_handle = pm.ikHandle(name=f"{self.limb_name}_ikh", startJoint=self.ik_joints[0], endEffector=self.ik_joints[2])
        pm.parent(ik_handle[0], self.rig_setup_grp)
        pm.parentConstraint(self.ik_ctl.ctl, ik_handle[0], maintainOffset=False)
        pm.poleVectorConstraint(self.ik_pv_ctl.ctl, ik_handle[0])

        pm.orientConstraint(self.ik_ctl.ctl, self.ik_joints[2], maintainOffset=False)

        # upper object constraints
        pm.parentConstraint(self.rig_upper_obj, self.ik_joints[0], maintainOffset=True)
        ik_fk_skin_point_const = pm.pointConstraint(self.fk_joints[0], self.ik_joints[0], self.skin_joints[0])
        pm.parentConstraint(self.rig_upper_obj, noroll_upper_joint, skipRotate=["x", "y", "z"], maintainOffset=True)

        # FK control constraints
        pm.parentConstraint(self.fk_ctls[0].ctl, self.fk_joints[0], maintainOffset=False)
        pm.parentConstraint(self.fk_ctls[1].ctl, self.fk_joints[1], maintainOffset=False)
        pm.parentConstraint(self.fk_ctls[2].ctl, self.fk_joints[2], maintainOffset=False)

        # Attribute creation
        limb_ik_controls_attr = Attr(main_object=self.driver_ctl,
                                     attr_name="ik_controls",
                                     nice_name="IK CONTROLS",
                                     dummy_attr=True,
                                     driver_prefix=self.limb_name)
        limb_fkik = Attr(main_object=self.driver_ctl,
                         attr_name="fkik",
                         nice_name="FKIK",
                         driver_prefix=self.limb_name,
                         float_min=0,
                         float_max=1,)
        limb_fkik.create_attr()

        fkik_rev = pm.createNode("floatMath", name=f"{self.limb_name}_fkik_rev_floatmath")
        fkik_rev.operation.set(1)
        pm.connectAttr(f"{self.driver_object}.{limb_fkik.driver_attr_str}", self.ik_ctl.main_grp.v)
        pm.connectAttr(f"{self.driver_object}.{limb_fkik.driver_attr_str}", fkik_rev.floatB)
        pm.connectAttr(fkik_rev.outFloat, self.fk_ctls[0].main_grp.v)

        # pm.connectAttr(f"{self.driver_object}.{limb_fkik.driver_attr_str}", f"{ik_fk_skin_point_const}.{self.fk_joints[0]}W0")
        # pm.connectAttr(fkik_rev.outFloat, f"{ik_fk_skin_point_const}.{self.ik_joints[0]}W1")


        fkik_quat_setup(name=self.limb_name,
                        input_obj_a=self.ik_joints[0],
                        input_obj_b=self.fk_joints[0],
                        output_obj=self.skin_joints[0],
                        slerp_t_obj=fkik_rev,
                        slerp_t_attr_str="outFloat")
        fkik_quat_setup(name=self.limb_name,
                        input_obj_a=self.ik_joints[1],
                        input_obj_b=self.fk_joints[1],
                        output_obj=self.skin_joints[1],
                        slerp_t_obj=fkik_rev,
                        slerp_t_attr_str="outFloat")
        fkik_quat_setup(name=self.limb_name,
                        input_obj_a=self.ik_joints[2],
                        input_obj_b=self.fk_joints[2],
                        output_obj=self.skin_joints[2],
                        slerp_t_obj=fkik_rev,
                        slerp_t_attr_str="outFloat")

        # Attribute linking
        # limb_fkik.driver_attr >>

        if self.stretch:
            stretch_grp = pm.group(name=f"{self.limb_name}_stretch_grp", empty=True)
            pm.parent(stretch_grp, self.rig_setup_grp)

            length_crv = pm.curve(name=f"{self.limb_name}_stretch_len_crv", p=[[1, 0, 0], [-1, 0, 0]], d=1)
            cluster_a = pm.cluster(length_crv.cv[0], name=f"{self.limb_name}_top_cluster")
            cluster_b = pm.cluster(length_crv.cv[1], name=f"{self.limb_name}_bottom_cluster")
            pm.parent(length_crv, stretch_grp)
            pm.parent(cluster_a, stretch_grp)
            pm.parent(cluster_b, stretch_grp)

            pm.parentConstraint(noroll_upper_joint, cluster_a, maintainOffset=False)
            pm.parentConstraint(self.ik_ctl.ctl, cluster_b, maintainOffset=False)

            arclength = pm.arclen(length_crv, ch=True)

            # SETTING CONSTANTS FOR UPPER > LOWER TX LENGTH AND LOWER > HAND/FOOT TX LENGTH
            upper_to_lower_const = pm.createNode("floatConstant", name=f"{self.limb_name.upper()}_UL_CONST")
            upper_to_lower_const.inFloat.set(self.ik_joints[1].tx.get())
            lower_to_hand_const  = pm.createNode("floatConstant", name=f"{self.limb_name.upper()}_LH_CONST")
            lower_to_hand_const.inFloat.set(self.ik_joints[2].tx.get())

            if self.stretch_modifiers:
                pass

        if self.pole_lock:
            # if not self.elbow_ctl:
            #     raise Exception(f"No elbow ctl specified for {self.limb_name}")
            # if not self.pole_vec_ctl:
            #     raise Exception(f"No pole vector control specified for {self.limb_name}")

            # Attribute creation
            limb_pole_lock = Attr(main_object=self.driver_ctl,
                             attr_name="pole_lock", nice_name="Pole Vec Lock",
                             driver_prefix=f"{self.limb_name}",
                             float_min=0, float_max=1, )
            limb_pole_lock.create_attr()

            self.pole_pin_upper_jnt = pm.duplicate(self.input_joints[0], parentOnly=True)[0]
            self.pole_pin_upper_jnt.rename(self.pole_pin_upper_jnt.name()[:-1].replace(self.ikfk_suffix_replace, "_pin"))
            pm.parent(self.pole_pin_upper_jnt, self.rig_setup_grp)
            self.pole_pin_lower_jnt = pm.duplicate(self.input_joints[1], parentOnly=True)[0]
            self.pole_pin_lower_jnt.rename(self.pole_pin_lower_jnt.name()[:-1].replace(self.ikfk_suffix_replace, "_pin"))
            pm.parent(self.pole_pin_lower_jnt, self.rig_setup_grp)

            upper_pin_point_const = pm.pointConstraint(self.ik_joints[0],
                                                       self.pole_pin_upper_jnt,
                                                       maintainOffset=False)
            lower_pin_point_const = pm.pointConstraint([self.skin_joints[1], self.pole_vec_obj],
                                                       self.pole_pin_lower_jnt,
                                                       maintainOffset=False)
            upper_pin_aim_const = pm.aimConstraint(self.pole_pin_lower_jnt,
                                                   self.pole_pin_upper_jnt,
                                                   worldUpType='objectrotation',
                                                   worldUpObject=self.skin_joints[0],
                                                   aimVector=[-1,0,0] if self.mirror else [1,0,0] )
            lower_pin_aim_const = pm.aimConstraint(self.skin_joints[2],
                                                   self.pole_pin_lower_jnt,
                                                   worldUpType='objectrotation',
                                                   worldUpObject=self.skin_joints[1],
                                                   aimVector=[-1,0,0] if self.mirror else [1,0,0] )

            pole_lock_rev = pm.createNode("floatMath", name=f"{self.limb_name}_limb_pole_lock_rev_floatmath")
            pole_lock_rev.operation.set(1)
            pm.connectAttr(f"{self.driver_object}.{limb_pole_lock.driver_attr_str}", pole_lock_rev.floatB)
            pm.connectAttr(pole_lock_rev.outFloat, f"{lower_pin_point_const}.{self.skin_joints[1]}W0")
            pm.connectAttr(f"{self.driver_object}.{limb_pole_lock.driver_attr_str}", f"{lower_pin_point_const}.{self.pole_vec_obj}W1")

        if self.bend_setup:
            pass

        return None


# class RigCreator:
#     def __init__(self, main_grp_name=""):
#         super().__init__()
#         self.main_grp = main_grp_name
#         self.rig_setup_grp = "rig_setup"
#         self.ctls_grp = "ctrls"
#
#         self.extracted_controller_grp = "ctls_extracted"
#         self.extracted_control_suffix = "ctl_extracted"
#
#         self.grp = "grp"
#         self.ctl = "ctl"
#         self.loc = "loc"
#         self.ctl_grps = []
#
#     def create_nurbs_cube(self, name=""):
#         ctl = pm.curve(d=1,
#                        p=[(-0.5, -0.5, .5), (-0.5, .5, .5), (.5, .5, .5), (.5, -0.5, .5),
#                           (.5, -0.5, -0.5), (.5, .5, -0.5), (-0.5, .5, -0.5), (-0.5, -0.5, -0.5),
#                           (.5, -0.5, -0.5), (.5, .5, -0.5), (.5, .5, .5), (-0.5, .5, .5),
#                           (-0.5, .5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, .5), (.5, -0.5, .5)],
#                        n=f'{name}_ctl')
#         return ctl
#
#
#     def base_ctrls_create(self, joint_set=list):
#         """
#
#         :param joint_set: list of multiple pm.nt.Joint types to create a cube nurbs curve for
#         :return:
#         """
#
#         self.ensure_setup_is_correct()
#
#         for jnt in joint_set:
#             jnt_parent = jnt.getParent() if jnt.getParent().exists() else None
#             parent_ctl = f"{jnt_parent}_{self.grp}"
#             parent_grp = f"{jnt_parent}_{self.grp}"
#             grp = pm.group(name=f"{jnt}_{self.grp}", empty=True)
#             if pm.objExists(f"{jnt}_{self.extracted_control_suffix}"):
#                 ctl = pm.duplicate(f"{jnt}_{self.extracted_control_suffix}", name=f"{jnt}_{self.grp}")
#             else:
#                 ctl = self.create_nurbs_cube(name=jnt)
#                 ctl.getShape().overrideRGBColors.set(1)
#                 if "_l_" in ctl.name():
#                     pm.color(ctl.getShape(), rgb=blue)
#                 elif "_r_" in ctl.name():
#                     pm.color(ctl.getShape(), rgb=red)
#                 else:
#                     pm.color(ctl.getShape(), rgb=yellow)
#
#             pm.parent(ctl, grp)
#             pm.xform(grp, matrix=pm.xform(jnt, q=True, matrix=True, ws=True), ws=True)
#             if pm.objExists(f"{jnt_parent}_{self.grp}"):
#                 pm.parent(grp, parent_ctl)
#
#         return None
#
#
#
#     def fkik_setup(self, input_joints=[pm.nt.Joint, pm.nt.Joint, pm.nt.Joint], slerp_t_obj=pm.nt.Transform, slerp_t_attr=""):
#         fk_joint_chain = pm.duplicate(input_joints, parentOnly=True, name="fk_joints_temp")
#         ik_joint_chain = pm.duplicate(input_joints, parentOnly=True, name="ik_joints_temp")
#         skin_joint_chain = pm.duplicate(input_joints, parentOnly=True, name="skin_joints_temp")
#
#         for index, jnt in enumerate(input_joints):
#             fk_jnt = fk_joint_chain[index]
#             ik_jnt = ik_joint_chain[index]
#             skin_jnt = skin_joint_chain[index]
#             fk_jnt.rename(jnt.name().replace("_jnt", "_fk_jnt") if "jnt" in jnt.name() else f"{jnt.name()}_fk_jnt")
#             ik_jnt.rename(jnt.name().replace("_jnt", "_ik_jnt") if "jnt" in jnt.name() else f"{jnt.name()}_ik_jnt")
#             skin_jnt.rename(jnt.name().replace("_jnt", "_skin_jnt") if "jnt" in jnt.name() else f"{jnt.name()}_skin_jnt")
#
#         for jnt in input_joints:
#             fk_jnt = pm.PyNode(jnt.name().replace("_jnt", "_fk_jnt") if "jnt" in jnt.name() else f"{jnt.name()}_fk_jnt")
#             ik_jnt = pm.PyNode(jnt.name().replace("_jnt", "_ik_jnt") if "jnt" in jnt.name() else f"{jnt.name()}_ik_jnt")
#             skin_jnt = pm.PyNode(jnt.name().replace("_jnt", "_skin_jnt") if "jnt" in jnt.name() else f"{jnt.name()}_skin_jnt")
#             self.fkik_quat_setup(name=jnt,
#                                  input_obj_a=fk_jnt,
#                                  input_obj_b=ik_jnt,
#                                  output_obj=skin_jnt,
#                                  slerp_t_obj=slerp_t_obj,
#                                  slerp_t_attr=slerp_t_attr)
#
#         self.ik_setup(jnt_a=ik_joint_chain[0], jnt_b=ik_joint_chain[1], jnt_c=ik_joint_chain[2])
#
#         return fk_joint_chain, ik_joint_chain, skin_joint_chain
#
#     def ik_setup(self, jnt_a, jnt_b, jnt_c):
#         """
#
#         :param jnt_a: IK joint chain top joint
#         :param jnt_b: IK joint chain middle joint
#         :param jnt_c: IK joint chain bottom joint
#         :return:
#         """
#         loc_centre_jnt = pm.spaceLocator()
#         loc_pv = pm.spaceLocator()
#         pm.parent(loc_pv, loc_centre_jnt)
#
#         point_const = pm.pointConstraint(jnt_a, jnt_c, loc_centre_jnt, maintainOffset=False)
#         pm.delete(point_const)
#         aim_const = pm.aimConstraint(jnt_b, loc_centre_jnt, maintainOffset=False)
#         pm.delete(aim_const)
#
#         loc_pv.tx.set(20)
#
#         ik_handle = pm.ikHandle(startJoint=jnt_a, endEffector=jnt_c)
#         pv_const = pm.poleVectorConstraint(loc_pv, ik_handle[0])
#         return loc_centre_jnt, loc_pv, ik_handle, pv_const
#
#
#
#     def bend_setup(self,
#                    name="",
#                    upper_joint=pm.nt.Joint,
#                    mid_joint=pm.nt.Joint,
#                    lower_joint=pm.nt.Joint,
#                    upper_mid_twist_joints=list,
#                    mid_lower_twist_joints=list):
#         """
#
#         :param upper_joint:
#         :param name:
#         :return:
#         """
#
#         self.ensure_setup_is_correct()
#
#         bend_setup_grp = pm.group(name=f"{name}_bend_setup_grp", empty=True)
#         pm.parent(bend_setup_grp, self.rig_setup_grp)
#
#         joint_count = 2 + len(upper_mid_twist_joints) + len(mid_lower_twist_joints)
#         pm.polyPlane()
#
#         return None
#
#     def mirror_control_shapes(self, controls=[]):
#
#         if not controls:
#             controls = pm.selected(type=pm.nt.Transform)
#
#         for control in controls:
#             if "_l_" in control.name():
#                 mirror_control = pm.PyNode(control.name().replace("_l_", "_r_"))
#             else:
#                 mirror_control = pm.PyNode(control.name().replace("_r_", "_l_"))
#             dup_control = pm.duplicate(control, rr=True)
#             pm.delete(mirror_control.getShape(), shape=True)
#             pm.parent(dup_control[0].getShape(), mirror_control, r=True, s=True)
#             pm.delete(dup_control)
#
#         return None
#
#     def copy_control_shapes(self, controls=[]):
#
#         if not controls:
#             controls = pm.selected(type=pm.nt.Transform)
#
#         dup_control = pm.duplicate(controls[0], rr=True)
#         pm.delete(controls[1].getShape(), shape=True)
#         pm.parent(dup_control[0].getShape(), controls[1], r=True, s=True)
#         pm.delete(dup_control)
#
#         return None
