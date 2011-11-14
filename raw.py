'''
raw.py

author: Diana Cai <dcai@eecs.harvard.edu>
date: 10/03/11

library to take ingredient file of format:
    3 ounces of oil
    5 cups of flour
    3 eggs
    2 tbsp of sugar
and produce raw data files, converted to weights
with all the ingredients listed after the raw data.
'''
import os
import numpy as np
import tabular as tb
import pylab
import ellipse

from matplotlib.patches import Ellipse

#w = open('header.txt', 'w')
c = open('cases.txt', 'a')
e = open('error.txt', 'a')

t = 1 # TODO: need to fix this code

ingredients = {}    # contains the primary ingredients
proportions = {}    # has all the proportions of the primary ingredients
found_ingred = {}   # how many instances of each ingredient we find
ing = []            # help us determine if we want to throw the recipe out 

strings = ["1/8","1/4","1/3","3/8","1/2","5/8","2/3","3/4","7/8"]
floats = [0.125,0.25,0.333,0.375,0.5,0.625,0.666,0.75,0.875]

# arguments:
#   * ing_file: the ingredient file
#   * raw_out: the path to write raw data out to
#   * mode 0: allrecipes.com
#   * mode 1: epicurious.com ?
def get_rawdata(ing_out, raw_out, mode):
    
    _init()  # initialize stuff
    
    c = open('cases.txt', 'a')
    e = open('error.txt', 'a')

    ing_file = open(ing_out, 'r')
    
    for line in ing_file:
        if _get_ingredients(t, line.strip()) == "fail":
            e.write("breaking from " + raw_out.strip() + ": " + \
                line.strip() + "\n")
            break
    ing_file.close()

    # don't print anything if hit one of the cases we want to throw out 
    if _discard_recipe(t) == False: 
        pass
    else:
        # write raw data out to file
        out = open(raw_out, 'w')
        out.write(raw_out.strip().split('/')[-1].split('.')[0])
        print len(ingredients.keys())
        for key in sorted(ingredients.keys()): 
#            w.write(key + '\t')
            print key + ': ' + str(round(ingredients[key], 3))
            out.write('\t' + str(round(ingredients[key], 3)))
#        w.write('ingredients\n')

        #add_ingredients(ing_file, out, mode)
        ing_file = open(ing_out, 'r')
        out.write('\t[')
        for line in ing_file:
            out.write(line.strip() + '|')
        out.write(']' + '\n')
        out.close()

    ing_file.close()
#    _close_files()


def add_header(category_file):
    f = open('header.txt', 'w')
    f.write('names\tapplesauce\tbaking_powder\tbaking_soda\t' +\
            'beer\tbutter\tbuttermilk\tcake_mix\tchoco_chips\t' +\
            'cinnamon\tcocoa\tcream_cheese\tcream_half\t' +\
            'cream_ice\tcream_other\tcream_sour\tcream_tartar\t' +\
            'cream_whipped\tegg\tflour_all\tflour_almond\t' +\
            'flour_bread\tflour_cake\tflour_other\tflour_rice\t' +\
            'flour_rye\tflour_wheat\thoney\tjuice_apple\t' +\
            'juice_can\tjuice_cider\tjuice_lemon\tjuice_lime\t' +\
            'juice_orange\tjuice_other\tjuice_pineapple\tlard\t' +\
            'margarine\tmilk\tnuts_almond\tnuts_cashew\t' +\
            'nuts_other\tnuts_pecan\toats\toil_canola\toil_olive\t' +\
            'oil_other\toil_vegetable\traisins\tsalt\tshortening\t' +\
            'soda\tsoymilk\tsugar_brown\tsugar_powder\t' +\
            'sugar_white\tvanilla\twater\tyeast\tyogurt\tingredients\n')
    f.close()
    os.system("cat header.txt " + category_file + ' > a')
    os.system('mv a ' + category_file)


def get_ellipseinfo(raw_out, viz_out):
    
    w = open(viz_out, 'w')
    x = tb.tabarray(SVfile=raw_out)
    a = _normalize_array(x)

    for i in range(0, 4):
        for j in range(i + 1, 5):
            (xy, width, height, angle) = ellipse.get_ellipse(a[:,i], a[:,j])
            w.write(str(xy) + ',' + str(width) + ',' + str(height) + \
                    ',' + str(angle) + '\t'),
            
