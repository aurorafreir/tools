TOOLS_DIR=$(dirname "$0") # Gets this script's running directory"

export PYTHONPATH="$TOOLS_DIR/python"
export MAYA_MODULE_PATH="$TOOLS_DIR/third_party/mgear_4.2.2/release"
export MAYA_PLUG_IN_PATH="$TOOLS_DIR/plugins"
export XBMLANGPATH="$TOOLS_DIR/icons"
export MAYA_SHELF_PATH="$TOOLS_DIR/shelves"

maya