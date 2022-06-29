![GitHub Workflow Status](https://raw.githubusercontent.com/cybergeek1943/badges/main/build-passing.svg) ![contributions welcome](https://raw.githubusercontent.com/cybergeek1943/badges/main/contributions-welcome.svg)

The t4json module was created to make working with [JSON](https://www.json.org/json-en.html) data in python easier. It provides a bunch of tools to seamlessly open, __edit__ and save JSON data. The tools provided by t4json have tons of features so that you can do really specific things... if you only want to read a few values from some flat simple json data you might as well use the standard json module.

This module should work on any installation of python 3.6
or later on any OS right out of the box.

Check out the ___docs___ [here](https://cybergeek1943.github.io/t4json/).

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


## Examples
### Loading the Data
Note - ( Each one of the examples below is all by itself. )
To load json data simply pass the data in when initializing the t4json object. Examples:

```python
data = T4Json('example.json')
```
OR
```python
data = T4Json('https://api.github.com/users?since=100')
```
OR
```python
json_data = """{
"name": "John"
"age": 67
"wealth": "above average"
"family": null
}"""
data = T4Json(json_data)
```
If you want to load json data later or have already loaded json data and want to load something else then just call one of the load methods like so - ```data.load("new_example.json")```.

If you want to start with a clean slate and create json data from scratch then:
```python
data = T4Json()
# start adding items here
```
By default, when creating new json data, the initial data is just an empty dictionary. If you want to specify the starting data to work with… pass it to the ```new()``` method:
```python
fresh_start = {'version': 1.0}
data = T4Json()
data.new(fresh_start)
# start adding items here
```
Note - ( The ```new()``` method will simply create an empty dictionary if nothing is passed to it. )

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
Note - ( The default path separator is '\\\\' - two back slashes - make sure that the fist backslash is not escaped by the second backslash. This can be done by prefixing the string with an 'r'. You can change the path separator properties using the ```set_path_separator_properties()``` method. )

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
### Flattening Nested Data
Flattening [nested data](https://en.wikipedia.org/wiki/Nesting_(computing)) is turning something like this ```[[1, 2, 3, [4, 5]], 6, 7, 8]``` into this ```[1, 2, 3, 4, 5, 6, 7, 8]```. Nested data can be flattened using the _T4Json_.```flatten()``` method. Below is an example of flattening some data from this [URL](https://mdn.github.io/learning-area/javascript/oojs/json/superheroes.json).

```python
>>> data = T4Json('https://mdn.github.io/learning-area/javascript/oojs/json/superheroes.json')
>>> data.flatten()
>>> data.read()
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

&emsp;

___

## Dependencies
The only third party dependency is the "request" module.

___

## Change Log - Latest major Fixes & Improvements

### v1.4.2
* Added ```types()``` method to T4Json instance.
* Added ```convert_singular_lists()``` method.
* Added **_convert_singular_lists_** parameter to ```flatten()``` method.
* The ```flatten()``` method should generally be up to 15% faster.
* The **_chain_key_include_index_** of the ```flatten()``` method was fixed/improved.
* Cleaned up code in internal methods.

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