def plot(data, path):

    # clear figures
    for i in range(1, 11):
        pylab.figure(i)
        pylab.clf()

    os.system('mkdir ' + os.path.join(path, data.split('/')[-1].split('.')[0]))

    marksize = 6 
    window = False 

    _plot_file(data, 'b', marksize, window)
    _plot_file('harvard.tsv', 'r', marksize, window)
    
    flist = [data, 'harvard.tsv']
    
    c = 1
    names = ['egg', 'fat', 'flour', 'sugar', 'liquid']
    for i in range(0, 4):
        for j in range(i + 1, 5):
            pylab.figure(c)
            pylab.xlabel(names[i])
            pylab.ylabel(names[j])
            _plot_legend(flist, '.tsv', 'upper right')
            pylab.savefig(os.path.join(path, data.split('/')[-1].split('.')[0], names[i] + '_' + names[j] + '.png'))
            c += 1

##########################################################################
##########################################################################
##########################################################################

# initializes stuff, including ingred dict
def _init():
   
    ingredients['applesauce'] = 0.0

    ingredients['baking_powder'] = 0.0
    ingredients['baking_soda'] = 0.0
    
    ingredients['beer'] = 0.0
    
    ingredients['butter'] = 0.0
    ingredients['buttermilk'] = 0.0
    
    ingredients['cake_mix'] = 0.0
   
    ingredients['choco_chips'] = 0.0

    ingredients['cinnamon'] = 0.0
    ingredients['cocoa'] = 0.0
    
    ingredients['cream_cheese'] = 0.0
    ingredients['cream_half'] = 0.0
    ingredients['cream_ice'] = 0.0
    ingredients['cream_other'] = 0.0
    ingredients['cream_sour'] = 0.0
    ingredients['cream_tartar'] = 0.0
    ingredients['cream_whipped'] = 0.0
    
    ingredients['egg'] = 0.0 
    
    ingredients['flour_all'] = 0.0
    ingredients['flour_almond'] = 0.0
    ingredients['flour_bread'] = 0.0
    ingredients['flour_cake'] = 0.0
    ingredients['flour_other'] = 0.0
    ingredients['flour_rice'] = 0.0
    ingredients['flour_rye'] = 0.0
    ingredients['flour_wheat'] = 0.0

    ingredients['honey'] = 0.0
    
    ingredients['juice_apple'] = 0.0
    ingredients['juice_can'] = 0.0
    ingredients['juice_cider'] = 0.0
    ingredients['juice_lemon'] = 0.0
    ingredients['juice_lime'] = 0.0
    ingredients['juice_orange'] = 0.0
    ingredients['juice_other'] = 0.0
    ingredients['juice_pineapple'] = 0.0
    
    ingredients['lard'] = 0.0
    
    ingredients['margarine'] = 0.0
    
    ingredients['milk'] = 0.0

    ingredients['nuts_almond'] = 0.0
    ingredients['nuts_cashew'] = 0.0
    ingredients['nuts_other'] = 0.0
    ingredients['nuts_pecan'] = 0.0

    ingredients['oats'] = 0.0
    
    ingredients['oil_canola'] = 0.0
    ingredients['oil_olive'] = 0.0
    ingredients['oil_other'] = 0.0
    ingredients['oil_vegetable'] = 0.0
    
    ingredients['raisins'] = 0.0
    
    ingredients['salt'] = 0.0
    
    ingredients['shortening'] = 0.0
   
    ingredients['soda'] = 0.0
    
    ingredients['soymilk'] = 0.0
    
    ingredients['sugar_brown'] = 0.0
    ingredients['sugar_powder'] = 0.0
    ingredients['sugar_white'] = 0.0
    
    ingredients['vanilla'] = 0.0
    
    ingredients['water'] = 0.0
    
    ingredients['yeast'] = 0.0
    ingredients['yogurt'] = 0.0
 
    for key in ingredients.keys():
        found_ingred[key] = 0

