 _______________
< leafymiracle! >
 ---------------
        \
         \     .---. __
    ,     \   /     \   \    ||||     
   \\\\      |O___O |    | \\||||
   \   //    | \_/  |    |  \   /     
    '--/----/|     /     |   |-'      
           // //  /     -----'        
          //  \\ /      /             
         //  // /      /              
        //  \\ /      /
       //  // /      /                
      /|   ' /      /
      //\___/      /                  
     //   ||\     /                   
     \\_  || '---'                    
     /' /  \\_.-
    /  /    --| |                     
    '-'      |  |
              '-'                     

[ Features ]

* Written in Python using the Pyramid web framework
* SQLAlchemy database model of Categories
* Interactive graph widget, using ToscaWidgets2 and the JIT
* Package mouse-over menus linking to downloads, acls, code
  bugs, builds and updates.
* Deep linking

[ Running ]

$ virtualenv --no-site-packages env && source env/bin/activate
$ ./link_in_system_modules.sh
$ python setup.py develop
$ python leafymiracle/populate.py
$ paster serve development.ini

[ Authors ]

* Luke Macken <lmacken@redhat.com>
