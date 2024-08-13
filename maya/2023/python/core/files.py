"""

"""

# SYSTEM IMPORTS
import pathlib

# EXTERNAL IMPORTS
import pymel.core as pm

# LOCAL IMPORTS


def current_paths():
    """
    Gets path information from the current scene and returns any required data about the current maya scene
    :return: full_path, file_name, raw_name, extension
    """
    full_path = pathlib.Path(pm.sceneName())
    file_name = full_path.name
    raw_name = full_path.stem
    extension = full_path.suffix

    return full_path, file_name, raw_name, extension


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
            result = check_dir_for_project_settings_file(directory=directory.parent,
                                                recursion_amount=recursion_amount,
                                                recursion_limit=recursion_limit)
            if result:
                return result

    project_tld = check_dir_for_project_settings_file(directory=dir_to_check, recursion_amount=0, recursion_limit=5)
    print(project_tld)

    cache_dir = pathlib.Path(project_tld, "cache")

    return project_tld, cache_dir


def convert_to_reference(objects: list) -> None:
    """
    Duplicates a reference and makes sure the new one matches the currently selected one
    Currently doesn't duplicate animation curves, and needs a bit of cleanup
    :return:
    """

    # TODO AFOX: refactor??

    selected_object = pm.selected()

    if not selected_object:
        raise Exception("Nothing selected!")

    ref_object = selected_object[0]

    if ":" not in ref_object.name():
        raise Exception("First selected object isn't referenced!")

    ref_name = ref_object.name().split(":")[0]
    ref_path = pm.referenceQuery(ref_object, filename=True)

    new_nodes = pm.createReference(ref_path, namespace=ref_path.replace("\\", "/").split("/")[-1].split(".ma")[0],
                                   returnNewNodes=True)

    new_ref_name = new_nodes[0].split(":")[0]
    print(ref_name, new_ref_name)

    affect_objects = [x for x in new_nodes if x.type() in ["transform", "locator"]]

    for new_obj in affect_objects:
        new_obj_attrs = new_obj.listAttr(keyable=True)
        for attr in new_obj_attrs:
            attr.set(pm.getAttr(f"{ref_name}:{attr.name().split(':')[-1]}"))

    pm.select([x.replace(ref_name, new_ref_name) for x in selected_object])

    return ref_path
