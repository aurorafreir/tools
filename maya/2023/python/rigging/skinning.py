"""
Trans Rights are Human Rights

A collection of skinning utilities that I use for my personal work.
"""
# SYSTEM IMPORTS
import pathlib

# STANDARD LIBRARY IMPORTS
import pymel.core as pm
import mgear.core.skin as skin
import ngSkinTools2.api as ngst_api

# LOCAL APPLICATION IMPORTS
from core import files


def export_skin():
    filepath, filename, raw_name, extension = files.current_paths()
    
    skin_dir = pathlib.Path(filepath.parent, "data", raw_name)
    skin_dir.mkdir(exist_ok=True, parents=True)

    skin_clusters = pm.ls(type="skinCluster")
    if skin_clusters:
        for i in skin_clusters:
            mesh = i.outputGeometry.listConnections()[0]
            skin_path = pathlib.Path(skin_dir, f"{mesh.name()}.jSkin")
            skin.exportSkin(filePath=skin_path.as_posix(), objs=[mesh])

        for i in pm.ls(type="ngst2SkinLayerData"):
            try:
                mesh = i.skinCluster.listConnections()[0].outputGeometry.listConnections()[0]
                output_file_name = pathlib.Path(skin_dir, f"ngskin_{mesh}.json")
                ngst_api.export_json(i.name(), file=output_file_name.as_posix())
                pm.displayInfo(f"Exported {i.name()} as {output_file_name.as_posix()}")
            except:
                pass

    else:
        print("No Skinclusters in scene!")

    return None

    
def import_skin():
    filepath, filename, raw_name, extension = files.current_paths()

    skin_dir = pathlib.Path(filepath.parent, "data", raw_name)
    print([i.name for i in list(skin_dir.glob("**/*"))])
    for file_name in list(skin_dir.glob("**/*")):
        if file_name.name.endswith(".jSkin"):
            mesh_name = file_name.name.split(".jSkin")[0]
            print(f"# Imported skin data for {mesh_name}")
            print(mesh_name)
            skin.importSkin(file_name.as_posix(), [mesh_name])
        if file_name.name.startswith("ngskin_"):
            mesh_name = file_name.name.split("ngskin_")[1].split(".json")[0]

            config = ngst_api.InfluenceMappingConfig()
            config.use_distance_matching = True
            config.use_name_matching = False

            ngst_api.import_json(
                mesh_name,
                file=pathlib.Path(skin_dir, file_name).as_posix(),
                vertex_transfer_mode=ngst_api.VertexTransferMode.vertexId,
                influences_mapping_config=config,
            )
            print(f"# Imported ngskin data for {mesh_name}")

    return None
