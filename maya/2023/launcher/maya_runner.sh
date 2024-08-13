
TOOLS_DIR=$(dirname "$PWD"); # Gets this script's running directory"

export PYTHONPATH="$TOOLS_DIR/python";
export MAYA_MODULE_PATH="$TOOLS_DIR/third_party/mgear_4.2.2/release";
#export MAYA_PLUG_IN_PATH="$SCRIPT_DIR/plugins";
#export XBMLANGPATH="$SCRIPT_DIR/icons/%B";
export MAYA_SHELF_PATH="$TOOLS_DIR/shelves";

#export MGEAR_SHIFTER_COMPONENT_PATH="$SCRIPT_DIR/mGearScripts/Components/";

maya;
