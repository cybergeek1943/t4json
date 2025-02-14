![GitHub Workflow Status](https://raw.githubusercontent.com/cybergeek1943/badges/main/build-passing.svg) ![contributions welcome](https://raw.githubusercontent.com/cybergeek1943/badges/main/contributions-welcome.svg)

The t4json module was created to make working with [JSON](https://www.json.org/json-en.html) data in python easier. It provides a bunch of tools to seamlessly open, __edit__ and save JSON data. The JSON data is first [deserialized](https://en.wikipedia.org/wiki/Serialization) and stored in an attribute of the T4Json class... this way you can work with the deserialized data directly... just as you would with the standard json module. The tools provided by t4json have tons of features so that you can do really specific things... if you only want to read a few values from some simple json data, then you might as well use the standard json module.

This module should work on any installation of python 3.6
or later on any OS right out of the box.

__Outline:__
- Open up json data from a file, URL/Endpoint, or string with the T4Json class.
- Use methods to make some changes.
- Save changes.
- That's it. Your done..

&emsp;

### Features

- Use paths to navigate the json data just like in the file system. Also includes relative/absolute path navigating.
- Easily make changes like changing the name of a key, changing a value, adding new items, moving/copying items to new locations, deleting items, flattening, and more. All with easy to use and intuitive methods.
- Easily open up json data - simply pass a File Path, URL, or Json String when creating the T4Json object, and it will automatically figure out what is what and give you the data you need to work with.
- And more.

T4json is designed to simply and easily work with json data without any hassle. It can be used to make simple quick changes, more complex changes, or to just retrieve data. All with only a few lines of code that are easy to understand and read.

&emsp;

### Installation

Using pip:

```pip install t4json```

Or just download the code from [GitHub](https://github.com/cybergeek1943/t4json) and use as a local module within your project… which may be more useful if you want to make changes to it.

Try to keep this package up to date... this project is under active development and with every update there can be much more improvement on the previous version.

&emsp;

### Notes
- Since v1.4.0, slicing operations are supported on T4Json instances. They can be used to delete, change and read values. Paths may also be used in the first slice to walk up a level. &emsp; Also, inplace/non-inplace adding and subtracting are supported for adding new items/pairs or removing items/pairs in bunches. &emsp; Iterating through T4Json instances is also now supported.
- All methods (where applicable) within the T4Json class will return un-copied mutable data. This is so that you can access the data and manipulate it just as you would if you were using the json module. You can use the built in ```copy()``` method of the returned mutable data to make a shallow copy… or you can use the copy module to make a deep copy. You can access the deserialized data through the ```data``` property of the T4Json class.
- Many of the methods and functions in t4json have a lot of arguments... So _key-word arguments_ may have to be used a lot of the time depending on what you are trying to do.
- Feel free to open it up and change some default arguments of the methods. If an argument looks like ```<parameter name>: <expected value> = None``` then that default argument needs to be changed with the attributes in the ```__init__()``` method of the T4Json class. __If__ the expected value/s has ```None``` in it like ```<parameter name>:<some expected value> | None = None```. In that case just change the default value of that parameter from ```None``` to something else if the arguments expected values allow it. Any 'flagged' T4Json methods or variables that look like ```__<name of method or var>__``` are not safe to tamper with as they are used by the T4Json class for processing the json data…

&emsp;

### Definitions/Terms
- Anything that holds data is called a **container**. Such as a dictionary or list
- A **pair** is short for a key/value pair or json object.
- A **value** is anything that has a corresponding key or index.
- A **key** is a string that is used to gain access to a value within a pair container.
- An **index** is an integer that is used to gain access to a value within a list container.
- An **item** is a non-pair __value__.
- A **pair container** is a dictionary.
- A **list container** is simply a list.
- If a path is an empty string ""… it is accessing the base container.

&emsp;

### JSON Conversion Table
Once you are done making changes/creating your json file… it needs to be [serialized](https://en.wikipedia.org/wiki/Serialization) / saved so that it can then be understood by other programs. For python to understand the JSON data it needs to be deserialized/loaded into a python data structure like a dictionary or list. Below are the tables used for that conversion process.

__Converting/Encoding to JSON:__

Python | t4json | JSON
-|-|-
dict | pair container | object
list/tuple | list container | array
str | <--------------> | string
int, float, int- & float-derived Enums | <--------------> | number
True | <--------------> | true
False | <--------------> | false
None | <--------------> | null



&emsp;

__Converting/Decoding from JSON to Python data structures:__

JSON | t4json | Python
-|-|-
object | pair container | dict
array | list container | list/tuple
string | <--------------> | str
number (int) | <--------------> | int
number (real) | <--------------> | float
true | <--------------> | True
false | <--------------> | False
null | <--------------> | None

&emsp;

### Overview of Global Functions

* ```multi_iter()```
* ```is_valid_json_data()```
* ```convert_to_valid_json_ready_data()```
* ```serialize_to_string()```
* ```deserialize_from_string```

&emsp;

### Overview of T4Json Class Methods
The parameters are not shown in the methods listed below.
&nbsp;

__Editing Methods__
* ```add()```
* ```chage_value()```
* ```change_key()```
* ```move_from_to()```
* ```copy_from_to()```
* ```delete()```
* ```delete_empty_containers()```
* ```convert_singular_lists()```
* ```new()```
* ```clear()``` / ```wipe()```
* ```format()```
* ```flatten()```

&emsp;

__Reading Methods__
* ```read()```
* ```multi_iter()```
* ```pair()```
* ```pairs()```
* ```key()```
* ```keys()```
* ```values()```
* ```all_pairs()```
* ```all_values()```
* ```all_keys()```
* ```search()```
* ```json_string()```

&emsp;

__Settings Methods__
* ```set_working_level()```
* ```set_indentation()```
* ```set_sort_keys()```
* ```set_only_ascii()```
* ```set_ignore_errors()```
* ```set_path_separator_properties()```
* ```set_json_separators()```
* ```set_path_separator_properties()```
* ```is_sorting_keys()```
* ```is_only_ascii()```
* ```is_ignoring_errors()```
* ```get_working_level()```
* ```get_indentation()```
* ```get_path_separator_properties()```
* ```get_known_objects_for_path()```
* ```reset_settings()```

&emsp;

__I/O Methods__
* ```load()```
* ```load_file()```
* ```load_from_string()```
* ```load_from_url()```
* ```load_object()```
* ```save()```
* ```save_as()```
* ```json_string()```
* ```close()```

&emsp;

__Other/Misc Methods__
* ```types()```
* ```pprint()```
* ```is_path_existent()```
* ```is_path_relative()```
* ```is_path()```

&emsp;

## T4Json Methods
The ```self``` parameter is omitted in the proceeding documentation.

Also, a parameter within most of the methods named ```ignore_errors``` has been omitted. What ```ignore_errors``` does is ignore non-critical errors such as the ```key```/```path``` to a value being incorrect.

___
#### Editing Methods:
###### _T4Json._ ```add(value, path='', existing_keys='pass', create=False, index=None, integrate_list_with_list=False)```
This method can be used to add new data anywhere in the json data.

___value___ This can be a dictionary of new pairs/s that you want to add to the current data, or it can be a __string__,  __integer__,  __float__,  __boolean__, __none__, __string__, or __list__.

___path___ leads to the location where the data will be added.

___existing_keys___ -  This parameter specifies what to do with keys that already exist on the current level. 
If set to "__pass__" then any key/s that already exists on the current level will be ignored. 
If set to "__replace__" then any key/s that already exist on the current level will have its value be replaced by the value of the new key/s. 
If set to "__combine__" then any key/s that already exist on the current level will have its value be combined with the value of the new key/s in a list.
If set to "__integrate__" then any key/s that already exist on the current level will have its value be integrated as best as possible with the value of the new key/s. If both the new and existing key/s have values that are containers… they will be integrated into ___one___ container.

___create___ when set to ```True``` a list will be created if ```path``` leads to a non-container item. This list will include the non-container item along with the new ```value```. Otherwise, if it is ```False``` it will raise an __```AddError```__.

___index___ when ```path``` leads to a __list__ and this argument is passed and integer… ```value``` will be inserted at the specified index. A string can also be passed to indicate where to place ```value```. It can be "center" (or "half"), "4q", "3q", "2q", "1q" or "0q" (The "q" stands for quarters)… or it can be a positive integer in a string that represents a proportional percentage/scale of where to place ```value```… with "0" being at the start and "100" being the end. When ```None``` is passed, ```value``` will be placed at the end of the list.

___integrate_list_with_list___ - If  ```path``` leads to a list and ```value``` is a list then both lists will be integrated into one list.


&emsp;
###### _T4Json._ ```change_value(path, new_value)```
This method can be used to change the value of a key anywhere in the json data.

___path___ leads to the key which holds the value you want to change.

___new_value___ is what you want to replace the old value with… It can be a __string__,  __integer__,  __float__,  __boolean__, __none__, __dictionary__, or __list__.


&emsp;
###### _T4Json._ ```change_key(path, new_key, existing_key='error')```
This method can be used to change the name of a key anywhere in the json data.

___path___ leads to the key that you want to change.

___new_key___ this is the new key… A __string__,  __integer__,  __float__,  __boolean__ or __none__ will be accepted but they of course will be converted to a __string__.

___existing_key___ -  This parameter specifies what to do if a key already exists on the current level. 
If set to "__pass__" then the key that already exists on the current level it will be ignored and nothing will change. 
If set to "__replace__" then the key that already exist on the current level will have its value be replaced by the value of the old key being changed. 
If set to "__combine__" then the key that already exist on the current level will have its value be combined with the value of the old key in a list.
If set to "__integrate__" then the key that already exist on the current level will have its value be integrated as best as possible with the value of the old key. If both the existing and old keys have values that are containers… they will be integrated into ___one___ container.
If set to "__error__" an ```ArgumentError``` will be raised if a key already exists on the current level.


&emsp;
###### _T4Json._ ```move_from_to(from_path, to_path, only_contents=False, existing_key='pass', create=False, index=None, integrate_list_with_list=False)```
This method can be used to move the specified data around inside the json data. If you try to move data further into itself an ```InvalidStructurePathError``` will be raised.

___from_path___ should lead to the key/json object of the data you want to move.

___to_path___ should lead to the location where the data will be moved.

___only_contents___ when set to ```True``` only the contents/value of the key/json object will be moved. Otherwise, if ```False``` the json object/key - value pair itself will be moved.

___existing_keys___ -  This parameter specifies what to do with keys that already exist on the current level. 
If set to "__pass__" then any key/s that already exists on the target level will be ignored.
If set to "__replace__" then any key/s that already exist on the target level will have its value be replaced by the value of the new key/s. 
If set to "__combine__" then any key/s that already exist on the target level will have its value be combined with the value of the new key/s in a list.
If set to "__integrate__" then any key/s that already exist on the target level will have its value be integrated as best as possible with the value of the new key/s. If both the new and existing key/s have values that are containers… they will be integrated into ___one___ container.

___create___ when set to ```True``` a list will be created if ```path``` leads to a non-container item. This list will include the non-container item along with the moved ```value```. Otherwise, if it is ```False``` it will raise an __```AddError```__.

___index___ when ```to_path``` leads to a __list__ and this argument is passed and integer… the _value_ from ```from_path``` will be inserted at the specified index. A string can also be passed to indicate where to place the _value_. It can be "center" (or "half"), "4q", "3q", "2q", "1q" or "0q" (The "q" stands for quarters)… or it can be a positive integer in a string that represents a proportional percentage/scale of where to place the _value_… with "0" being at the start and "100" being the end. When ```None``` is passed, the _value_ will be placed at the end of the list.

___integrate_list_with_list___ - If  ```to_path``` leads to a list and the _value_ from ```from_path``` is a list then both lists will be integrated into one list.


&emsp;
###### _T4Json._ ```copy_from_to(from_path, to_path, only_contents=False, overwrite_existing=False, create=False, index=None, integrate_list_with_list=False)```
This method can be used to copy the specified data to another location inside the json data.

___from_path___ should lead to the key/json object of the data you want to move.

___to_path___ should lead to the location where the data will be moved.

All the other arguments are the same as in ```move_from_to()```.


&emsp;
###### _T4Json._ ```delete(path)```
This method can be used to delete the specified data.

___path___ should lead to the pair/item you want to delete.


&emsp;
###### _T4Json._ ```convert_singular_lists(path)```
Converts all values on the current level that are lists containing only one item to the item that is inside that list.

___path___ should lead to the level in which you want to convert any singular lists to their one value.


&emsp;
###### _T4Json._ ```delete_empty_containers(path)```
This method can be used to delete any keys with empty containers as _values_.

___path___ should lead to the level in which you want to remove any __keys__ that have an empty container as __values__.


&emsp;
###### _T4Json._ ```new(start)```
This method can be used to start fresh. The difference between this method and ```load_object``` is that it replaces the data of the currently "opened" file... so that when you call ```save()``` the new data will be saved to the currently "opened" file.

___start___ can be a __dictionary__, __list__, __tuple__ (which will be converted to a list), __string__,  __integer__,  __float__,  __boolean__, or __none__. All current data will be overwritten/replaced with ```start```.


&emsp;
###### _T4Json._ ```clear()``` or ```wipe()```
Simply deletes everything and leaves you with an empty dictionary.


&emsp;
###### _T4Json._ ```format(indentation=4, sort_keys=True, only_ascii=False)```
This method formats the json file to make it look nice.

___indentation___ Sets the indentation amount of the json file.

___sort_keys___ Will sort all the keys in the json file in alphabetical and numerical order.

___only_ascii___ will escape any non-ASCII characters.


&emsp;
###### _T4Json._ ```flatten(path='', chain_keys=False, chain_key_separator='_', flatten_opposite_container_type=True, pull_pairs_from_lists=True, pull_lists_from_pairs=False, existing_keys='integrate', list_index=None, convert_singular_lists=True, delete_empty_containers=True)```
This method flattens nested data.

___path___ can be used to select which level you want to flatten.

___chain_keys___ when set to ```True``` the data will be flattened with all the keys being renamed to include there previous parents names.

__chain_key_separator__ - This is used as the separator between the keys as they are being renamed to include their previous parents names. ```chain_keys``` must be set to ```True``` for this argument to apply.

___flatten_opposite_container_type___ when set to ```True``` the opposite container type of the target one being flattened will also be flattened. For example: If you are flattening a pair container then all the list containers inside the pair container will also be flattened. Or if you are flattening a list container then all the pair containers within that list container will be flattened.

__pull_pairs_from_lists__ - If flatting a pair container… then any pair/s contained in lists will be pulled out and flattened. This will only work if ```flatten_opposite_container_type``` has been set to ```True```.

__pull_list_from_pairs__ - If flatting a list container… then any pair/s within that data that contain lists as values will be pulled out and flattened. This will only work if ```flatten_opposite_container_type``` has been set to ```True```.

___existing_keys___ -  This parameter specifies what to do with keys that already exist on the base level. 
If set to "__pass__" then any key/s that already exists on the base level will be ignored.
If set to "__replace__" then any key/s that already exist on the base level will have its value be replaced by the value of the new key/s. 
If set to "__combine__" then any key/s that already exist on the base level will have its value be combined with the value of the new key/s in a list.
If set to "__integrate__" then any key/s that already exist on the base level will have its value be integrated as best as possible with the value of the new key/s. If both the new and existing key/s have values that are containers… they will be integrated into ___one___ container.

___list_index___ when a _list_ is being flattened any nested contents will be pulled to the specified index. A string can also be passed to indicate where to place the _value_. It can be "center" (or "half"), "4q", "3q", "2q", "1q" or "0q" (The "q" stands for quarters)… or it can be a positive integer in a string that represents a proportional percentage/scale of where to place the _value_… with "0" being at the start and "100" being the end. When ```None``` is passed, the _value_ will be placed at the end of the list. If a nested _list_ is being flattened, and you want the contents to keep their positions than pass "hold".

___convert_singular_lists___ - When the flatting has finished, if this is set to ```True```, then any values that are lists and only contain one item will be converted to the item that is contained within themselves. This does the same thing as the ```convert_singular_lists()``` method.

___delete_empty_containers___ - Once the flatting is all done and dusted and if this is set to ```True``` then any keys with empty containers as values will be deleted.


&emsp;

&emsp;
___
#### Reading Methods:
###### _T4Json._ ```read(path='')```
Returns the value of wherever ```path``` leads.

___path___ Leads to the key that will have its value be returned.

&emsp;
###### _T4Json._ ```multi_iter(var_count=2, step=None, start_index=0, stop_index=None, include_uneven=False, uneven_placeholder=None, path: str = '', read_values_from_keys=False)```
This method makes it possible to loop multiple variables through the data in a ```for``` loop.

___var_count___ is the number of _variables_ that will be in the ```for``` loop.

___step___ is the number of _items_ you want to skip over when iterating. Which by default is ```None``` and is equivalent to being the same number that **_var_count_** is in order to sequentially iterate the variables through the data.

___start_index___ is the beginning index which is where the variables start iterating.

___start_index___ is the ending index which is where the variables stop iterating.

___include_uneven___ when set to ```True``` will add in filler values for the remaining _items_ in the _data_ if the _data_ is unevenly divided by the number of variables (**_var_count_**) being iterated through it. The default filler value is ```None```.

___uneven_placeholder___ is the _filler value_ when for when the _data_ is not evenly divided by the number variables (**_var_count_**) being iterated through it.

___path___ Leads to the data that will be iterated through.

___read_values_from_keys___ when set to ```True``` the **values** instead of the **keys** of mapping data will be iterated through.

&emsp;

Example:
```python
data = T4Json([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

for x, y, z in data.multi_iter(var_count=3):
    print(x, y, z)
```
Output:
```
1 2 3
4 5 6
7 8 9
10 11 12
```

&emsp;

&emsp;
###### _T4Json._ ```json_string(path='', indent=None, sort_keys=None, only_ascii=None, separators=None)```
Returns a json formatted string. This string can then… for example be saved to a file.

___path___ Leads to the key that will have its value be returned as a json formatted string.

___indent___ Can be an _Integer_, _String_, or _None_. If an _Integer_ is passed then the json will have its indentation set to the specified amount of whitespaces. If a _string_ is passed then it will be used as the indentation space. If _None_ is passed then there will be no indentation.

___sort_keys___ When ```True``` is passed the key will be sorted in alphabetical/numerical order.

___only_ascii___ When set to ```True``` any non-ascii characters will be escaped/encoded.

___separators___ Must be a tuple with two items. The fist is used to separate pairs or items. It is ", " by default. The second is used to separate key and values. It is ": " by default.


&emsp;
###### _T4Json._ ```pair(path, as_dictionary=False)```
Returns a pair in the form of a tuple (```key```, ```value```) or dictionary pair {```key```: ```value```} from wherever ```path``` leads.

___path___ Leads to the value that will be put in a __tuple__ along with its key.

__as_dictionary__ When ```True``` the target pair will be returned as dictionary - {```key```: ```value```}, otherwise it will be returned as a tuple - (```key```, ```value```).


&emsp;
###### _T4Json._ ```pairs(path='', as_dictionaries=False)```
Returns a __list__ of __tuples__ of (key, value) pairs - [(key, value), (key, value)..] of the selected level. This method is very similar to the ```items()``` method of ```dict```.

___path___ Leads to the key that will have its contents be returned in this format.

__as_dictionaries__ When set to ```False``` it will return all the pairs like so - (```key```, ```value```). If set to ```True``` they will be returned as - {```key```: ```value```}


&emsp;
###### _T4Json._ ```key(path)```
Returns the key of the value that ```path``` leads to. If the value is in a __list__ the values index will be returned as an __integer__.

___path___ Leads to the value that will have its key be returned.


&emsp;
###### _T4Json._ ```keys(path='')```
Returns a __list__ of all the of keys in the location that is specified by ```path```. If ```path``` leads to a non-container value than it will return the key of that value.

___path___ Leads to the container where the keys are.


&emsp;
###### _T4Json._ ```values(path='')```
Returns a __list__ of all the of values in the location that is specified by ```path```. If ```path``` leads to a non-container value than that value will simply be returned.

___path___ Leads to the key that will have its value be returned.


&emsp;
###### _T4Json._ ```all_pairs(path='', search_lists=True, as_dictionaries=False)```
Returns a __list__ of __tuples__ of all (key, value) pairs as - [(key, value), (key, value)..] past a point specified by ```path```.

___path___ Leads to the key that will have its contents be returned in this format.

__return_as_dictionaries__ When set to ```True``` will return all the pairs like so - {```key```: ```value```}. If set to ```False``` they will be returned as - (```key```, ```value```)

__search_lists__ When set to ```True``` will also search through lists for pairs.


&emsp;
###### _T4Json._ ```all_keys(path='', search_lists=True, as_paths: bool = False)```
Returns a __list__ of all the keys past a certain point which is specified by ```path```. This method only returns keys that have a non-container value

___path___ Leads to the container where all keys past itself will be returned.

__search_lists__ When set to ```True``` will also search through lists for keys.

__as_paths__ If set to ```True``` will return all the keys as paths to where they are in within the data.


&emsp;
###### _T4Json._ ```all_values(path='', search_lists=True)```
Returns a __list__ of all the of values in the location that is specified by ```path```. If ```path``` leads to a non-container value than that value will simply be returned.

___path___ Leads to the key that will have its value be returned.

__search_lists__ When set to ```True``` will also search through lists for values that have a corresponding key.


&emsp;
###### _T4Json._ ```search(key, path='', search_list=True)```
Searches through all the json data or (past a certain point specified by ```path```) for ```key```. If there are multiple keys with the same name spread throughout the data, a list of their all there values will be returned.

___path___ Leads to the key that will have its value be returned.

__search_lists__ When set to ```True``` will also search through lists for values that have a corresponding key.


&emsp;

&emsp;
___

#### Settings Methods:
###### _T4Json._ ```set_working_level(path='')```
Sets the working level within a nested data structure.

___path___ Leads to the level that will be set as the current working level. If path leads to a non-container value than its parent container will be selected as the current working level.


&emsp;
###### _T4Json._ ```set_indentation(indentation)```
Sets the indentation of the json file which will be applied when it is saved/serialized.

___indentation___ Can be an _Integer_, _String_, or _None_. If an _Integer_ is passed then the json will have its indentation set to the specified amount of whitespaces. If a _string_ is passed then it will be used as the indentation space. If _None_ is passed then there will be no indentation.


&emsp;
###### _T4Json._ ```set_sort_keys(boolean)```

___boolean___ When ```True``` is passed the key will be sorted in alphabetical/numerical order. This will be applied when the file is saved/serialized.



&emsp;
###### _T4Json._ ```set_only_ascii(boolean)```

___boolean___ When set to ```True``` any non-ascii characters will be escaped/encoded. This will be applied when the file is saved/serialized.



&emsp;
###### _T4Json._ ```set_ignore_errors(boolean)```

___boolean___ If ```True``` is passed then any non-critical errors (such as the path being incorrect) will be ignored.


&emsp;
###### _T4Json._ ```set_path_separator_properties(separator, relative, relative_back)```
Sets the path separator and relative path navigation properties.

___separator___ is the character/s used to separate the keys. It is "\\\\" by default.

__relative__ is the character/s used at the start of the path to signify that it is starting at the current working level. It is "." by default.

__relative_back__ is the character/s used at the start of the path to signify that it is starting at the current working level and going back up one level. There can be multiple relative back commands to go back up multiple levels before continuing with a normal path. __relative_back__ is ". ." by default.


&emsp;
###### _T4Json._ ```set_json_separators(item_separator, key_value_separator)```
Sets the pair and item separator properties for the json data when it is saved/serialized. The most compact arguments would be ("," and ":") instead of the default (", " and ": ").

___item_separator___ is used to separate pairs or items. It is ", " by default.

__pair_separator__ is used to separate key and values. It is ": " by default.


&emsp;
###### _T4Json._ ```set_known_objects_for_path(objects=None)```
Sets the objects that will be recognized as keys within paths.

___objects___ must be provided a list of objects to add to the known objects collection. If nothing is passed, and it is ```None```, then the known object collection will be reset to the default set of known objects.


&emsp;
###### _T4Json._ ```is_sorting_keys()```
Returns ```True``` if the keys are being sorted in alphabetical/numerical order. Otherwise, it returns ```False```.


&emsp;
###### _T4Json._ ```is_only_ascii()```
Returns ```True``` if all non-ascii characters are being escaped/encoded. Otherwise, it returns ```False```.


&emsp;
###### _T4Json._ ```is_ignoring_errors()```
Returns ```True``` if non-critical errors are being ignored. Otherwise, ```False``` is returned.


&emsp;
###### _T4Json._ ```get_working_level()```
Returns the current working level as a _path_.


&emsp;
###### _T4Json._ ```get_indentation()```
Returns the indentation property. An _Integer_, _String_ or _None_ can be expected.


&emsp;
###### _T4Json._ ```get_path_separator_properties()```
Returns the path separator properties in a tuple - (path separator, relative command, relative_back command)

&emsp;
###### _T4Json._ ```get_known_objects_for_path()```
Returns a list of the known objects that are recognized as keys within paths.

&emsp;
###### _T4Json._ ```reset_settings()```
Resets any settings that have been changed… back to their original default values.


&emsp;

&emsp;
___

#### I/O Methods:
__Note__ - ( A few parameters have been left out in the documentation below. The first is ```encoding``` and ```encoding_errors```/```errors```. These parameters are part of the built-in open() function. Check out the open() functions [docs](https://docs.python.org/3/library/functions.html#open) for more information. In addition ```decode_html_entities``` has also been left out. ```decode_html_entities``` just decodes any HTML [entities](https://www.freeformatter.com/html-entities.html)... by default it is set to ```False```.)


&emsp;

__Note__ - ( The ```__init__()``` for the T4Json class uses the same parameters as the ```load()``` method because it calls ```load()```. If you decide to not pass any data when initiating the T4Json class then you can call ```load()``` and it will do the same thing. )

&emsp;

&emsp;

###### _T4Json._ ```load(source, url_parameters=None, url_headers=None, url_body=None, url_user_auth=None, url_request_method='GET', url_raise_for_status=False, create=False)```
This method loads the json data. It can receive a *File Path*, *URL*, *JSON String*, *dict*, or *list*.

___source___ must be passed a string - File Path, URL/Endpoint, JSON String, Dict, or List.

___url_parameters___ must be passed a __dict__, __list__, or __bytes__ that contains the parameters that will be combined with the URL. Check out this [guide](https://pythonexamples.org/python-requests-send-parameters-in-url/)

___url_headers___ must be passed a __dict__ containing the HTTP headers. Check out this [guide](https://www.tutorialspoint.com/requests/requests_http_requests_headers.htm).

___url_body___ must be passed a JSON serializable object (usually a __dict__) containing the HTTP body that will be sent when the request is made.

___url_user_auth___ must be passed a __tuple__/__auth object__ used to authenticate a user using HTTP Basic/Digest/Custom Authentication or methods like OAuth. Check out the docs [here](https://docs.python-requests.org/en/latest/user/authentication).

___url_request_method___ must be passed a __string__ such as "GET", "POST", "PUT" or "DELETE".

___url_raise_for_status___ when set to ```True``` it will raise an error if response/status code is anything other than 200.

___create___ If you are attempting to load a file that does not exist and this parameter is set to ```True``` then the non-existent file will be created.


&emsp;
###### _T4Json._ ```load_file(file_path, create=False)```
Loads the Json data from a specified file.

___file_path___ must be passed a path that leads to the file you want to open.

___create___ If you are attempting to load a file that does not exist and this parameter is set to ```True``` then the non-existent file will be created.


&emsp;
###### _T4Json._ ```load_from_string(string)```
Loads Json data from a _string_.

___string___ must be passed a _String_ of serialized json data.



&emsp;
###### _T4Json._ ```load_from_url(url, parameters=None, headers=None, body=None, user_auth=None, request_method='GET', raise_for_status=False)```
Loads json data from the specified URL/Endpoint.

___url___ must be passed a URL/Endpoint that leads to the Json data you want to load.

___parameters___ must be passed a __dict__, __list__, or __bytes__ that contains the parameters that will be combined with the URL. Check out this [guide](https://pythonexamples.org/python-requests-send-parameters-in-url/)

___headers___ must be passed a __dict__ containing the HTTP headers. Check out this [guide](https://www.tutorialspoint.com/requests/requests_http_requests_headers.htm).

___body___ must be passed a JSON serializable object (usually a __dict__) containing the HTTP body that will be sent when the request is made.

___user_auth___ must be passed a __tuple__/__auth object__ used to authenticate a user using HTTP Basic/Digest/Custom Authentication or methods like OAuth. Check out the docs [here](https://docs.python-requests.org/en/latest/user/authentication).

___request_method___ must be passed a __string__ such as "GET", "POST", "PUT" or "DELETE".

___raise_for_status___ when set to ```True``` it will raise an error if response/status code is anything other than 200.

This functionality comes from the "requests" package. If you are not familiar with the [request](https://docs.python-requests.org/en/latest/) package you may want to look into it before using these features. Here is a good [guide](https://www.nylas.com/blog/use-python-requests-module-rest-apis/) on working with APIs using the requests module.


&emsp;
###### _T4Json._ ```load_object()```
Receives a __dict__ or __list__ and loads it. This way you could load a dictionary work with it... and then save it.


&emsp;
###### _T4Json._ ```save(indent=None, sort_keys=None, only_ascii=None, separators=None)```
Saves the currently opened file if a file has already been opened.

___indent___ Can be an _Integer_, _String_, or _None_. If an _Integer_ is passed then the json will have its indentation set to the specified amount of whitespaces. If a _string_ is passed then it will be used as the indentation space. If _None_ is passed then there will be no indentation.

___sort_keys___ When ```True``` is passed the key will be sorted in alphabetical/numerical order.

___only_ascii___ When set to ```True``` any non-ascii characters will be escaped/encoded.

___separators___ Must be a tuple with two items. The fist is used to separate pairs or items. It is ", " by default. The second is used to separate key and values. It is ": " by default.


&emsp;
###### _T4Json._ ```save_as(file_path, overwrite=False, indent=None, sort_keys=None, only_ascii=None, separators=None)```
Save the JSON data as a new file.

___file_path___ Is the new file name which can include a path to wherever you want to place it.

___overwrite___ When set to ```True``` and ```file_path``` already exist then the already existing file will have its contents overwritten.

___indent___ Can be an _Integer_, _String_, or _None_. If an _Integer_ is passed then the json will have its indentation set to the specified amount of whitespaces. If a _string_ is passed then it will be used as the indentation space. If _None_ is passed then there will be no indentation.

___sort_keys___ When ```True``` is passed the key will be sorted in alphabetical/numerical order.

___only_ascii___ When set to ```True``` any non-ascii characters will be escaped/encoded.

___separators___ Must be a tuple with two items. The fist is used to separate pairs or items. It is ", " by default. The second is used to separate key and values. It is ": " by default.


&emsp;
###### _T4Json._ ```json_string(path='', indent=None, sort_keys=None, only_ascii=None, separators=None)```
Returns a json formatted string. This string can then.. for example be saved to a file.

___path___ Leads to the key that will have its value be returned as a json formatted string.

___indent___ Can be an _Integer_, _String_, or _None_. If an _Integer_ is passed then the json will have its indentation set to the specified amount of whitespaces. If a _string_ is passed then it will be used as the indentation space. If _None_ is passed then there will be no indentation.

___sort_keys___ When ```True``` is passed the key will be sorted in alphabetical/numerical order.

___only_ascii___ When set to ```True``` any non-ascii characters will be escaped/encoded.

___separators___ Must be a tuple with two items. The fist is used to separate pairs or items. It is ", " by default. The second is used to separate key and values. It is ": " by default.


&emsp;
###### _T4Json._ ```close()```
Simply closes the data that's already open and leaves you with an empty dictionary.

&emsp;

&emsp;
___

#### Other/Misc Methods:


###### _T4Json._ ```types(path='')```
Returns a __set__ of all the types on the current level (as defined by ***path***). If the current level is a dictionary than the types of all the values will be in the returned __set__.

It can be used to check if a specific data type is on the current level. For example:
```python
>>> instance = T4Json([16, 'abc', 3.14])
>>> int in instance
True
>>> str in instance
True
>>> tuple in instance
False
```


&emsp;
###### _T4Json._ ```pprint(path='', indent=1, print_to_console=True)```
Note - it is not necessary to call this method if you just want to only view the data. You can simply print the instance of the T4Json class you would like to view. 

___path___ can lead to the level that you want to print.

___indent___ must be passed an integer. This specifies the amount of indentation you would like.

___print_to_console___ when set to ```True``` will print it to the console. If set to ```False```, this method will only return the string that was going to be printed.


&emsp;
###### _T4Json._ ```is_path_existent(path)```
Checks to see if ___path___ exist in the currently opened data structure. ```True``` is return if it does exist… and ```False``` otherwise.


&emsp;
###### _T4Json._ ```is_path_relative(path)```
Checks to see if ___path___ is a relative path. ```True``` is returned if it is… and ```False``` otherwise.


&emsp;
###### _T4Json._ ```is_path(path)```
Checks to see if ___path___ is considered a path in the current T4Json instance.


&emsp;

&emsp;
___

## Global Functions


###### _T4Json._ ```multi_iter(data, var_count=2, step=None, start_index=0, stop_index=None, include_uneven=False, uneven_placeholder=None, path: str = '', read_values_from_keys=False)```
This function makes it possible to loop multiple variables through _data_ in a ```for``` loop.

___data___ is the data that you want to loop through. You can pass a _list_, _tuple_, _str_, _T4Json_, _dict_, _set_, or _frozenset_.

___var_count___ is the number of _variables_ that will be in the ```for``` loop.

___step___ is the number of _items_ you want to skip over when iterating. Which by default is ```None``` and is equivalent to being the same number that **_var_count_** is in order to sequentially iterate the variables through the data.

___start_index___ is the beginning index which is where the variables start iterating.

___start_index___ is the ending index which is where the variables stop iterating.

___include_uneven___ when set to ```True``` will add in filler values for the remaining _items_ in the _data_ if the _data_ is unevenly divided by the number of variables (**_var_count_**) being iterated through it. The default filler value is ```None```.

___uneven_placeholder___ is the _filler value_ when for when the _data_ is not evenly divided by the number variables (**_var_count_**) being iterated through it.

___read_values_from_keys___ when set to ```True``` the **values** instead of the **keys** of mapping data will be iterated through.

&emsp;

Example:
```python
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

for x, y, z in multi_iter(data, var_count=3):
    print(x, y, z)
```
Output:
```
1 2 3
4 5 6
7 8 9
10 11 12
```

&emsp;

&emsp;
###### ```is_valid_json_data(source)```
This function returns ```True``` if the JSON data is valid. Otherwise, it returns ```False```.

___source___ must be passed a string - File Path, URL, or JSON String.


&emsp;
###### ```convert_to_valid_json_ready_data(value)```
Converts _value_ into json ready data. It will remove any unsupported keys and convert the keys that are not string into strings.

___value___ must be passed a _dictionary_, _list_, _tuple_ or any other basic type of python data.


&emsp;
###### ```serialize_to_string(value, indent=None, sort_keys=None, only_ascii=None, separators=None)```
Returns a json formatted string from _value_. This string can then.. for example be saved to a file.

___value___ must be passed a _dictionary_, _list_, _tuple_ or any other basic type of python data.

___indent___ Can be an _Integer_, _String_, or _None_. If an _Integer_ is passed then the json will have its indentation set to the specified amount of whitespaces. If a _string_ is passed then it will be used as the indentation space. If _None_ is passed then there will be no indentation.

___sort_keys___ When ```True``` is passed the key will be sorted in alphabetical/numerical order.

___only_ascii___ When set to ```True``` any non-ascii characters will be escaped/encoded.

___separators___ Must be a tuple with two items. The fist is used to separate pairs or items. It is ", " by default. The second is used to separate key and values. It is ": " by default.


&emsp;
###### ```deserialize_from_string(string)```
Loads Json data from a _string_ and returns the python data structure.

___string___ must be passed a _String_ of serialized json data.


&emsp;

&emsp;
___

## Slicing Operations
Data in T4Json instances can be edited using slicing operations. This can be really useful if you don't want to use the _T4Json_.methods().

Reading:
```python
>>> data = T4Json({'phone': {'area': 503, 'middle': 464, 'last': 9787}})
>>> data['phone']['area']
501
```

Adding / Changing:
```python
>>> data = T4Json({'phone': {'area': 503, 'middle': 464, 'last': 9787}})
>>> data['phone']['area'] = [5, 0, 3]
>>> data
{'phone': {'area': [5, 0, 3], 'middle': 464, 'last': 9787}}
```

Deleting:
```python
>>> data = T4Json({'phone': {'area': 503, 'middle': 464, 'last': 9787}})
>>> del data['phone']['area']
>>> data
{'phone': {'middle': 464, 'last': 9787}}
```

We can also use paths within our slices (if it is the first slice) to easily access deep levels (using relative paths, if needed). For example:

```python
>>> starting_data = {
...     "internet": {
...         "airplane mode": False,
...         "wifi": [True, {"known": ["home", "office"]}],
...         "wifi calling": False,
...         "mobile hotspot": False}
... }
>>> 
>>> data = T4Json(starting_data)
>>> data.set_working_level(r'internet\\wifi\\1')
>>> data[r'..\\..']['wifi'] = 404
>>> data
{
    "internet": {
        "airplane mode": False,
        "wifi": 404,
        "wifi calling": False,
        "mobile hotspot": False
    }
}
```


&emsp;

&emsp;
___

## Examples
### Loading the Data
To load json data simply pass the data in when initializing the t4json object.

Loading a **File**:
```python
data = T4Json('example.json')
```
Loading from a **URL/Endpoint**:
```python
data = T4Json('https://api.github.com/users?since=100')
```
Loading from a **string**:
```python
json_data = """{
"name": "John"
"age": 67
"wealth": "above average"
"family": null
}"""
data = T4Json(json_data)
```
Loading from a **dict/list**:
```python
dictionary = {'new_data': 512}
data = T4Json(dictionary)
```
If you want to load new data into the same T4Json instance after you have already loaded data - ```data.load("new_example.json")```.

If you want to start with a clean slate and create json data from scratch then:
```python
data = T4Json()
# start adding items here
```


&emsp;

&emsp;
### Using Paths to Navigate the Data
Note - ( This section assumes familiarity with absolute/relative paths within the file system. )
Once the data is loaded you can navigate it using paths - similar to a file/directory path. If you are working in some nested part of the data then you can set that as the current working level to make it easier to read/edit the data in there. For example:
Here is the json data in a file we will call ```settings.json```:
```json
{
  "internet": {
      "airplane mode": false,
      "wifi": [true, {"known": ["home", "office"]}],
      "wifi calling": false,
      "mobile hotspot": false,
      "mobile data": false
  },
  "bluetooth": [true, {"paired": ["headphones", "laptop"]}],
  "sound": {
    "volume": 65, "vibration": true,
    "ringtone": "guitar", "notification": "ping"
  },
  "display": {
    "brightness": {"auto": true, "level": 80},
    "wallpaper": "trees",
    "navigation bar": "gesture",
    "font": 70,
    "timeout time": 30
  }
}
```
Note - ( The default path separator is '\\' - two back slashes - make sure that the fist backslash is not escaped by the second backslash. This can be done by prefixing the string with an 'r' or by using '\\\\' as the seperator. You can change the path separator properties using the ```set_path_separator_properties()``` method. )

Here is some code being run in the terminal using paths to navigate the data. It shows the difference between absolute vs relative paths. 

Absolute:
```python
>>> data = T4Json('hero_file.json')
>>> data.read(r'display\\brightness\\auto')
True
>>> data.read(r'internet\\wifi\\1\\known')
['home', 'office']
>>> data.read(r'display\\brightness\\level')
80
>>> data.read('sound')
{'volume': 65, 'vibration': True, 'ringtone': 'guitar', 'notification': 'ping'}
```

Relative:
```python
>>> data.set_working_level(r'internet\\wifi\\1')
>>> data.read(r'.\\known\\0')
home
>>> data.read(r'.\\known')
['home', 'office']
>>> data.read(r'..\\0')
True
>>> data.read(r'..\\..\\..\\bluetooth\\1\\paired')
['headphones', 'laptop']
>>> data.read(r'..\\..\\..\\sound\\volume')
65
>>> data.read(r'..\\..\\..\\display\\brightness')
{'auto': True, 'level': 80}
```

Note - (There can be a separator at the beginning of the path if you want it. Sometimes it may be necessary to do that if there is a key that is an empty string "". This is because an empty string "" is used to access the base level. So both ```\\formed``` and ```formed``` would be the same thing.)
Using these relative paths we not only can read but can do all sorts of edits easily and without the hassle of always having to walk down the path of nested data.


&emsp;

&emsp;
### Searching the Data
You can search the data for a specific key if the keys value is not a pair container. We will use this [URL](https://mdn.github.io/learning-area/javascript/oojs/json/superheroes.json) as an example:

```python
>>> data = T4Json('https://mdn.github.io/learning-area/javascript/oojs/json/superheroes.json')
>>> data.search('powers')
```
Look at the json data from the [URL](https://mdn.github.io/learning-area/javascript/oojs/json/superheroes.json) and see how it looks compared to the searched data below.
```json
[
    "Radiation resistance", 
    "Turning tiny", 
    "Radiation blast", 
    "Million tonne punch", 
    "Damage resistance", 
    "Superhuman reflexes", 
    "Immortality", 
    "Heat Immunity", 
    "Inferno", 
    "Teleportation", 
    "Interdimensional travel"
]
```


&emsp;

&emsp;
### Flattening Nested Data
Flattening [nested data](https://en.wikipedia.org/wiki/Nesting_(computing)) is turning something like this ```[[1, 2, 3, [4, 5]], 6, 7, 8]``` into this ```[1, 2, 3, 4, 5, 6, 7, 8]```. Nested data can be flattened using the _T4Json_.```flatten()``` method. 

There are basically, two different ways that T4Json data can be flattened:
1. **Grounding:** All the kay/value pairs (that do not contain containers as values) are moved to the base level. Any key/value pairs that have the same keys get their values combined or replaced.
2. **Chaining:** All the keys get chained togather. The values (that are not containers) remain the same.


&emsp;
#### Grounding:
We will be using the data from this [URL](https://mdn.github.io/learning-area/javascript/oojs/json/superheroes.json) as example data.

```python
>>> data = T4Json('https://mdn.github.io/learning-area/javascript/oojs/json/superheroes.json')
>>> data.flatten()
>>> data
```
Look at the original json data from the [URL](https://mdn.github.io/learning-area/javascript/oojs/json/superheroes.json) and compare it with the flattened data below.
```json
{
    "squadName": "Super Hero Squad", 
    "homeTown": "Metro City", 
    "formed": 2016, 
    "secretBase": "Super tower", 
    "active": true, 
    "name": [
        "Molecule Man", 
        "Madame Uppercut", 
        "Eternal Flame"
    ], 
    "age": [
        29, 
        39, 
        1000000
    ], 
    "secretIdentity": [
        "Dan Jukes", 
        "Jane Wilson", 
        "Unknown"
    ], 
    "powers": [
        "Radiation resistance", 
        "Turning tiny", 
        "Radiation blast", 
        "Million tonne punch", 
        "Damage resistance", 
        "Superhuman reflexes", 
        "Immortality", 
        "Heat Immunity", 
        "Inferno", 
        "Teleportation", 
        "Interdimensional travel"
    ]
}
```


&emsp;
#### Chaining:
We will be using this data as an example:
```json
{
  "internet": {
      "airplane mode": false,
      "wifi": [true, {"known": ["home", "office"]}],
      "wifi calling": false,
      "mobile hotspot": false
  },
  "bluetooth": [true, {"paired": ["headphones", "laptop"]}],
  "sound": {
    "volume": 65, "vibration": true,
    "ringtone": "guitar", "notification": "ping"
  },
  "display": {
    "brightness": {"auto": true, "level": 80},
    "wallpaper": "trees",
    "navigation bar": "gesture",
    "font": 70,
    "timeout time": 30
  }
}
```

We will then run the fallowing code to flatten the data:
```python
>>> data = T4Json('example.json')
>>> data.flatten(chain_keys=True)
>>> data
```

And here is the result:
```json
{
  "bluetooth": [true],
  "internet_airplane mode": false,
  "internet_wifi": [true],
  "internet_wifi calling": false,
  "internet_mobile hotspot": false,
  "sound_volume": 65,
  "sound_vibration": true,
  "sound_ringtone": "guitar",
  "sound_notification": "ping",
  "display_wallpaper": "trees",
  "display_navigation bar": "gesture",
  "display_font": 70,
  "display_timeout time": 30,
  "bluetooth_paired": ["headphones", "laptop"],
  "internet_wifi_known": ["home", "office"],
  "display_brightness_auto": true,
  "display_brightness_level": 80
}
```
Note - when there is only one item in a list such as ```{"bluetooth": [true]}``` from above, you can set the parameter ```convert_singular_lists``` of the ```flatten()``` method to ```True``` and the output will be ```{"bluetooth": true}``` instead of ```{"bluetooth": [true]}```.


&emsp;

&emsp;

___

## Dependencies
The only third party dependency is the "request" module.

___

## Change Log - Latest Fixes & Improvements

### v1.4.3
* Added ```multi_iter()``` method to T4Json instance so that multiple variables can be looped through the data at the same time.
* Also added ```multi_iter()``` as a global function.
* Cleaned up code and made it just a bit faster.
* The dunder methods of the T4Json class were improved.

### v1.4.2
* Added ```types()``` method to T4Json instance.
* Added ```convert_singular_lists()``` method.
* Added **_convert_singular_lists_** parameter to ```flatten()``` method.
* The ```flatten()``` method should generally be up to 15% faster.
* The **_chain_key_include_index_** of the ```flatten()``` method was fixed/improved.
* Cleaned up code in internal methods.

### v1.4.1
* Added support for re-calling T4Json instances to load new data.
* Changed the ```chain_key``` parameter to ```chain_keys``` within the ```flatten()``` method.

### v1.4.0
* Slicing Operations now supported on T4Json instances.
* Support for adding and subtracting items or pairs to/from T4Json instances.
* Support for iterating through a T4Json instance.
* Support for getting the length of a T4Json instance - (number of all the pairs/items on the first level).
* Support for checking equality (of data) between two T4Json instances.
* Support for checking in-equality (number of all the pairs/items on the first level) between two T4Json instances.
* Default support for printing a T4Json instance.
* Adding a pretty print method.
* Cleaned up code.

### v1.3.3
* Greatly improved the error messages.
* Fixed ___t4json___.```save()``` method.
* Improved ___t4json___.```load()```&```load_file()```&```load_from_url()```&```load_from_string()```
* Added ___t4json___.```load_object()``` for loading python objects.
* Added new parameters to ___t4json___.```load_from_url()``` for making ```POST``` (and others) requests. Also added support for headers and body.
* Improved walking up levels in nested data using paths.
* Improved support for key paths to work with non-string objects that are keys.
* Cleaned up code in general.

___

## Roadmap
* Build better search algorithms.
* Improve Documentation & move it to a better/more-organized website.
* Make even more improvements on error messages.
* Improve the __docstrings__

___

## License

__MIT__
Copyright (c) 2022 Isaac Wolford

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contact
Email: cybergeek.1943@gmail.com
