import pymel.core as pm

# This needs updating and cleaning up, just wanted it working quickly

def time_slider_bookmarks_to_game_exporter():
    unordered_bookmarks = pm.ls(type="timeSliderBookmark")
    bookmarks = []
    for bookmark in unordered_bookmarks:
        bm_timestart = bookmark.timeRangeStart.get()
        bm_timestop = bookmark.timeRangeStop.get()
        bm_color = bookmark.color.get()
        bm_name = pm.getAttr(f"{bookmark}.name")
            # a straight .name on the object gets the object name rather than the "name" attribute

        bookmarks.append({"name": bm_name,
                          "start_frame": bm_timestart,
                          "end_frame": bm_timestop,
                          "color": bm_color})

    anim_clip_len = len(pm.getAttr("gameExporterPreset2.animClips", mi=True) or [])
    for i in range(anim_clip_len):
        pm.mel.eval("gameExp_DeleteAnimationClipLayout 0;")

    for index, bookmark in enumerate(bookmarks):
        gep_ac = f"gameExporterPreset2.animClips[{index}]"
        pm.setAttr(f"{gep_ac}.animClipName", bookmark["name"])
        pm.setAttr(f"{gep_ac}.animClipStart", bookmark["start_frame"])
        pm.setAttr(f"{gep_ac}.animClipEnd", bookmark["end_frame"])