def _get_ingredients(t, line):

    if t == 1: # bakery
        '''
        searches the line for the ingredient. 
        If present, we convert it to new unit (TBD) 
        and store it in the dictionary.
        '''
        first = line.split()[0] # first word
        if "dash" in first or "confectioner" in first or \
                "pinch" in first or "salt" in first or \
                "whipped" in first or "vanilla" in first or \
                "powdered" in first:
            return 1 # do nothing for these cases
        try:
            if "egg" in line:
                found_ingred['egg'] += 1
                if "yolk" in line:
                    ingredients['egg'] += _check_units(line, 1)
                elif "white" in line:
                    ingredients['egg'] += _check_units(line, 2)
                elif "substitute" in line:
                    ingredients['egg'] += _check_units(line, 3)
                else: # otherwise we assume it's a normal egg
                    ingredients['egg'] += _check_units(line, 0)
            elif "flour" in line:
                if "all-purpose" in line:
                    found_ingred['flour_all'] += 1
                    ingredients['flour_all'] += _check_units(line, 3)  
                elif "almond flour" in line:
                    found_ingred['flour_almond'] += 1
                    ingredients['flour_almond'] += _check_units(line, 3)  
                elif "bread flour" in line:
                    found_ingred['flour_bread'] += 1
                    ingredients['flour_bread'] += _check_units(line, 3)  
                elif "cake flour" in line:
                    found_ingred['flour_cake'] += 1
                    ingredients['flour_cake'] += _check_units(line, 3)  
                elif "rice flour" in line:
                    found_ingred['flour_rice'] += 1
                    ingredients['flour_rice'] += _check_units(line, 3)  
                elif "rye flour" in line:
                    found_ingred['flour_rye'] += 1
                    ingredients['flour_rye'] += _check_units(line, 3)  
                elif "wheat flour" in line:
                    found_ingred['flour_wheat'] += 1
                    ingredients['flour_wheat'] += _check_units(line, 3) 
                else:
                    found_ingred['flour_other'] += 1
                    ingredients['flour_other'] += _check_units(line, 3) 
            elif "baking powder" in line:
                found_ingred['baking_powder'] += 1
                ingredients['baking_powder'] += _check_units(line, 3)
            elif "baking soda" in line:
                found_ingred['baking_soda'] += 1
                ingredients['baking_soda'] += _check_units(line, 3)
            elif "butter or margarine" in line:
                found_ingred['butter'] += 1
                ingredients['butter'] += _check_units(line, 3)
            elif "butter" in line:
                if "buttermilk" in line:
                    found_ingred['buttermilk'] += 1
                    ingredients['buttermilk'] += _check_units(line, 3)
                if "shortening" in line:
                    found_ingred['shortening'] += 1
                    ingredients['shortening'] += _check_units(line, 3)
                else:
                    found_ingred['butter'] += 1
                    ingredients['butter'] += _check_units(line, 3)
            elif "margarine" in line:
                found_ingred['margarine'] += 1
                ingredients['margarine'] += _check_units(line, 3)
            elif "chocolate chips" in line:
                found_ingred['choco_chips'] += 1
                ingredients['choco_chips'] += _check_units(line, 3)
            elif "ground cinnamon" in line:
                found_ingred['cinnamon'] += 1
                ingredients['cinnamon'] += _check_units(line, 3)
            elif "cocoa" in line:
                found_ingred['cocoa'] += 1
                ingredients['cocoa'] += _check_units(line, 3)
            elif "cream" in line.split():
                if "whipped" in line or "whipping" in line:
                    found_ingred['cream_whipped'] += 1
                    ingredients['cream_whipped'] += _check_units(line, 3)
                elif "cheese" in line.split():
                    found_ingred['cream_cheese'] += 1
                    ingredients['cream_cheese'] += _check_units(line, 3)
                elif "half" in line:
                    found_ingred['cream_half'] += 1
                    ingredients['cream_half'] += _check_units(line, 3)
                elif "ice" in line:
                    found_ingred['cream_ice'] += 1
                    ingredients['cream_ice'] += _check_units(line, 3)
                elif "sour" in line.split():
                    found_ingred['cream_sour'] += 1
                    ingredients['cream_sour'] += _check_units(line, 3)
                elif "tartar" in line:
                    found_ingred['cream_tartar'] += 1
                    ingredients['cream_tartar'] += _check_units(line, 3)
                else:
                    found_ingred['cream_other'] += 1
                    ingredients['cream_other'] += _check_units(line, 3)
            elif "oatmeal" in line or "oats" in line:
                found_ingred['oats'] += 1
                ingredients['oats'] += _check_units(line, 3)
            elif "oil" in line.split():
                if "canola" in line.split():
                    found_ingred['oil_canola'] += 1
                    ingredients['oil_canola'] += _check_units(line, 3)
                elif "olive" in line.split():
                    found_ingred['oil_olive'] += 1
                    ingredients['oil_olive'] += _check_units(line, 3)
                elif "vegetable" in line.split():
                    found_ingred['oil_vegetable'] += 1
                    ingredients['oil_vegetable'] += _check_units(line, 3)
                else:
                    found_ingred['oil_other'] += 1
                    ingredients['oil_other'] += _check_units(line, 3)
            elif "nuts" in line: # walnuts, macadamia
                found_ingred['nuts_other'] += 1
                ingredients['nuts_other'] += _check_units(line, 3)
            elif "almonds" in line:
                found_ingred['nuts_almond'] += 1
                ingredients['nuts_almond'] += _check_units(line, 3)
            elif "cashews" in line:
                found_ingred['nuts_cashew'] += 1
                ingredients['nuts_cashew'] += _check_units(line, 3)
            elif "pecans" in line:
                found_ingred['nuts_pecan'] += 1
                ingredients['nuts_pecan'] += _check_units(line, 3)
            elif "raisins" in line:
                found_ingred['raisins'] += 1
                ingredients['raisins'] += _check_units(line, 3)
            elif "shortening" in line:
                found_ingred['shortening'] += 1
                ingredients['shortening'] += _check_units(line, 3)
            elif "lard" in line:
                found_ingred['lard'] += 1
                ingredients['lard'] += _check_units(line, 3)
            elif "applesauce" in line:
                found_ingred['applesauce'] += 1
                ingredients['applesauce'] += _check_units(line, 3)
            elif "water" in line:
                found_ingred['water'] += 1
                ingredients['water'] += _check_units(line, 3)
            elif "soda" in line:
                found_ingred['soda'] += 1
                ingredients['soda'] += _check_units(line, 3)
            elif "beer" in line:
                found_ingred['beer'] += 1
                ingredients['beer'] += _check_units(line, 3)
            elif "cider" in line:
                found_ingred['juice_cider'] += 1
                ingredients['juice_cider'] += _check_units(line, 3)
            elif "juice" in line:
                if "can" in line:
                    found_ingred['juice_can'] += 1
                    ingredients['juice_can'] += _check_units(line, 3)
                if "lemon" in line:
                    found_ingred['juice_lime'] += 1
                    ingredients['juice_lime'] += _check_units(line, 3)
                if "lime" in line:
                    found_ingred['juice_lemon'] += 1
                    ingredients['juice_lemon'] += _check_units(line, 3)
                if "orange" in line:
                    found_ingred['juice_orange'] += 1
                    ingredients['juice_orange'] += _check_units(line, 3)
                if "apple" in line:
                    found_ingred['juice_apple'] += 1
                    ingredients['juice_apple'] += _check_units(line, 3)
                if "pineapple" in line:
                    found_ingred['juice_pineapple'] += 1
                    ingredients['juice_pineapple'] += _check_units(line, 3)
                else:
                    found_ingred['juice_other'] += 1
                    ingredients['juice_other'] += _check_units(line, 3)
            elif "milk" in line:
                found_ingred['milk'] += 1
                ingredients['milk'] += _check_units(line, 3)
            elif "salt" in line.split():
                found_ingred['salt'] += 1
                ingredients['salt'] += _check_units(line, 3)
            elif "soymilk" in line:    
                found_ingred['soymilk'] += 1
                ingredients['soymilk'] += _check_units(line, 3)
            elif "honey" in line.split():    
                found_ingred['honey'] += 1
                ingredients['honey'] += _check_units(line, 3)
            elif "vanilla extract" in line:    
                found_ingred['vanilla'] += 1
                ingredients['vanilla'] += _check_units(line, 3)
            elif "sugar" in line:
                if "confectioner" in line:
                    found_ingred['sugar_powder'] += 1
                    ingredients['sugar_powder'] += _check_units(line,3)
                if "brown" in line.split():
                    found_ingred['sugar_brown'] += 1
                    ingredients['sugar_brown'] += _check_units(line,3)
                else:
                    found_ingred['sugar_white'] += 1
                    ingredients['sugar_white'] += _check_units(line,3)
            elif "yeast" in line.split():
                found_ingred['yeast'] += 1
                ingredients['yeast'] += _check_units(line, 3)
            elif "yogurt" in line.split():
                found_ingred['yogurt'] += 1
                ingredients['yogurt'] += _check_units(line, 3)
            elif "&nbsp;" in line or "FILLING:" in line or \
                    "FROSTING:" in line or "GLAZE:" in line or \
                    "EGG WASH:" in line or "TOPPING:" in line or \
                    "SAUCE:" in line or "CREAM:" in line or \
                    "ICING" in line or "GARNISH:" in line or \
                    "MERINGUE" in line:
                return "fail" 
            else:
                return 1 # ingredient not found; do nothing
        except TypeError:
            c.write("TypeError: " + line.strip() + '\n')
        except ValueError:
            c.write("ValueError: " + line.strip() + '\n')
        except IndexError:
            c.write("IndexError: " + line.strip() + '\n')
      
