# 
# cltree.py
#
# Functions to read the class genealogy from a python package or module
# and define a Digraph able to create a tree graphic and export it to a file
#
# silvia.innocenti@ec.gc.ca, Jan 2022
# adapted from .... 

# TODO: 
# - docs !!!
# - order and group methods (e.g., separate the inheritated methods from the new ones, 
#   group methods with similar uses, etc ...)
# 


from os import listdir
import sys
import inspect


from graphviz import Digraph


from inspect import getclasstree, isabstract, classify_class_attrs, signature
from html import escape
from types import  BuiltinFunctionType


# strings used in file names that must be ignored
IGNORED_STR = ['.v0','_v0','__init__','.old','_old','.tmp', '_tmp', '__pycache__']

 
def get_userdef_classes(fld,ignore_str=IGNORED_STR,ext='.py'):
    """
    get all the classes in a package: list all modules (files) in a package (folder)  
    and select the user-defined classes. 
    \n INPUT:
    fld -
    \n OPTIONS:
    ignore_str (lst) - List of strings identifying the file to be ignored .... 
    ext (str) - Extension of files to be considered. Default: '.py'
    """

    # assert fld[0]!='.', 'cannot use relative paths in dir'
    
    # get the list of files and folder in the specfied dir
    file_list = listdir(fld)
    sys.path.append(fld)
    
    # only select the files with the specified extension
    flist = [f for f in file_list if f[-3:]==ext]
    # print(flist)
    
    # get the list of classes in each file
    classes = []
    for f in flist:
        # print(f)
        
        # ignore the file, if its name contains one of the IGNORED_STR strings
        if not any([s in f  for s in ignore_str]):         
            
            # import the module from the file name
            __import__(f[:-3]) 
            
            
            # only select user-defined classes in the module
            mod = [m for m in sys.modules.keys() if f[:-3] in m]
            classes_f = []
            for m in mod:
                classes_f  += [obj for _,obj in inspect.getmembers(sys.modules[m], inspect.isclass) if type(obj) is obj.__class__] 
                    
            # select only classes defined in the specified module (no builtin)      
            classes += [c for c in classes_f  if f[:-3] in c.__module__]
   
    return [s for s in set(classes)]


def generate_tree(classes, **kwargs):
    """ 
    ...
    \n INPUT: 
    classes  - ....
    \n OPTIONS:
    **kwargs -  arguments to be passed to generate_digraph()
    """

    # get the class tree
    # print('get the class tree')
    # print(classes)
    classtree = getclasstree(classes, unique=True)
    # print(classtree)
    
    # generate graphic tree 
    tree = generate_digraph(classtree,  **kwargs) #show_all=True, 

    return tree


def generate_digraph(classtree, show_object=False, **kwargs):# show_internal=False,  hide_override=HIDE_METHODS, 
    """
    Recurse through classtree structure and return a Digraph object
    \n 
    INPUT:
    classtree
    \n OPTIONS:
    show_object (bool) - If True show the 'object' tree root (i.e. start the digraph to an user-derfined 
                        class called 'object')  Default: False
    **kwargs - arguments to be passed to the class_node function  
    """
    
    # def a digraph maker
    dot = Digraph(name=None, comment=None, filename=None, directory=None, format='svg', 
        engine=None, encoding='utf-8', graph_attr=None, node_attr=dict(shape='none'),
        edge_attr=dict( arrowtail='onormal', dir="forward"),body=None, strict=False) #dir="back"

    
    # def a function that ....
    def recurse(classtree):
        for classobjs in classtree:  
            if isinstance(classobjs, tuple):
                cls, bases = classobjs 
                
                if show_object or cls is not object:
                    # define a box with the class name and other info
                    dot.node(cls.__name__, label=class_node(cls, **kwargs))
                    
                for base in bases:
                    if show_object or base is not object:
                        dot.edge(base.__name__, cls.__name__, style="dashed" if isabstract(base) else 'solid')
            
            if isinstance(classobjs, list):
                recurse(classobjs)
                
    # call recurse to define all the tree knots         
    recurse(classtree)
    
    # return the digraph maker
    return dot


