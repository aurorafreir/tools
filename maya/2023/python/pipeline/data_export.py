"""

"""
import pathlib

import pymel.core as pm
from core import files
import json

from importlib import reload
reload(files)

def cache_mesh_set_to_alembic(set_type: str):
    """

    :return:
    """

    # TODO AFOX update to remove unneeded files
    # TODO AFOX update to not export template meshes

    if not pm.objExists(set_type):
        return None

    project_tld, cache_dir = files.get_project_directories()

    for mesh_set in pm.PyNode(set_type).getChildren():
        shape_nodes = pm.PyNode(mesh_set).getChildren(ad=True, type=pm.nt.Mesh)
        export_shape_nodes = []
        for i in shape_nodes:
            if i.intermediateObject.get():
                continue
            else:
                export_shape_nodes.append(i)

        pm.select(export_shape_nodes)

        set_cache_dir = pathlib.Path(cache_dir, set_type)
        set_cache_dir.mkdir(exist_ok=True)

        cache_path = pathlib.Path(set_cache_dir, mesh_set+".abc")

        arg = f"-sl -frameRange 1 1 -uvWrite -dataFormat ogawa -root {mesh_set} -file {cache_path.as_posix()}"
        pm.AbcExport(jobArg=arg)

    return None
