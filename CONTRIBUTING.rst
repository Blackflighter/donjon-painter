Submitting New Themes
=====================
`Fork`_ this repository, and create a new theme folder (located in **donjon_painter/themes/**). The steps for creating a theme are down below. After doing so, make a `pull request`_ to this repository.

.. _Fork: https://help.github.com/articles/fork-a-repo/
.. _pull request: https://help.github.com/articles/about-pull-requests/

Creating New Themes 
===================
donjon-painter isn't limited to just the themes it comes with. You can easily make your own with a little work. Each theme is made up of 12 different tile assets, some rotated to face different ways (Top/Bottom/Left/Right).

Creating a theme is just a matter of making a folder of at least 12 images that comprise those 12 different asset types. Each image should be in the shape of a square, examples of which can be seen in this project's `theme folder`_, the inbuilt themes that donjon-painter comes with. These images will be automatically rotated when necessary - **you only need a single asset of each tile type** to make it work.

.. _theme folder: https://github.com/donjon-painter/donjon-painter/tree/master/donjon_painter/themes

Having chosen your selected theme, use the command below to make donjon-painter save these rotated images into a proper theme. While it'll work fine without those extra assets, it keeps things orderly, and taxes the script a little less. Make sure to name your image assets according to the `tile asset table`_.

::

   donjon-painter MAPFILE --tileset ./donjon_painter/themes/mytheme --savetiles

The command above will create a map from one of donjon's randomly generated dungeons, using the folder of assets you provided it. It will then attempt to fill out any gaps it can, automatically rotating the remaining images needed, saving them to the folder.

Alternatively, you can also open up donjon-painter in interactive mode (just run the program without any additional parameters), which will let you select your theme folder more dynamically. All you need to do is specify the directory of your theme folder. After doing so, select the option to generate your theme.

::

   donjon-painter

.. _tile asset table:

----------------
Tile Asset Table
----------------

+-----------------+---------------------+--------------------+
| Tile Types      | Asset Names         | Donjon TSV Symbol  |
+=================+=====================+====================+
| Floor           | 0-Floor             | F                  |
+-----------------+---------------------+--------------------+
| Space           | 1-Space             | (Blank Space)      |
+-----------------+---------------------+--------------------+
| Wall            | 2-T_Wall            | (Inferred by F)    |
|                 +---------------------+                    |
|                 | 2-B_Wall            |                    |
|                 +---------------------+                    |
|                 | 2-L_Wall            |                    |
|                 +---------------------+                    |
|                 | 2-R_Wall            |                    |
+-----------------+---------------------+--------------------+
| Inwards Corner  | 3-TR_Corner_I       | (Inferred by F)    |
|                 +---------------------+                    |
|                 | 3-BR_Corner_I       |                    |
|                 +---------------------+                    |
|                 | 3-BL_Corner_I       |                    |
|                 +---------------------+                    |
|                 | 3-TL_Corner_I       |                    |
+-----------------+---------------------+--------------------+
| Outwards Corner | 4-TR_Corner_O       | (Inferred by F)    |
|                 +---------------------+                    |
|                 | 4-BR_Corner_O       |                    |
|                 +---------------------+                    |
|                 | 4-BL_Corner_O       |                    |
|                 +---------------------+                    |
|                 | 4-TL_Corner_O       |                    |
+-----------------+---------------------+--------------------+
| Regular Door    | 5-T_Door            | DT                 |
|                 +---------------------+--------------------+
|                 | 5-B_Door            | DB                 |
|                 +---------------------+--------------------+
|                 | 5-L_Door            | DL                 |
|                 +---------------------+--------------------+
|                 | 5-R_Door            | DR                 |
+-----------------+---------------------+--------------------+
| Secret Door     | 6-T_Door_Secret     | DST                |
|                 +---------------------+--------------------+
|                 | 6-B_Door_Secret     | DSB                |
|                 +---------------------+--------------------+
|                 | 6-L_Door_Secret     | DSL                |
|                 +---------------------+--------------------+
|                 | 6-R_Door_Secret     | DSR                |
+-----------------+---------------------+--------------------+
| Portcullis Door | 7-T_Door_Portcullis | DPT                |
|                 +---------------------+--------------------+
|                 | 7-B_Door_Portcullis | DPB                |
|                 +---------------------+--------------------+
|                 | 7-L_Door_Portcullis | DPL                |
|                 +---------------------+--------------------+
|                 | 7-R_Door_Portcullis | DPR                |
+-----------------+---------------------+--------------------+
| Up Stair (1)    | 8-T_Stair_U         | SU                 |
|                 +---------------------+                    |
|                 | 8-B_Stair_U         |                    |
|                 +---------------------+                    |
|                 | 8-L_Stair_U         |                    |
|                 +---------------------+                    |
|                 | 8-R_Stair_U         |                    |
+-----------------+---------------------+--------------------+
| Up Stair (2)    | 9-T_Stair_UU        | SUU                |
|                 +---------------------+                    |
|                 | 9-B_Stair_UU        |                    |
|                 +---------------------+                    |
|                 | 9-L_Stair_UU        |                    |
|                 +---------------------+                    |
|                 | 9-R_Stair_UU        |                    |
+-----------------+---------------------+--------------------+
| Down Stair (1)  | 10-T_Stair_D        | SD                 |
|                 +---------------------+                    |
|                 | 10-B_Stair_D        |                    |
|                 +---------------------+                    |
|                 | 10-L_Stair_D        |                    |
|                 +---------------------+                    |
|                 | 10-R_Stair_D        |                    |
+-----------------+---------------------+--------------------+
| Down Stair (2)  | 11-T_Stair_DD       | SDD                |
|                 +---------------------+                    |
|                 | 11-B_Stair_DD       |                    |
|                 +---------------------+                    |
|                 | 11-L_Stair_DD       |                    |
|                 +---------------------+                    |
|                 | 11-R_Stair_DD       |                    |
+-----------------+---------------------+--------------------+
