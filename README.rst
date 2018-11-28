donjon-painter - Dungeon Map Maker
==================================

donjon-painter is a companion script to `donjon's Random Dungeon Generator`_. By selecting a TSV file along with a set of tile assets, you can easily create large, beautiful dungeon maps.

.. _donjon's Random Dungeon Generator: https://donjon.bin.sh/fantasy/dungeon/

-------------
Prerequisites
-------------
- Python:
    - >= 3.4
    - Pillow

Installation
============

-----------
Windows EXE
-----------
Windows users have the option of downloading an EXE version of the script, which can be found `over here`_. You'll need to run the EXE from the terminal - this can be done more easily by editing your `PATH`_ environment variable.

.. _over here: https://github.com/Blackflighter/donjon-painter/releases/
.. _PATH: https://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/

---------
Using pip
---------
donjon-painter is available on PyPI. Until I get to creating packages for different Linux distributions, this is the ideal way of using it on them. Get it using this command:

::

    pip install --user --upgrade donjon-painter

--------
setup.py
--------
This requires you to download the TAR.GZ version of donjon-painter, found `here`_. Having done so, extract the files, and navigate to the location of said folder. Having done this, run this command:

::

    python3 setup.py install

.. _here: https://github.com/Blackflighter/donjon-painter/releases/

Usage
=====
-------------------------
1. Download your TSV file
-------------------------
First of all, begin by heading to `donjon's Random Dungeon Generator`_ to generate the dungeon of your liking. Having done that, you should select the option to download a TSV map of the generated file, as depicted below:

.. image:: /res/donjon.png
.. _donjon's Random Dungeon Generator: https://donjon.bin.sh/fantasy/dungeon/

------------------
2. Run the command
------------------
Having done this, run donjon-painter. The most basic command for making the script run is to specify both the command and the map file of your choice:

::

    donjon-painter [OPTIONS] MAPFILE

If you're using the EXE file, you may have to specify the location of it beforehand to make things work.

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