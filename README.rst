donjon-painter - Dungeon Map Maker
==================================

This is a fork of the outdated `Blackflighter/donjon-painter`_.

donjon-painter is a companion script to `donjon's Random Dungeon Generator`_.
By selecting a TSV file along with a set of tile assets, you can easily create large, beautiful dungeon maps.
Learn how to create new tilesets for donjon-painter `here`_.

.. _Blackflighter/donjon-painter: https://github.com/Blackflighter/donjon-painter
.. _donjon's Random Dungeon Generator: https://donjon.bin.sh/fantasy/dungeon/
.. _here: https://github.com/donjon-painter/donjon-painter/blob/master/CONTRIBUTING.rst

-------------
Prerequisites
-------------
- Python:
    - >= 3.5
    - Pillow

Installation
============

---------------
Linux and MacOS
---------------

Download the appropriate executable from `the releases page`_.
Then extract the archive and run in the terminal.

::

    donjon-painter

.. _the releases page: https://github.com/donjon-painter/donjon-painter/releases/

------------------------
AUR Package (Arch Linux)
------------------------
If you're using Arch Linux, get the PKGBUILD `from here`_.

.. _from here: https://aur.archlinux.org/packages/donjon-painter/

---------
Using pip
---------
donjon-painter is `available on PyPI`_. Get it using this command:

::

    pip install --user --upgrade donjon-painter

.. _available on PyPI: https://pypi.org/project/donjon-painter/

-----------
Windows EXE
-----------
Windows users have the option of downloading an EXE version of the script, which can be found `over here`_.
If you wish to run the EXE in the terminal often, you can edit your `PATH`_ environment variable so you don't need to navigate to the program first.

.. _over here: https://github.com/donjon-painter/donjon-painter/releases/
.. _PATH: https://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/



--------
setup.py
--------
All that needs to be done here is to `clone this repository`_. Having done so, extract the files, and navigate to the location of said folder. Once you're done with that, run this command:

::

    python3 setup.py install

.. _clone this repository: https://help.github.com/articles/cloning-a-repository/

Usage
=====
-------------------------
1. Download your TSV file
-------------------------
First of all, begin by heading to `donjon's Random Dungeon Generator`_ to generate the dungeon of your liking. Having done that, you should select the option to download a TSV map of the generated file, as depicted below:

.. image:: https://raw.githubusercontent.com/donjon-painter/donjon-painter/master/res/donjon.png
.. _donjon's Random Dungeon Generator: https://donjon.bin.sh/fantasy/dungeon/

------------------
2. Run the command
------------------
Having done this, run donjon-painter. By default, if you don't specify anything, it will default to interactive mode. This brings up a menu of options in the terminal, which you can then input.

::

    donjon-painter

If you're using the EXE file, all you need to do is open it up, and this will bring you to interactive mode.

A more advanced usage entails specifying both the command and the map file of your choice:

::

    donjon-painter [OPTIONS] MAPFILE

------------------------------------
3. [Optional] Using interactive mode
------------------------------------
Creating a map in interactive mode is a fairly simple process. You'll be given a set of options to choose from, marked numerically. All you need to do is input said number, and follow the instructions provided.

At minimum, you must select your TSV file of choice, along with the theme you would like to use. Other options can be toggled/set if you'd like some further customisation.

.. image:: https://raw.githubusercontent.com/donjon-painter/donjon-painter/master/res/interactive.png

Options
=======
There's a number of things you can do to change the behaviour of this script, as detailed below.

::

    -h, --help          Display the commands below
    -t, --tileset       Specify a theme folder outside of the inbuilt ones (consult CONTRIBUTING.rst for further information)
    -m, --measure       Measure the time it takes to create your map
    -o, --output        Choose a different location/name to save your map to
    -p, --pixels        Choose a different size to make your map tiles in pixels (default 70)
    -r, --randomise     Shuffle the map floor patterns for some variation if required
    -s, --savetiles     Used in conjunction with the --tileset option, create a complete tileset theme (consult CONTRIBUTING.rst)
