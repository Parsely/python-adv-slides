# python-adv-slides

This is a set of slides for a 3-day course on Python intended for existing programmers who want to learn the joy that is the Zen of Python.

It does not waste time teaching the basics of programming -- instead, it dives right into what makes Python special. The first day is spent exploring common Python idioms and ways of doing things.

The second day is spent on advanced Python features and techniques that make the language such a joy to use.

The final day is spent on learning the Python standard library and all its wonders.

I have given this presentation at places like BarCamp, HackNY, and other smaller conferences and gatherings.

## View the slides online

Slides can be viewed in compiled form at:

http://pixelmonkey.org/pub/python-training/

## How this was built

Using Python, of course. It's turtles all the way down.

I wrote the slides using [reST](http://docutils.sourceforge.net/rst.html), and specifically Docutils [support for S5 export](http://docutils.sourceforge.net/docs/user/slide-shows.html). Scripts are included to compile the presentation from the index.rst file and also to allow development of new slides with live recompilation using pyinotify (Linux systems only). See `build.sh` and `monitor.sh` for more information.
