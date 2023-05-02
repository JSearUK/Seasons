# [ SEASON IMPLEMENTATION ]

# WARNING: This file overrides the `file_slots(title):` screen. If you have
#   made any changes to that screen yourself, you should incorporate them into
#   the screen provided in this file (or vice versa).

# To use:
#  - Add this file to your project.
#  - If this is NOT Season 1, make sure that this line, in options.rpy, matches
#      the same line in your previous Season (around line 146):
#      `define config.save_directory = "Seasons Demo"`
#  - Adjust 'this_season', 'season_start_label' and 'season_epilogue' in the
#      Seasonal Control section below, to match your project
#  - If you need to save data for the next Season, use:
#      jump end_of_season-saving
#  - If you need to load data from the previous Season, use:
#      jump import_previous_season

# WARNING: Make sure the variable 'season_start_label', defaulted below, is set
#            to the label in your script where you wish to continue from after
#            loading gameplay data from a previous end-of-season save. For the
#            same reason, the label to jump to after making the end-of-season
#            save should also be set in 'season_epilogue'.
# WARNING: Do not set 'season_transfer' to True during the first season; there
#            is no previous Season to load from! Behaviour will be undefined,
#            dependant upon Developer script progression and control.


# Seasonal Control
define this_season = 1
define season_start_label = "true_start"
define season_epilogue = "epilogue"
default season = this_season
default season_transfer = False
default season_position = "Gameplay"


# End of Season Saving
# NOTE: 'jump' here when you reach the point in your script where you want to
#          create an end-of-season save. You can modify some of this.
label end_of_season_saving:
    if season_transfer:
        # This gets the game back on track after a seasonal load 'return's us
        #   here from 'label after_load' (as this is where we saved before...)
        $ season_transfer = False
        jump expression season_start_label
    $ season_position = "Ending"
    # \/\/\/ DEVELOPER CAN SAFELY MODIFY THE SECTION BELOW \/\/\/
    # Example: scene here
    $ renpy.say(narrator, "End of Season " + str(this_season) + ". Make a save before quitting -\n- it will be loadable at the beginning of Season " + str(this_season + 1) + ".")
    # Example: stop music and sounds here
    # /\/\/\ DEVELOPER CAN SAFELY MODIFY THE ABOVE SECTION /\/\/\
    $ season_position = "Gameplay"
    jump expression season_epilogue


# Beginning of Season Loading
# NOTE: 'jump' here when you reach the point in your script where you want to
#          import an end-of-season save. You can modify some of this.
label import_previous_season:
    $ season_transfer = True
    call screen load()
    # If we reach this point, the load failed: no save present, or the player
    #   exited the screen manually, or the dev set Seasons up incorrectly, etc.
    # \/\/\/ DEVELOPER CAN SAFELY MODIFY THE SECTION BELOW \/\/\/
    "Import unsuccessful.\nIf you exited out of the menu, click to re-enter it.\nIf there were no files to load: save here, create one in the previous season, then load here in this season - and click to try again."
    # /\/\/\ DEVELOPER CAN SAFELY MODIFY THE ABOVE SECTION /\/\/\
    jump import_previous_season


# NOTE: This is a special Ren'Py label that is called whenever a load happens.
#   It allows the developer to correct the game state, if necessary, before any
#   gameplay. You can modify some of this, and probably should.
label after_load:
    if not season == this_season:
        # The load came from the previous season. Block rollback. Hide any
        #   screens that may have been showing, are still present, and should
        #   not be seen now. Readjust any seasonal flags altered by the load.
        $ renpy.block_rollback()
        $ season = this_season
        $ season_transfer = True
        # \/\/\/ DEVELOPER CAN SAFELY MODIFY THE SECTION BELOW \/\/\/
        # Example: Update buggy variables here
        # /\/\/\ DEVELOPER CAN SAFELY MODIFY THE ABOVE SECTION /\/\/\
    # Let Ren'Py take us where we need to go...
    return


init python:
    # A function that will be called upon saving. This adds/updates JSON data
    #   that will be added to the save - this can be queried before loading.
    def s1_json_save_callback(save_dict):
        save_dict["Season"] = season
        save_dict["Season_Position"] = season_position

    # Registers the above function with the list of callbacks.
    config.save_json_callbacks.append(s1_json_save_callback)


# Overrides the `file_slots(title):` screen, to provide compatibility with the
#   the Seasons system.
screen file_slots(title):
    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"),
                                                     auto=_("Automatic saves"),
                                                     quick=_("Quick saves")
                                                    )
    use game_menu(title):
        fixed:
            order_reverse True
                ## This ensures the input will get the enter event before any
                ##   of the buttons do.

            ## The page name, which can be edited by clicking on a button.
            button:
                style "page_label"
                key_events True
                xalign 0.5
                action page_name_value.Toggle()
                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"
                xalign 0.5
                yalign 0.5
                spacing gui.slot_spacing
                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    # Seasonal code begins ------------------------------------
                    python:
                        slot = i + 1
                        slot_season = FileJson(slot, "Season")
                        slot_position = FileJson(slot, "Season_Position")
                        slot_name = FileSaveName(slot)
                        slot_empty = _("empty slot")
                        slot_time = FileTime(slot,
                                             format=_("{#file_time}"
                                                      "%A, %B %d %Y, %H:%M"),
                                             empty=slot_empty
                                            )
                        valid = (title == _("Save")
                                 and slot_time == slot_empty)
                        if season_transfer:
                            if (title == _("Load")
                                and slot_season == season-1
                                and slot_position == "Ending"):
                                    valid = True
                        elif slot_season == season:
                            if (title == _("Load")
                                or slot_position != "Ending"
                                or (slot_position
                                    == season_position
                                    == "Ending")):
                                        valid = True
                        elif not slot_season:
                            if this_season == 1:
                                valid = True
                        thumbnail = (FileScreenshot(slot) if valid
                                     else Null(width=config.thumbnail_width,
                                               height=config.thumbnail_height
                                              )
                                    )
                    # Seasonal code ends --------------------------------------

                    button:
                        sensitive valid
                        action FileAction(slot)
                        has vbox
                        add thumbnail xalign 0.5
                        if slot_name:
                            text slot_name:
                                style "slot_name_text"
                        if slot_season:
                            text _("Season {}: {}").format(slot_season,
                                                           slot_position):
                                style "slot_name_text"
                        text slot_time:
                            style "slot_time_text"
                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            hbox:
                style_prefix "page"
                xalign 0.5
                yalign 1.0
                spacing gui.page_spacing
                textbutton _("<") action FilePagePrevious()
                if config.has_autosave:
                    textbutton _("{#auto_page}A") action FilePage("auto")
                if config.has_quicksave:
                    textbutton _("{#quick_page}Q") action FilePage("quick")
                for page in range(1, 10):
                    ## range(1, 10) gives the numbers from 1 to 9.
                    textbutton "[page]" action FilePage(page)
                textbutton _(">") action FilePageNext()
