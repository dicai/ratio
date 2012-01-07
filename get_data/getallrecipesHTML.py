'''
getallrecipesHTML.py

Author: Diana Cai <dcai@eecs.harvard.edu>
Date: 09/26/11

Downloads html from Allrecipes.com for recipes of a category/search term

Arguments: category, path relative to script to save files, mode
    *category: e.g. category (e.g. cookie) or search term (e.g. tart)
    *path: path of category directory, will have subdirs such as /html/
        and /ingredient/
    *mode: 0 (category), 1 (search term), 2 (all recipes)
    *TEST_MODE: for testing purposes 0 false 1 true

Usage: python getallrecipesHTML.py cookies ../data/ 0 1
    gets the cookies category with TEST_MODE turned on.
'''
import sys
import os
import raw  # raw data library 

if len(sys.argv) is not 5:
    print 'Usage: python getallrecipesHTML.py category path mode TEST_MODE'
    sys.exit()

# mode to test code
TEST_MODE = False
if sys.argv[4] is 0:
    TEST_MODE = False
elif sys.argv[4] is 1:
    TEST_MODE = True
else:
    print 'Usage: python getallrecipesHTML.py category path mode TEST_MODE'


# arguments
category = str(sys.argv[1])
path = str(sys.argv[2])
mode = int(sys.argv[3])

# list of recipe names downloaded
print path
if path[-1:] is '/':
    records = open(os.path.join(path, category + '.txt'), 'w')
    path = path.strip('/')
else:
    records = open(path + '/records.txt', 'w')
recipe_names = {} # stores all the recipe names 

RECIPES_PER_PAGE = 20
LINK_ROOT = 'http://allrecipes.com/'

link = ''
desserts = ['candies', 'chocolate', 'cookies', 'cakes', \
        'custards-and-puddings', 'fruit-crumbles', 'mousse', \
        'pies', 'pralines', 'tiramisu', 'trifles']
breakfast = ['baked-goods', 'crepes', 'pancakes', 'french-toast', 'waffles']
link_bool = True
if mode == 0:
    if category in desserts:
        belongs = 'Desserts'
    elif category in breakfast:
        belongs = 'Breakfast-and-brunch'
    else:
        "Category not found...performing search"
        link_bool = False
    if link_bool:     
        link = LINK_ROOT + 'Recipes/' + belongs + '/' + category + \
                '/ViewAll.aspx'
    else:
        link = LINK_ROOT + 'Search/Recipes.aspx?WithTerm=' + category

# search term
if mode == 1:
    link_bool = False
    link = LINK_ROOT + 'Search/Recipes.aspx?WithTerm=' + category
# all recipes from website
if mode == 2:
    link = LINK_ROOT + 'ViewAll.aspx'

if link_bool:
    link += '?&Page='
else:
    link += '&SearchIn=All&Page='

# get first page and then number of pages needed to scrape
print link + '1'
os.system('curl "' + link + '1" > test.txt')
outfile = open('test.txt', 'r')
s = outfile.read()
outfile.close()

pages = s.split('Displaying 1-20 (of ')[1][0:10]
pages = pages.split(')')[0]

if ',' in pages:
    num_pages = int(pages.split(',')[0] + pages.split(',')[1])
else:
    num_pages = int(pages)

# divide total number of recipes over number on a page
num_pages = num_pages / RECIPES_PER_PAGE + 1

if TEST_MODE:
    num_pages = 2  # for testing purposes only

# iterate through all the pages and grab links to html
os.system('rm test.txt')
for i in range(1, num_pages):
    os.system('curl "' + link + str(i) + '" >> test.txt')
# parse file and get links 
if link_bool:
    grepstring =  "ctl00_CenterColumnPlaceHolder_rlvRecipes"
else:
    grepstring = "ctl00_CenterColumnPlaceHolder_RecipeList_rptRecipeList"
os.system('grep ' + grepstring + ' test.txt > grep.txt')
os.system('grep "span class=" grep.txt > g.txt')

grepfile = open('g.txt', 'r')
for line in grepfile:
    recipe_name = line.strip().split('"')[5].split('/')[4]
    if recipe_name not in recipe_names.keys():
        recipe_names[recipe_name] = LINK_ROOT + 'recipe/' + \
                recipe_name + '/detail.aspx'
        records.write(recipe_name + '\n')
        records.flush()
grepfile.close()
records.close()

if TEST_MODE:
    os.system('rm grep.txt')
    os.system('rm test.txt')
    os.system('rm g.txt')

# create appropriate directories
os.system("mkdir " + os.path.join(path, 'html'))
os.system("mkdir " + os.path.join(path, 'ing'))
os.system("mkdir " + os.path.join(path, 'raw'))
os.system("mkdir " + os.path.join(path, 'viz'))
os.system("rm " + os.path.join(path, 'html', category, '*'))
os.system("rmdir " + os.path.join(path, 'html', category))
os.system("mkdir " + os.path.join(path, 'html', category)) # make html folder
os.system("rm " + os.path.join(path, 'ing', category, '*')) 
os.system("rmdir " + os.path.join(path, 'ing', category))
os.system("mkdir " + os.path.join(path, 'ing', category)) # make ing folder
os.system("rm " + os.path.join(path, 'raw', category, '*'))
os.system("rmdir " + os.path.join(path, 'raw', category)) 
os.system("mkdir " + os.path.join(path, 'raw', category)) # make raw folder
os.system("rm " + os.path.join(path, 'viz', category, '*'))
os.system("rmdir " + os.path.join(path, 'viz', category))
os.system("mkdir " + os.path.join(path, 'viz', category)) # make viz folder

# now we have a dict recipe_names with all the recipe names/links
# we iterate through the keys and write the html out to the desired dir
# we also parse the html and write that out to an ingredients directory
category_out = os.path.join(path, 'raw', category, category + '.tsv')
for recipe in recipe_names.keys():
    html_out = os.path.join(path, 'html', category, recipe + '.html')
    ing_out = os.path.join(path, 'ing', category, recipe + '.txt')
    raw_out = os.path.join(path, 'raw', category, recipe + '.tsv')
    viz_out = os.path.join(path, 'viz', category, recipe + '.csv')
    recipe_link = recipe_names[recipe]
    os.system("curl " + recipe_link + ">" + html_out)

    # parse the html and write out to ingredients file
    recipe_html = open(html_out, 'r')
    ing_file = open(ing_out, 'w')

    line_mark = False
    for line in recipe_html:
        if '<div class="ingredients"' in line:
            line_mark = True
        if '</li>' in line.strip() and line_mark is True:
            ing_file.write(line.strip()[:-5] + '\n')
        if '</ul>' in line and line_mark is True:
            break
    recipe_html.close()
    ing_file.close()

    # now we want to take the parsed data and get our raw data
    raw.get_rawdata(ing_out, raw_out, 0) # mode 0 for allrecipes.com
    os.system("cat " + raw_out + " " + category_out + " > new")
    os.system("mv new " + category_out)

# append header
raw.add_header(category_out)

# lastly take raw data and get ellipse info for the visualizer
raw.get_ellipseinfo(category_out, viz_out)