def _discard_recipe(t):
    if t == 1:
        # we require that all bakery items contain flour 
        if found_ingred['flour_almond'] == 0 and \
                found_ingred['flour_all'] == 0 and \
                found_ingred['flour_cake'] == 0.0 and \
                found_ingred['flour_bread'] == 0.0 and \
                found_ingred['flour_cake'] == 0.0 and \
                found_ingred['flour_other'] == 0.0 and \
                found_ingred['flour_rice'] == 0.0 and \
                found_ingred['flour_rye'] == 0.0 and \
                found_ingred['flour_wheat'] == 0.0:
            return False
        # catch cases where we double count butter and margarine
        if found_ingred['butter'] > 0 and found_ingred['margarine'] > 0:
            return False
        else:
            return True

def _check_units(line, ingred):
    '''
    checks the unit in the line
    ingred:
        0: normal egg
        1: egg yolk
        2: egg white
        3: normal ingredient
    '''
    # 1 egg = 1.75 oz
    if ingred == 0:
        try:
            eggs = float(line.split(' ')[0])
        except TypeError:
            c.write(line + '\n')
        return 1.75 * eggs
    # 1 egg yolk = 0.75 oz
    elif ingred == 1:
        try:
            eggs = float(line.split(' ')[0])
        except TypeError:
            c.write(line + '\n')
        return 0.75 * eggs
    # 1 egg white = 1.0 oz
    elif ingred == 2:
        try:
            eggs = float(line.split(' ')[0])
        except TypeError:
            c.write(line + '\n')
        return 1.0 * eggs
    # normal ingeredients : grab the string and then convert to float
    elif ingred == 3:
        return _convert_unit(line)
    else:
        print "something wrong happened in _check_units()"

