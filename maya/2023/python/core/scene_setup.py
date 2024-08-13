"""

"""
import pymel.core as pm


def scene_setup():
    """

    :return:
    """

    scene = ["characters", "environment", "lights"]

    for grp in scene:
        if not pm.objExists(grp):
            pm.group(name=grp, empty=True)

    return None
