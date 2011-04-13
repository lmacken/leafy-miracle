The auspicious and venerable Leafy Miracle
==========================================

::

|-----------------------------------------------|
|         _______________                       |
|        < leafymiracle! >                      |
|         ---------------                       |
|                \                              |
|                 \     .---. __                |
|            ,     \   /     \   \    ||||      |
|           \\\\      |O___O |    | \\||||      |
|           \   //    | \_/  |    |  \   /      |
|            '--/----/|     /     |   |-'       |
|                   // //  /     -----'         |
|                  //  \\ /      /              |
|                 //  // /      /               |
|                //  \\ /      /                |
|               //  // /      /                 |
|              /|   ' /      /                  |
|              //\___/      /                   |
|             //   ||\     /                    |
|             \\_  || '---'                     |
|             /' /  \\_.-                       |
|            /  /    --| |                      |
|            '-'      |  |                      |
|                      '-'                      |
|_______________________________________________|

Features
~~~~~~~~

* Written in Python using the Pyramid web framework
* SQLAlchemy database model of Categories
* Interactive graph widget, using ToscaWidgets2 and the JIT
* Package mouse-over menus linking to downloads, acls, code
  bugs, builds and updates.
* Deep linking

Running
~~~~~~~

::

$ sudo yum -y install python-virtualenv
$ virtualenv env && source env/bin/activate
$ python setup.py develop
$ python leafymiracle/populate.py
$ paster serve development.ini

Authors
~~~~~~~

* Luke Macken <lmacken@redhat.com>
* Ralph Bean <ralph.bean@gmail.com>
