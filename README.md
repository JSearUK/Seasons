# Seasons
Facilitates the transfer of Ren'py game data between projects, using the save folder method.

Instructions for use are provided via the comments in the `season.rpy` file itself.

This code is freeware.

---
WARNING!
- This technique is NOT recommended or supported by the official Ren'Py development team!
- In fact, they are startled that it works at all!
- This code is provided "as is" - I will not be providing support.
---
```php
Version 1.0

RenPy 7.4.10.2178 and 7.4.11.2266
```
- I have not tested it in any other version of Ren'Py
---

NOTE:
### Only data that is normally saved within save slots will be available:
- Variables that have been initialised with `default`.
- JSON data added to the save via the relevant callback.
### This does not include:
- Anything initialised with `define`, including Characters.
- Anything initialised with a Python one-liner (`$`).
- Transforms, etc.
### If you want these *constants* to be in the new project, you'll need to copy those manually as part of the script.