def _convert_unit(line):
    # return oz
    if "oz" in line or "ounce" in line:
        try:
            return float(line.split(' ')[0]) 
        except TypeError:
            c.write(line + '\n')
    # 1 cup = 8.0 oz
    elif "cup" in line:
       cups = _string_to_float(line)
       return 8.0 * cups
    # 1 tsp = 0.1667 oz
    elif "teaspoon" in line:
        tsp = _string_to_float(line)
        return 0.1667 * tsp
    # 1 tbsp = 0.5 oz
    elif "tablespoon" in line:
        tbsp = _string_to_float(line)
        return 0.5 * tbsp
    # 1 lb = 16 oz
    elif "pound" in line:
        lb = _string_to_float(line)
        return 16.0 * lb
    # 1 gallon = 4 oz
    elif "gallon" in line:
        lb = _string_to_float(line)
        return 128.0 * lb
    # 1 stick of butter = 4 oz
    elif "stick" in line:
        stick = _string_to_float(line)
        return 4.0 * stick
    # 1 quart = 32 oz
    elif "quart" in line:
        quart = _string_to_float(line)
        return 32.0 * quart
    elif "pint" in line:
        pint = _string_to_float(line)
        return 16.0 * pint
    elif "dash" in line:
        return 0.01
    elif "pinch" in line:
        return 0.02
    elif "container" in line or "can" in line or "package" in line \
            or "bag" in line:
        container = _string_to_float(line) # number of packs
        try:
            ounces = float(line.strip().split('(')[1].split()[0]) # ounces in a pack
        except TypeError:
            c.write(line + '\n')
        return ounces * container
    elif "packet" in line and "oat" in line:
        packet = _string_to_float(line)
        return 1.0 * packet
    else:
        print "missing this unit in _check_units(): " + line

