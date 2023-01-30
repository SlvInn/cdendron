#!./venv/bin/python3 
# example.py
#
# Produce the genealogy tree of a set of user defined classes
# silvia.innocenti@ec.gc.ca, Jan 2023
# 


# import the function to create the garphic
from cltree import generate_tree 
from cltree import get_userdef_classes as get_classes


# # manually get the list of considerd classes:
# from example_module.ex_vehicles import *
# import inspect  
# import sys
# classes = [obj for _,obj in inspect.getmembers(sys.modules[__name__], inspect.isclass) ]
# classes = [c for c in classes if 'ex_vehicles' in c.__module__]
# print("\n classes from manual import")
# print([s.__name__ for s in classes])


# # get the list of considerd classes with the get_classes function
module = '/home/sin007/ords/codes/cdendron/example_module/'
classes = get_classes(module)

# print the list of classes
print("\n classes from get_classes_from_module")
print([s.__name__ for s in classes])
print("\n")





# define a tree maker
tree_gr = generate_tree(classes,show_object=False) #show_all=True, show_internal=False


# create a graphic and export it into the desired format
grfname = module  + 'classes_tree'
tree_gr.render(grfname, format='pdf')
tree_gr.render(grfname, format='png')


# define a tree maker
tree_gr = generate_tree(classes,show_object=False,show_methods=False) #show_all=True, show_internal=False


# create a graphic and export it into the desired format
grfname = module  + 'classes_tree_withour_methods'
tree_gr.render(grfname, format='png')