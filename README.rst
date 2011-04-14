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

* Written in `Python <http://python.org>`_ using the `Pyramid <http://pylonsproject.org>`_ web framework
* `SQLAlchemy <http://sqlalchemy.org>`_ database model of `Yum <http://yum.baseurl.org>`_ Categories, Groups, Packages, and Dependencies
* Interactive graph widget, using `ToscaWidgets2 <http://toscawidgets.org/documentation/tw2.core>`_ and the `JavaScript InfoVis Toolkit <http://thejit.org>`_
* Package mouse-over menus linking to downloads, acls, code
  bugs, builds and updates.
* Deep linking
* Search bar with auto-completion

Source
~~~~~~

* `Git repository <http://fedorapeople.org/gitweb?p=lmacken/public_git/leafymiracle>`_ on fedorapeople.

Running
~~~~~~~

::

   sudo yum -y install python-virtualenv
   git clone git://fedorapeople.org/~lmacken/leafymiracle && cd leafymiracle
   virtualenv env && source env/bin/activate
   python setup.py develop
   python leafymiracle/populate.py
   paster serve development.ini

Authors
~~~~~~~

* Luke Macken <lmacken@redhat.com>
* Ralph Bean <ralph.bean@gmail.com>
