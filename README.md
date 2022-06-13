# filename-based-rename
Rename files in bulk based on other filenames.

# Example
An example use case is if you have a bunch of video, audio, and subtitle files, and you want them all to have the same general filename based on how one of them is already formatted. If we want to use the video filenames as a template, we put them in the left box and then put the other two sets of files in the right box as seen in this image:

![preview1](https://user-images.githubusercontent.com/99392600/173462160-31935abe-bdf2-4134-93e2-3b489bd3ce7d.png)

We change "Number of files to rename per template file" to 2 to indicate that there are two files to rename per video file (the subtitle and the audio). Note that order matters here. If we have more than one file per template file, they should be together as seen in the above image. Then we put in a suffix if we want one and then if we press "Preview Rename", we can see what the program will do:

![preview2](https://user-images.githubusercontent.com/99392600/173462292-e6ffc7b2-6708-4121-a864-3e2e2937d2dc.png)

If this looks good, press "Rename!" and then we're done!

# Installation
As of now there is no release or build of any kind, so you'll have to clone this repository and make sure you have the following dependencies:

- Python >=3.6.1 (as required by PySide6)
- PySide6 (`pip install pyside6`)

Then run `rename.py` and try it out!

In the future there may be a more proper release to avoid pushing these dependencies on potential users.
