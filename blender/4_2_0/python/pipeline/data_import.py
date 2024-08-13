import bpy
import pathlib


# TODO AFOX: convert this to a core function rather than duplicate in maya/blender toolset
def current_paths():
    """
    Gets path information from the current scene and returns any required data about the current maya scene
    :return: full_path, file_name, raw_name, extension
    """
    full_path = pathlib.Path(bpy.data.filepath)
    file_name = full_path.name
    raw_name = full_path.stem
    extension = full_path.suffix

    return full_path, file_name, raw_name, extension

# TODO AFOX: convert this to a core function rather than duplicate in maya/blender toolset
def get_project_directories():
    full_path, _, _, _ = current_paths()

    dir_to_check = full_path.parent

    def check_dir_for_project_settings_file(directory, recursion_amount, recursion_limit):
        """
        recursion is confusing and scary :) (i am kidding but this might need rewriting)
        :param directory:
        :param recursion_amount:
        :param recursion_limit:
        :return:
        """
        for i in list(directory.iterdir()):
            if "project_settings.json" in i.name:
                return directory
            # else do nothing
        if recursion_amount <= recursion_limit:
            recursion_amount += 1
            return check_dir_for_project_settings_file(directory=directory.parent,
                                                       recursion_amount=recursion_amount,
                                                       recursion_limit=recursion_limit)

    project_tld = check_dir_for_project_settings_file(directory=dir_to_check, recursion_amount=0, recursion_limit=5)
    print(project_tld)

    cache_dir = pathlib.Path(project_tld, "cache")

    return project_tld, cache_dir


def delete_all_items_in_collection(collection_name):
    remove_collection_objects = True
    coll = bpy.data.collections.get(collection_name)
    if coll:
        if remove_collection_objects:
            obs = [o for o in coll.objects if o.users == 1]
            while obs:
                bpy.data.objects.remove(obs.pop())
        bpy.data.collections.remove(coll)


project_tld, cache_dir = get_project_directories()

# TODO AFOX: convert this to a core variable rather than duplicate in maya/blender toolset
collections = ["characters", "environment", "lights"]

for col in collections:
    if col not in [i.name for i in list(bpy.data.collections)]:
        collection = bpy.data.collections.new(col)
        bpy.context.scene.collection.children.link(collection)

# Set Scene as active collection
scene_collection = bpy.context.view_layer.layer_collection
bpy.context.view_layer.active_layer_collection = scene_collection

for cache_type in list(cache_dir.iterdir()):
    print(cache_type.name)

    if cache_type.name in [i.name for i in list(bpy.data.collections)]:
        delete_all_items_in_collection(cache_type.name)

    collection = bpy.data.collections.new(cache_type.name)
    bpy.context.scene.collection.children.link(collection)

for cache_type in list(cache_dir.iterdir()):
    for file in list(cache_type.iterdir()):
        print(file)
        bpy.ops.wm.alembic_import(filepath=file.as_posix())

        collection = bpy.data.collections[cache_type.name]

        for obj in bpy.context.selected_objects:
            for other_col in obj.users_collection:
                other_col.objects.unlink(obj)
            if obj.name not in collection.objects:
                collection.objects.link(obj)