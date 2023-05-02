# Seasons
Facilitates the transfer of Ren'py game data using the save folder method

Instructions for use are provided vie the comments in the `season.rpy` file itself.

I know that this works in Ren'Py 7.4.10.2178 and 7.4.11.2266
I have not tested it in any other version - your mileage may vary!

# WARNING!
This technique is NOT recommended or supported by the official Ren'Py development team!
In fact, they are startled that it works at all!

Only data that is normally saved within save slots will be available:
- Variables that have been properly defaulted.
- JSON data added to the save via the relevant callback.
This does not include:
- Anything `define`d, including Characters.
- Anything initialised as a Python one-liner ($).
- Transforms, etc.
If you want these constants in the new project, you'll need to copy those manually as part of the script.