def class_node(cls, show_methods = True, show_internal=False, show_private=False, excluded_types= (BuiltinFunctionType), hide_override=set()): 
    """ 
    Define a digraph node to be shown as a rectangular box divided in up to 3 sub-sections: 
    ____________________
    |       Name       | 
    |__________________|
    | class attributes | 
    |__________________|
    |     methods      |
    |_________________ |
    
    INPUT:
    cls (obj) - ... 
    
    OPTIONS: 
    show_methods   (bool)  - If true show the class attributes in the 2nd box section, and 
                        and methods in the 3rd one, otherwise show only the class name. 
                        Default: True
    show_internal  (bool)  - If true list all internal and private method. Default: False
    hide_override          -  .... Default: set()
    excluded_types (tuple) - ... Default: (BuiltinFunctionType), i.e. exclude native python methods 
                        (e.g. __new__, __call__, etc)
    """
    italic_format = '<i>{}</i>'.format
    name_format   = italic_format if isabstract(cls) else format
    
    
    attributes = []
    methods    = []
    
    if show_methods:
        
        # get the abstract methods of the class (excluded for the oment)
        abstractmethods = getattr(cls, "__abstractmethods__", ())
        # TODO: add instructions to show abstract methods only in the first parent showing the method
    
        # # collect all the attribute and methods that we want to show
        for attr in classify_class_attrs(cls):
        
                 
            # check the attribute is an abstract method:
            is_absmtd = attr.name in abstractmethods
            
            # check if we are dealing with an interla or private method
            is_internal = attr.name[0] == '_' # this also include the check 'is_private' for which attr.name[:2] == '__'   
            # is_private  = attr.name[:2] == '__' # this only check for private method of the class, not for the parents
            is_private  = is_internal and ('__' in attr.name) # this checks for private method of the class and its parents
            
            # init a variable that defines if we must consider the method
            # ## show_this_att = True # show all
            # ## OR
            # show all class type that are not in the excluded types:
            show_this_att = not isinstance(attr.object, excluded_types) 
            
            # eliminate internal and private methods
            if not show_internal: 
                show_this_att = show_this_att and (not is_internal) # exclude private and internal methods
                
            if not show_private: 
                show_this_att = show_this_att and (not is_private) # exclude private methods    
                
            # hide override:
            show_this_att = show_this_att and attr.name not in hide_override
            
            # exclude the abstract methods
            show_this_att = show_this_att and not is_absmtd
            
            
            if show_this_att :
                
                # def a string for the method name
                if 'name' in abstractmethods:
                    name = italic_format(attr.name)
                else:
                    name = attr.name
                    
                    
                # classify the attributes in class properties and callable methods 
                if attr.kind in {'property', 'data'}: 
                    # add the class attributes in the first box section
                    attributes.append(name)
                else:
                    
                    # collect the method name and the input arguments
                    try:
                        args = escape(str(signature(attr.object)))
                    except (ValueError, TypeError) as e:
                        print(f' warning: not able to get signature for {attr}, {repr(e)}')
                        args = '()'
                    methods.append(name + args)
                
                
                
    # def the text sections for each node/box             
    td_align  = '<td align="left" balign="left">'
    line_join = '<br/>'.join
    
    attr_section   = f"<hr/><tr>{td_align}{line_join(attributes)}</td></tr>"
    method_section = f"<hr/><tr>{td_align}{line_join(methods)}</td></tr>"
    
    # Return a box with structure:
    # ____________________
    # |   Class name     | 
    # | ---------------- |
    # | class attributes | 
    # | ---------------- |
    # | class methods    |
    # |_________________ |
    
    clbox = f"""<
    <table border="1" cellborder="0" cellpadding="2" cellspacing="0" align="left">
    <tr><td align="center">
      <b>{name_format(cls.__name__)}</b>
    </td></tr>
    {attr_section}
    {method_section}
    </table>>"""   
    return clbox 