def _string_to_float(line):
    '''
    checks if one of the numbers in the strings list is in the line
    grabs the index of the matching string
    gets the appropriate float value and adds it to the whole number
    '''
    value = 0.0
    index = 0
    for string in strings:
        # if we have a fraction match, save the float in value
        if string in line: 
            index = strings.index(string)
            value = floats[index]
    # add the whole number to get the final value
    if line[0:3] != strings[index]:
        try:
            value += float(line.split(' ')[0])
        except TypeError:
            c.write(line + '\n')
    return value

def _add_ingredients(ing_file, raw_out, mode):
    raw_out.write('\t[')
    for line in ing_file:
        print line.strip()
        raw_out.write(line.strip() + '|')
    raw_out.write(']' + '\n')

def _close_files():
    e.close()
    c.close()

def _normalize_array(x):
    flour = tb.tabarray(columns=[x['flour_all'] + x['flour_almond'] + \
            x['flour_bread'] + x['flour_cake'] + x['flour_other'] + \
            x['flour_rice'] + x['flour_wheat'] + x['flour_rye']], \
            names=['flour'])

    liquid = tb.tabarray(columns=[x['milk'] + x['water'] + \
            x['soymilk'] + x['buttermilk'] + x['juice_apple'] + \
            x['juice_can'] + x['juice_lemon'] + x['juice_lime'] + \
            x['juice_orange'] + x['juice_other'] + x['juice_pineapple']], \
            names=['liquid'])

    fat = tb.tabarray(columns=[x['butter'] + x['cream_cheese'] + \
            x['cream_half'] + + x['cream_ice'] + x['cream_other'] + \
            x['cream_tartar'] + x['cream_whipped'] + x['margarine'] + \
            x['oil_canola'] + x['oil_olive'] + x['oil_other'] + \
            x['oil_vegetable'] + x['lard'] + x['shortening']], \
            names=['fat'])

    sugar = tb.tabarray(columns=[x['sugar_brown'] + x['sugar_powder'] + \
            x['sugar_white']], names=['sugar'])

    a = x[['egg']].colstack(fat).colstack(flour).colstack(liquid)\
            .colstack(sugar).extract()
    a = a / np.repeat(a.sum(axis = 1), a.shape[1])\
            .reshape(a.shape[0], a.shape[1])
    return a

def _plot_file(filename, col, marksize, window):
    array = tb.tabarray(SVfile=filename)
    a = _normalize_array(array)

    if not window:
        pylab.ioff()

    count = 1
    for i in range(0, 4):
        for j in range(i + 1, 5):
            fig = pylab.figure(count)
            ax = fig.add_subplot(111)
            pylab.plot(a[:,i], a[:,j], '+', color=col, markersize=marksize)
            plot_ellipse(a[:,i], a[:,j], ax, color=col)
            count += 1

def _plot_legend(flist, ext, location):
    pylab.legend([f.split('/')[-1].split(ext)[0] for f in flist], loc=location)

def plot_ellipse(x, y, ax, color):
	(xy, width, height, angle) = ellipse.get_ellipse(x, y)
	e = Ellipse(xy, width, height, angle)
	ax.add_artist(e)
	e.set_alpha(0.2)
	e.set_facecolor(color)
