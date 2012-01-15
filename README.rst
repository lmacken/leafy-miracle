`leafy-miracle.rhcloud.com <http://leafy-miracle.rhcloud.com>`_


.. image:: http://lewk.org/img/leafy-screenshot.png


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

* `Git repository <http://github.com/lmacken/leafy-miracle>`_ on github.

Running
~~~~~~~

::

   sudo yum -y install python-virtualenv
   git clone git://github.com/lmacken/leafy-miracle.git && cd leafy-miracle
   virtualenv env && source env/bin/activate
   python setup.py develop
   python leafymiracle/populate.py
   paster serve development.ini

Authors
~~~~~~~

* Luke Macken <lmacken@redhat.com>
* Ralph Bean <ralph.bean@gmail.com>
