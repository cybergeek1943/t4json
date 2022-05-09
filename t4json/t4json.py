# __/\\\\\\\\\\\\\\\____________/\\\_________/\\\\\\\\\\\__________________________________________
#  _\///////\\\/////___________/\\\\\________\/////\\\///___________________________________________
#   _______\/\\\______________/\\\/\\\____________\/\\\______________________________________________
#    _______\/\\\____________/\\\/\/\\\____________\/\\\______/\\\\\\\\\\_____/\\\\\_____/\\/\\\\\\___
#     _______\/\\\__________/\\\/__\/\\\____________\/\\\_____\/\\\//////____/\\\///\\\__\/\\\////\\\__
#      _______\/\\\________/\\\\\\\\\\\\\\\\_________\/\\\_____\/\\\\\\\\\\__/\\\__\//\\\_\/\\\__\//\\\_
#       _______\/\\\_______\///////////\\\//___/\\\___\/\\\_____\////////\\\_\//\\\__/\\\__\/\\\___\/\\\_
#        _______\/\\\_________________\/\\\____\//\\\\\\\\\_______/\\\\\\\\\\__\///\\\\\/___\/\\\___\/\\\_
#         _______\///__________________\///______\/////////_______\//////////_____\/////_____\///____\///__
import json
from requests.auth import AuthBase, HTTPBasicAuth, HTTPDigestAuth, HTTPProxyAuth
from typing import Any


class T4Json:

    __slots__: tuple = (
        '__file_path__', 'ignore_method_errors', 'indentation', 'sort_keys', 'only_ascii', '__known_objects_for_path__',
        '__json_separators__', '__path_separator__', '__relative_path_command__', '__relative_back_path_command__',
        '__working_level__', '__root__', '__data__')

    def __init__(self, source: str or bytes or dict or list = None, url_parameters: dict or list or bytes = None,
                 url_headers: dict = None, url_body: Any = None, url_user_auth: Any = None,
                 url_request_method: str = 'GET', url_raise_for_status: bool = False, create: bool = False,
                 encoding: str = 'utf-8', encoding_errors: str = 'ignore', decode_html_entities: bool = False):
        self.__file_path__: str or None = None  # used throughout the class to open, write and read to JSON files

        # user_settings
        self.ignore_method_errors: bool = False
        self.indentation: int or str or None = 4
        self.sort_keys: bool = False
        self.only_ascii: bool = False

        # off limit __vars__
        self.__known_objects_for_path__: dict = {'bool': bool, 'int': int, 'float': float, 'complex': complex,
                                                 'list': list, 'tuple': tuple, 'frozenset': frozenset,
                                                 'set': set, 'dict': dict, 'str': str, 'object': object, }
        self.__json_separators__: tuple = (', ', ': ')  # index 0 is for items and index 1 is fore pairs keys and values
        self.__path_separator__: str = '\\\\'
        self.__relative_path_command__: str = '.'
        self.__relative_back_path_command__: str = '..'
        self.__working_level__: str = ''
        self.__root__: str = ''

        self.__data__: dict = {self.__root__: {}}

        if source is not None:
            self.load(source=source, url_parameters=url_parameters, url_headers=url_headers, url_body=url_body,
                      url_request_method=url_request_method, url_raise_for_status=url_raise_for_status,
                      url_user_auth=url_user_auth, create=create, encoding=encoding, encoding_errors=encoding_errors,
                      decode_html_entities=decode_html_entities)

    def __str__(self) -> str:
        return self.pprint(print_to_console=False)

    def add(self, value: dict or list or str or float or int or bool or None, path: str = '', existing_keys: str = 'replace', create: bool = False, index: int or str or None = None, integrate_list_with_list: bool = False, ignore_errors: bool = None) -> 'T4Json':
        """Adds *value* to the base... or elsewhere if specified by *path*."""

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors

        # main
        try:
            data_: tuple = self.__walk_path__(path=path, ignore_path_errors=ignore_errors)
            data: dict or list or str or float or int or bool or None = data_[0][data_[1]]
            if isinstance(data, dict):
                if existing_keys == 'replace':
                    data.update(value)
                elif existing_keys == 'pass':
                    for k, v in value.items():
                        data.setdefault(k, v)
                elif existing_keys == 'combine':
                    duplicates: dict = {}
                    for k, v in value.items():
                        if k in data:
                            duplicates.update({k: v})
                        else:
                            data.update({k: v})
                    for k in duplicates:
                        if not isinstance(data[k], list):
                            self.change_value(f'{path}{self.__path_separator__}{k}', [data[k], duplicates[k]])
                        else:
                            self.add(value=duplicates[k], path=f'{path}{self.__path_separator__}{k}',
                                     existing_keys=existing_keys, create=True, index=index, integrate_list_with_list=False, ignore_errors=ignore_errors)
                elif existing_keys == 'integrate':
                    duplicates: dict = {}
                    for k, v in value.items():
                        if k in data:
                            duplicates.update({k: v})
                        else:
                            data.update({k: v})
                    for k in duplicates:
                        self.add(value=duplicates[k], path=f'{path}{self.__path_separator__}{k}',
                                 existing_keys=existing_keys, create=True, index=index, integrate_list_with_list=True, ignore_errors=ignore_errors)
                else:
                    self.__raise_error__(ArgumentError('<existing_pairs> must be equal to "pass", "replace", "combine" or "integrate".'), ignore_errors)
                    self.add(value, path, create=create, index=index, integrate_list_with_list=True,
                             ignore_errors=ignore_errors)  # recursive step
            else:
                if index is None:
                    if integrate_list_with_list and isinstance(value, list):
                        data.extend(value)
                    else:
                        data.append(value)
                else:
                    if isinstance(index, str):
                        if index.isdigit():
                            index: int = (len(data) / 100 * int(index)).__floor__()
                        elif index in ('center', 'half', '2q'):
                            index: int = len(data) // 2
                        elif index == '3q':
                            index: int = (len(data) / 100 * 75).__floor__()
                        elif index == '1q':
                            index: int = (len(data) / 100 * 25).__floor__()
                        elif index == '0q':
                            index: int = 0
                        elif index == '4q':
                            index: None = None
                        else:
                            self.__raise_error__(error=ArgumentError(
                                'If <index> is a string it must be - "center", "half", "0q", "1q", "2q", "3q", "4q '
                                'or a positive integer within a string that represents a percentage of where to '
                                'place the <value>."'), ignore=ignore_errors)
                            index: None = None
                    if integrate_list_with_list and isinstance(value, list):
                        if index is None:
                            data.extend(value)
                        else:
                            data[index:index] = value
                    else:
                        data.insert(index, value)

            return self
        except (AttributeError, TypeError):
            if create:
                if path == '':
                    self.__data__[self.__root__] = [self.__data__[self.__root__]]
                    self.add(value=value, path='', existing_keys=existing_keys, create=create, index=index,
                             integrate_list_with_list=integrate_list_with_list, ignore_errors=ignore_errors)
                else:
                    self.change_value(path, [self.read(path=path)])
                    self.add(value=value, path=path, existing_keys=existing_keys, create=create, index=index,
                             integrate_list_with_list=integrate_list_with_list, ignore_errors=ignore_errors)
            else:
                self.__raise_error__(AddError, ignore_errors)

    def change_value(self, path: str, new_value: dict or list or str or float or int or bool or None,
                     ignore_errors: bool = None) -> 'T4Json':
        """Changes the value of the key/index that *path* leads to."""
        data: tuple = self.__walk_path__(path=path, ignore_path_errors=ignore_errors)
        data[0][data[1]] = new_value

        if self.is_path_relative(path):
            path: str = self.__interpret_path__(path, return_as_str=True)  # in-case <path> is relative
        if self.__working_level__.startswith(path):
            if self.__path_separator__ in path:
                self.set_working_level(self.__path_separator__.join(path.split(self.__path_separator__)[:-1]))
            else:
                self.set_working_level(path='')

        return self

    def change_key(self, path: str, new_key: str or int or float or bool or None, existing_key: str = 'error',
                   ignore_errors: bool = None) -> 'T4Json':
        """Changes the key that *path* leads to."""

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors
        if path == '':
            self.__raise_error__(error=KeyPathError('<path> must be/(lead to) a key.'), ignore=ignore_errors)
            return self
        if self.is_path_relative(path):
            path: str = self.__interpret_path__(path, return_as_str=True)
        new_key: str = str(new_key)

        # main
        try:
            if not (path.endswith(self.__path_separator__ + new_key) or path == new_key):
                data: tuple = self.__walk_path__(path=path)

                if new_key not in data[0]:
                    data[0][new_key] = data[0].pop(data[1])  # replaces key in dict with new key while keeping the value

                    if self.__working_level__.startswith(path):  # TODO: test this
                        new_working_level = self.__working_level__.split(self.__path_separator__)
                        new_working_level[len(path.split(self.__path_separator__)) - 1] = new_key
                        self.set_working_level(path=self.__path_separator__.join(new_working_level))

                else:  # if a key does already exist with the same name
                    if existing_key in ('combine', 'integrate', 'replace', 'pass'):

                        if self.__path_separator__ in path:
                            new_path: str = self.__interpret_path__(
                                f'{self.__relative_back_path_command__}{self.__path_separator__}{new_key}',
                                working_level=path, return_as_str=True)
                        else:
                            new_path: str = new_key

                        if existing_key == 'combine':
                            self.change_value(path=new_path, new_value=[self.read(path=new_path), self.read(path=path)])
                        elif existing_key == 'integrate':
                            self.add(value=data[0][data[1]], path=new_path, existing_keys='integrate', integrate_list_with_list=True, create=True)
                        elif existing_key == 'replace':
                            self.change_value(path=new_path, new_value=self.read(path=path))
                        elif existing_key == 'pass':
                            return self

                        if self.__working_level__.startswith(new_path) or self.__working_level__.startswith(path):
                            self.set_working_level(path=new_path)

                        self.delete(path)
                    elif existing_key == 'error':
                        self.__raise_error__(ArgumentError('\n\n<new_key> is already being used on this level.'
                                                           '\n\nSet the <existing_key> argument to "combine" so that '
                                                           'the values will be combined into a list.\nSet the '
                                                           '<existing_key> argument to "integrate" so that the values '
                                                           'will be integrated with each other.\nSet the '
                                                           '<existing_key> argument to "replace" so that that the '
                                                           'key that already exists will have its value be replaced.'
                                                           '\nSet the <existing_key> argument to "pass" so that that '
                                                           'the key that already exists will have its value be '
                                                           'replaced by the key being renamed.'), ignore_errors)
                    else:
                        self.__raise_error__(ArgumentError('<existing_pair> argument must be equal to "combine", '
                                                           '"integrate", "replace", "pass" or "error".'), ignore_errors)

            return self
        except (IndexError, TypeError):
            self.__raise_error__(
                IndexError('The path you entered leads to a list... Use a path that leads to a JSON object/dict pair.'),
                ignore_errors)

    def move_from_to(self, from_path: str, to_path: str, only_contents: bool = False, existing_keys: str = 'combine',
                     create: bool = False, index: int or str or None = None, integrate_list_with_list: bool = False,
                     ignore_errors: bool = None) -> 'T4Json':
        """Moves data from *from_path* to *to_path*."""

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors

        # functions
        def delete(path: str) -> tuple or None:
            """For <self.move_from_to()> the output of this func must always
            be in the format of: (<value>, <key>, <parent_level>)... the (deleted key and value) and parent level."""
            # parameter setup
            if self.is_path_relative(path):
                path: str = self.__interpret_path__(path=path, return_as_str=True)  # in-case <path> is relative
            if path == '':
                self.__raise_error__(KeyPathError, ignore_errors)
                return

            # main
            data: tuple = self.__walk_path__(path=path)
            out: dict or str or list or int or float or bool or None = data[0].pop(data[1])

            if self.__working_level__.startswith(path):
                if self.__path_separator__ in path:
                    self.set_working_level(self.__path_separator__.join(path.split(self.__path_separator__)[:-1]))
                else:
                    self.set_working_level(path='')

            return out, data[1], data[0]

        # main
        if not to_path.startswith(from_path):
            deleted_data: tuple = delete(from_path)

            if only_contents:
                self.add(value=deleted_data[0], path=to_path, existing_keys=existing_keys, create=create, index=index,
                         integrate_list_with_list=True)
            else:
                if isinstance(deleted_data[2], dict):
                    self.add(value={deleted_data[1]: deleted_data[0]}, path=to_path, existing_keys=existing_keys, create=create,
                             index=index, integrate_list_with_list=integrate_list_with_list)
                else:
                    self.add(value=deleted_data[0], path=to_path, existing_keys=existing_keys, create=create, index=index,
                             integrate_list_with_list=integrate_list_with_list)

        else:
            self.__raise_error__(error=ArgumentError('Cannot move the current level - <from_path> - further into itself.'), ignore=ignore_errors)

        return self

    def copy_from_to(self, from_path: str, to_path: str, only_contents: bool = False, existing_keys: str = 'combine',
                     create: bool = False, index: int or str or None = None, integrate_list_with_list: bool = False,
                     ignore_errors: bool = None) -> 'T4Json':
        """Copy's data from *from_path* to *to_path*."""
        if not to_path.startswith(from_path):
            data: tuple = self.__walk_path__(path=from_path, ignore_path_errors=ignore_errors)

            if only_contents:
                self.add(value=data[0][data[1]], path=to_path, existing_keys=existing_keys, create=create, index=index,
                         integrate_list_with_list=True)
            else:
                if isinstance(data[0], dict):
                    self.add(value={data[1]: data[0][data[1]]}, path=to_path, existing_keys=existing_keys, create=create, index=index,
                             integrate_list_with_list=integrate_list_with_list)
                else:  # if the key is an integer I know it must be an index to a list
                    self.add(value=data[0][data[1]], path=to_path, existing_keys=existing_keys, create=create, index=index,
                             integrate_list_with_list=integrate_list_with_list)
        else:
            self.__raise_error__(error=ArgumentError('Cannot copy the current level - <from_path> - further into itself.'), ignore=ignore_errors)

        return self

    def delete(self, path: str, ignore_errors: bool = None) -> 'T4Json':
        """Deletes the pair or item wherever *path* leads."""

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors
        if self.is_path_relative(path):
            path: str = self.__interpret_path__(path=path, return_as_str=True)  # in-case <path> is relative
        if path == '':
            self.__raise_error__(ArgumentError('<path> must lead to a key.'), ignore_errors)
            return self

        # main
        data: tuple = self.__walk_path__(path=path, ignore_path_errors=ignore_errors)
        data[0].pop(data[1])

        if self.__working_level__.startswith(path):
            if self.__path_separator__ in path:
                self.set_working_level(self.__path_separator__.join(path.split(self.__path_separator__)[:-1]))
            else:
                self.set_working_level(path='')

        return self

    def delete_empty_containers(self, path: str = '', ignore_errors: bool = None) -> 'T4Json':
        """Deletes any keys with empty containers as values. *path* can be used to select the level where this will take place"""

        data_: tuple = self.__walk_path__(path=path, ignore_path_errors=ignore_errors)
        data: dict or list = data_[0][data_[1]]

        if isinstance(data, dict):
            for k in list(data):
                if isinstance(data[k], (dict, list)):
                    if not data[k]:  # if empty
                        self.delete(path=f'{path}{self.__path_separator__}{k}')
        if isinstance(data, list):
            def recursive_func() -> None:
                try:
                    for i, v in enumerate(data):
                        if isinstance(v, (dict, list)):
                            if not v:  # if empty
                                self.delete(path=f'{path}{self.__path_separator__}{i}')
                except IndexError:
                    recursive_func()
            recursive_func()

        return self

    def new(self, new: dict or str or list or int or float or bool or None) -> 'T4Json':
        """Overwrites/replaces all the current data with *new*"""
        if isinstance(self.__data__[self.__root__], (dict, list)):
            self.__data__[self.__root__].clear()
            self.__data__[self.__root__]: Any = new
        else:
            self.__data__[self.__root__]: Any = new
        self.__working_level__: str = ''
        return self

    def wipe(self) -> 'T4Json':
        """Removes all data and leaves you with an empty dict."""
        return self.new({})

    def clear(self) -> 'T4Json':
        """Removes all data and leaves you with an empty dict."""
        # BE CAREFUL to NOT rename this method because it is names the same name as the dictionary method clear()... refactoring will mess that up.
        return self.new({})

    def format(self, indentation: int or str or None = 4, sort_keys: bool = True, only_ascii: bool = False) -> 'T4Json':
        """This method formats the JSON file to make it look nice."""

        self.set_indentation(indentation)
        self.set_sort_keys(sort_keys)
        self.set_only_ascii(only_ascii)
        return self

    def flatten(self, path: str = '', chain_key: bool = False, chain_include_index: bool = False,
                chain_key_separator: str = '_', flatten_opposite_container_type: bool = True,
                pull_pairs_from_lists: bool = True, pull_lists_from_pairs: bool = False,
                existing_keys: str = 'integrate', list_index: int or str or None = None,
                delete_empty_containers: bool = True, ignore_errors: bool = None) -> 'T4Json':
        """This method flattens nested data."""

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors
        if chain_key and chain_key_separator == self.__path_separator__:
            self.__raise_error__(ArgumentError(f'The argument <chained_keys_separator> cannot be the same as the current path separator: "{self.__path_separator__}".'), ignore=ignore_errors)
        if self.is_path_relative(path):
            path: str = self.__interpret_path__(path=path, return_as_str=True)
        self.set_working_level(path='')

        # main
        data: tuple = self.__walk_path__(path)
        container: dict or list = data[0][data[1]]
        if isinstance(container, dict):
            def recursive_func() -> None:
                for key in container:
                    if isinstance(container[key], dict):

                        if chain_key:
                            for key_ in list(container[key]):
                                self.change_key(
                                    path=f'{path}{self.__path_separator__}{key}{self.__path_separator__}{key_}',
                                    new_key=f'{key}{chain_key_separator}{key_}', existing_key='integrate')

                        self.move_from_to(f'{path}{self.__path_separator__}{key}', to_path=path, only_contents=True,
                                          existing_keys=existing_keys, index=list_index)
                        recursive_func()
                        break
                    if flatten_opposite_container_type and isinstance(container[key], list):
                        for index, value in enumerate(container[key]):
                            if isinstance(value, list):
                                if list_index == 'hold':
                                    self.move_from_to(
                                        from_path=f'{path}{self.__path_separator__}{key}{self.__path_separator__}{index}',
                                        to_path=f'{path}{self.__path_separator__}{key}', only_contents=True,
                                        existing_keys=existing_keys, index=index, integrate_list_with_list=True)
                                else:
                                    self.move_from_to(
                                        from_path=f'{path}{self.__path_separator__}{key}{self.__path_separator__}{index}',
                                        to_path=f'{path}{self.__path_separator__}{key}', only_contents=True,
                                        existing_keys=existing_keys, index=list_index, integrate_list_with_list=True)
                                recursive_func()
                                return
                            elif pull_pairs_from_lists and isinstance(container[key][index], dict):

                                if chain_key:
                                    if chain_include_index:
                                        for key_ in list(container[key][index]):
                                            self.change_key(
                                                path=f'{path}{self.__path_separator__}{key}{self.__path_separator__}{index}{self.__path_separator__}{key_}',
                                                new_key=f'{key}{chain_key_separator}{index}{chain_key_separator}{key_}', existing_key='integrate')
                                    else:
                                        for key_ in list(container[key][index]):
                                            self.change_key(
                                                path=f'{path}{self.__path_separator__}{key}{self.__path_separator__}{index}{self.__path_separator__}{key_}',
                                                new_key=f'{key}{chain_key_separator}{key_}', existing_key='integrate')

                                self.move_from_to(
                                    from_path=f'{path}{self.__path_separator__}{key}{self.__path_separator__}{index}',
                                    to_path=path, only_contents=True, existing_keys=existing_keys, index=list_index)
                                recursive_func()
                                return

            recursive_func()
        elif isinstance(container, list):
            def recursive_func() -> None:
                if list_index == 'hold':
                    for index, value in enumerate(container):
                        if isinstance(value, list):
                            self.move_from_to(from_path=f'{path}{self.__path_separator__}{index}', to_path=path,
                                              only_contents=True, existing_keys=existing_keys, index=index)
                            recursive_func()
                            break
                else:
                    for index, value in enumerate(container):
                        if isinstance(value, list):
                            self.move_from_to(from_path=f'{path}{self.__path_separator__}{index}', to_path=path,
                                              only_contents=True, existing_keys=existing_keys, index=list_index)
                            recursive_func()
                            break

            recursive_func()
            if flatten_opposite_container_type:
                for i, v in enumerate(container):
                    if isinstance(v, dict):
                        self.flatten(path=f'{path}{self.__path_separator__}{i}', chain_key=chain_key,
                                     chain_key_separator=chain_key_separator,
                                     flatten_opposite_container_type=flatten_opposite_container_type,
                                     pull_pairs_from_lists=pull_pairs_from_lists,
                                     existing_keys=existing_keys, list_index=list_index,
                                     delete_empty_containers=False)
                if pull_lists_from_pairs:
                    def recursive_func() -> None:
                        for index, value in enumerate(container):
                            if isinstance(value, dict):
                                for key in value:
                                    if isinstance(value[key], list):
                                        self.move_from_to(
                                            from_path=f'{path}{self.__path_separator__}{index}{self.__path_separator__}{key}',
                                            to_path=path, only_contents=True, index=list_index)
                                        recursive_func()
                                        break

                    recursive_func()

        if delete_empty_containers:
            self.delete_empty_containers()

        return self

    def read(self, path: str = '', ignore_errors: bool = None) -> dict or str or list or int or float or bool or None:
        """Returns the value of wherever *path* leads."""

        data: tuple = self.__walk_path__(path=path, ignore_path_errors=ignore_errors)
        return data[0][data[1]]

    def pair(self, path: str, as_dictionary: bool = False, ignore_errors: bool = None) -> tuple or dict:
        """Returns a pair in the form of a tuple (<key>, <value>) or dictionary pair {<key>: <value>}
        from wherever *path* leads."""

        data: tuple = self.__walk_path__(path=path, ignore_path_errors=ignore_errors)
        if as_dictionary:
            return {data[1]: data[0][data[1]]}
        else:
            return data[1], data[0][data[1]]

    def pairs(self, path: str = '', as_dictionaries: bool = False, ignore_errors: bool = None) -> list:
        """Returns a list of tuples of (key, value) pairs - [(key, value), (key, value)..] of the selected level.
        This method is very similar to the items() method of dict."""

        data_: tuple = self.__walk_path__(path=path, ignore_path_errors=ignore_errors)
        data: dict or str or list or int or float or bool or None = data_[0][data_[1]]
        if isinstance(data, dict):
            if as_dictionaries:
                return [{k: v} for k, v in data.items()]
            else:
                return list(data.items())

    def key(self, path: str, ignore_errors: bool = None) -> str or int or float or bool or None:
        """Returns the key of the value that *path* leads to. If the value is in a list the values index will be
        returned as an integer."""
        return self.__walk_path__(path=path, ignore_path_errors=ignore_errors)[1]

    def keys(self, path: str = '', ignore_errors: bool = None) -> list:
        """Returns a list of all the of keys in the location that is specified by *path*. If *path* leads
        to a non-container value than it will return the key of that value."""

        data: tuple = self.__walk_path__(path=path, ignore_path_errors=ignore_errors)
        if isinstance(data[0][data[1]], dict):
            return list(data[0][data[1]])
        elif isinstance(data[0][data[1]], list):
            return [i for d in data[0][data[1]] if isinstance(d, dict) for i in d]

    def values(self, path: str = '', only_values_of_pairs: bool = True, ignore_errors: bool = None) -> list:
        """Returns a list of all the of values in the location that is specified by *path*. If *path* leads
        to a non-container value than that value will simply be returned."""

        data_: tuple = self.__walk_path__(path=path, ignore_path_errors=ignore_errors)
        data: dict or str or list or int or float or bool or None = data_[0][data_[1]]
        if isinstance(data, dict):
            return list(data.values())
        elif isinstance(data, list):
            if only_values_of_pairs:
                return [i for d in data if isinstance(d, dict) for i in d.values()]
            else:
                return [d for d in data if not isinstance(d, dict)] + [i for d in data if isinstance(d, dict) for i in d.values()]

    def all_keys(self, path: str = '', search_lists: bool = True, as_paths: bool = False, ignore_errors: bool = None) -> list:
        """Returns a list of all the keys past a certain point which is specified by *path*. This method only returns0
         keys that have a non-container value"""
        # TODO build a better algorithm here instead of using the flatten() method.
        from copy import deepcopy
        data: T4Json = T4Json()

        try:
            data.load_object(deepcopy(self.read(path=path)))

            if isinstance(data.__data__[data.__root__], dict):
                if not as_paths:
                    data.flatten(flatten_opposite_container_type=search_lists, pull_pairs_from_lists=search_lists,
                                 pull_lists_from_pairs=True)
                else:
                    current_path_separator: str = data.__path_separator__
                    data.set_path_separator_properties(separator=r'_sep-\\//-sep_')
                    data.flatten(chain_key=as_paths, chain_include_index=True, chain_key_separator=current_path_separator,
                                 flatten_opposite_container_type=search_lists, pull_pairs_from_lists=search_lists,
                                 pull_lists_from_pairs=True)
            elif isinstance(data.__data__[data.__root__], list):
                data.flatten(flatten_opposite_container_type=False, delete_empty_containers=False)
                out: T4Json = T4Json()
                for d in data.__data__[data.__root__]:
                    if isinstance(d, dict):
                        out.add(value=d, existing_keys='combine')
                data.load_object(out.__data__[data.__root__])
                if not as_paths:
                    data.flatten(flatten_opposite_container_type=search_lists, pull_pairs_from_lists=search_lists,
                                 pull_lists_from_pairs=True)
                else:
                    current_path_separator: str = data.__path_separator__
                    data.set_path_separator_properties(separator=r'_sep-\\//-sep_')
                    data.flatten(chain_key=as_paths, chain_include_index=True, chain_key_separator=current_path_separator,
                                 flatten_opposite_container_type=search_lists, pull_pairs_from_lists=search_lists,
                                 pull_lists_from_pairs=True)
            return list(data.__data__[data.__root__])

        except (KeyPathError, AddError):
            data.__raise_error__(ValueError('There was a problem while searching through the JSON data.'), ignore_errors)
        except AttributeError:
            pass

    def all_values(self, path: str = '', search_lists: bool = True, ignore_errors: bool = None) -> list:
        """Returns a list of all the of values in the location that is specified by *path*. If *path* leads to a
        non-container value than that value will simply be returned."""
        # TODO build a better algorithm here instead of using the flatten() method.
        from copy import deepcopy
        data: T4Json = T4Json()

        try:
            data.load_object(deepcopy(self.read(path=path)))

            if isinstance(data.__data__[data.__root__], dict):
                data.flatten(flatten_opposite_container_type=search_lists, pull_pairs_from_lists=search_lists,
                             pull_lists_from_pairs=True)
            elif isinstance(data.__data__[data.__root__], list):
                data.flatten()
                out: T4Json = T4Json()
                for d in data.__data__[data.__root__]:
                    if isinstance(d, dict):
                        out.add(value=d, existing_keys='combine')
                data.load_object(out.__data__[data.__root__])
                data.flatten(flatten_opposite_container_type=search_lists, pull_pairs_from_lists=search_lists,
                             pull_lists_from_pairs=True)

            return list(data.__data__[data.__root__].values())

        except (KeyPathError, AddError):
            data.__raise_error__(ValueError('there was a problem while searching through the JSON data.'),
                                 ignore_errors)
        except AttributeError:
            pass

    def all_pairs(self, path: str = '', search_lists: bool = True, as_dictionaries: bool = False, ignore_errors: bool = None) -> list:
        """Returns a list of tuples of all (key, value) pairs as - [(key, value), (key, value)..] past a point
        specified by *path*."""
        # TODO build a better algorithm here instead of using the flatten() method.
        from copy import deepcopy
        data: T4Json = T4Json()

        try:
            data.load_object(deepcopy(self.read(path=path)))

            if isinstance(data.__data__[data.__root__], dict):
                data.flatten(flatten_opposite_container_type=search_lists, pull_pairs_from_lists=search_lists,
                             pull_lists_from_pairs=True)
            elif isinstance(data.__data__[data.__root__], list):
                data.flatten()
                out: T4Json = T4Json()
                for d in data.__data__[data.__root__]:
                    if isinstance(d, dict):
                        out.add(value=d, existing_keys='combine')
                data.load_object(out.__data__[data.__root__])
                data.flatten(flatten_opposite_container_type=search_lists, pull_pairs_from_lists=search_lists,
                             pull_lists_from_pairs=True)

            return data.pairs(as_dictionaries=as_dictionaries)

        except (KeyPathError, AddError):
            data.__raise_error__(KeyPathError('there was a problem while searching through the JSON data.'),
                                 ignore_errors)
        except AttributeError:
            pass

    def search(self, key: str, path: str = '', search_lists: bool = False,
               ignore_errors: bool = None) -> list or str or int or float or bool or None:
        """Searches through all the JSON data or (past a certain point specified by *path*) for *key*. If there are
        multiple keys with the same name spread throughout the data, a list of their all there values will be returned.
        Containers will not be returned."""
        # TODO build a better algorithm here instead of using the flatten() method.
        from copy import deepcopy

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors

        # main
        data: T4Json = T4Json()
        try:
            data.load_object(deepcopy(self.read(path=path)))

            if isinstance(data.__data__[data.__root__], dict):
                data.flatten(flatten_opposite_container_type=search_lists, pull_pairs_from_lists=search_lists,
                             pull_lists_from_pairs=search_lists)
            elif isinstance(data.__data__[data.__root__], list):
                data.flatten()
                out: T4Json = T4Json()
                for d in data.__data__[data.__root__]:
                    if isinstance(d, dict):
                        out.add(value=d, existing_keys='combine')
                data.load_object(out.__data__[data.__root__])
                data.flatten(flatten_opposite_container_type=search_lists, pull_pairs_from_lists=search_lists,
                             pull_lists_from_pairs=search_lists)

            return data.read(path=key)

        except (KeyPathError, AddError):
            data.__raise_error__(KeyPathError(f'The key "{key}" could not be found.'),
                                 ignore_errors)
        except AttributeError:
            pass

    def json_string(self, path: str = '', indent: int or str = None, sort_keys: bool = None, only_ascii: bool = None,
                    separators: tuple = None, ignore_errors: bool = None) -> str:
        """Returns a JSON formatted string. This string can then... for example be saved to a file."""

        if indent is None:
            indent: int or str or None = self.indentation
        if sort_keys is None:
            sort_keys: bool or None = self.sort_keys
        if only_ascii is None:
            only_ascii: bool = self.only_ascii
        if separators is None:
            separators: tuple = self.__json_separators__
        return json.dumps(self.read(path=path, ignore_errors=ignore_errors), skipkeys=True, indent=indent,
                          sort_keys=sort_keys, ensure_ascii=only_ascii, separators=separators)

    def set_working_level(self, path: str = '', ignore_errors: bool = None) -> 'T4Json':
        """Sets the working level within a nested data structure."""

        if self.is_path_relative(path):
            path: str = self.__interpret_path__(path, return_as_str=True)

        if isinstance(self.read(path=path, ignore_errors=ignore_errors), (dict, list)):
            self.__working_level__: str = path
        else:
            self.__working_level__: str = self.__path_separator__.join(path.split(self.__path_separator__)[:-1])

        return self

    def set_indentation(self, indentation: int or str or None) -> 'T4Json':
        """Sets the indentation of the JSON file which will be applied when it is saved/serialized."""
        self.indentation: int or str or None = indentation
        return self

    def set_sort_keys(self, boolean: bool) -> 'T4Json':
        """Keys will be sorted in alphabetical/numerical order. This will be applied when the file is saved/serialized."""
        self.sort_keys: bool = boolean
        return self

    def set_only_ascii(self, boolean: bool) -> 'T4Json':
        """Any non-ascii characters will be escaped/encoded. This will be applied when the file is saved/serialized."""
        self.only_ascii: bool = boolean
        return self

    def set_ignore_errors(self, boolean: bool) -> 'T4Json':
        """Any non-critical errors (such as the path being incorrect) will be ignored."""
        self.ignore_method_errors: bool = boolean
        return self

    def set_path_separator_properties(self, separator: str = None, relative: str = None, relative_back: str = None) -> 'T4Json':
        """Sets the path separator and relative path navigation properties."""

        # parameter setup
        if separator is None:
            separator: str = self.__path_separator__
        if relative is None:
            relative: str = self.__relative_path_command__
        if relative_back is None:
            relative_back: str = self.__relative_back_path_command__

        # main
        def is_common_element_in_str(a, b) -> bool:
            if set(a) & set(b):
                return True
            else:
                return False
        if (separator == '') or (' ' in separator):
            raise ArgumentError('Argument <separator> cannot be used.')
        elif (relative == '') or (' ' in relative):
            raise ArgumentError('Argument <relative> cannot be used.')
        elif (relative_back == ' ') or (' ' in relative_back):
            raise ArgumentError('Argument <relative_back> cannot be used.')
        elif relative == relative_back:
            raise ArgumentError('Argument <relative> and <relative_back> cannot be the same.')
        elif is_common_element_in_str(separator, relative):
            raise ArgumentError('Argument <relative> and <separator> cannot have any character in common.')
        elif is_common_element_in_str(separator, relative_back):
            raise ArgumentError('Argument <relative_back> and <separator> cannot have any character in common.')
        else:
            self.__working_level__: str = self.__working_level__.replace(self.__path_separator__, separator)  # incase working path already exist
            self.__path_separator__: str = separator

        return self

    def set_json_separators(self, item_separator: str = None, key_value_separator: str = None) -> 'T4Json':
        """Sets the pair and item separator properties for the JSON data when it is saved/serialized.
        The most compact arguments would be ("," and ":") instead of the default (", " and ": ")."""

        if item_separator is None:
            item_separator: str = self.__json_separators__[0]
        if key_value_separator is None:
            key_value_separator: str = self.__json_separators__[1]

        self.__json_separators__: tuple = (item_separator, key_value_separator)
        return self

    def set_known_objects_for_path(self, objects: list = None) -> 'T4Json':
        """Updates the known objects that path uses to navigate data - (and uses these objects as keys)."""
        if objects is None:
            self.__known_objects_for_path__: dict = {'bool': bool, 'int': int, 'float': float, 'complex': complex,
                                                     'list': list, 'tuple': tuple, 'frozenset': frozenset,
                                                     'set': set, 'dict': dict, 'str': str, 'object': object, }
        for o in objects:
            self.__known_objects_for_path__.update({o.__name__: o})
        return self

    def is_sorting_keys(self) -> bool:
        """Returns True if the keys are being sorted in alphabetical/numerical order. Otherwise, it returns False."""
        return self.sort_keys

    def is_only_ascii(self) -> bool:
        """Returns True if all non-ascii characters are being escaped/encoded. Otherwise, it returns False."""
        return self.only_ascii

    def is_ignoring_errors(self) -> bool:
        """Returns True if non-critical errors are being ignored. Otherwise, False is returned."""
        return self.ignore_method_errors

    def get_working_level(self) -> str:
        """Returns the current working level as a path."""
        return self.__working_level__

    def get_indentation(self) -> int or str or None:
        """Returns the indentation property. An int, str or None can be expected."""
        return self.indentation

    def get_path_separator_properties(self) -> tuple:
        """Returns the current path separator properties."""
        return self.__path_separator__, self.__relative_path_command__, self.__relative_back_path_command__

    def get_known_objects_for_path(self) -> list:
        """Returns a list of the objects that have been made known."""
        return list(self.__known_objects_for_path__.values())

    def reset_settings(self) -> None:
        """Resets any settings that have been changed... back to their original default values."""

        # user_settings
        self.ignore_method_errors: bool = False
        self.indentation: int or str or None = 4
        self.sort_keys: bool = False
        self.only_ascii: bool = False

        self.set_known_objects_for_path()

        # off limit __vars__
        self.__json_separators__: tuple = (', ', ': ')  # index 0 is for items and index 1 is for JSON objects
        self.__path_separator__: str = '\\\\'
        self.__relative_path_command__: str = ''
        self.__relative_back_path_command__: str = '..'
        self.__working_level__: str or None = None

    def is_path_existent(self, path) -> bool:
        """Checks to see if *path* exist in the currently opened data structure. True is return if it
        does exist... and False otherwise."""

        try:
            self.__walk_path__(path, ignore_path_errors=False)
            return True
        except KeyPathError:
            return False

    def is_path_relative(self, path: str = '') -> bool:
        """Checks to see if *path* is a relative path. True is returned if it is... and False otherwise."""

        if path == '':
            return False
        else:
            if path in (self.__relative_path_command__, self.__relative_back_path_command__):
                return True
            elif path.startswith(self.__relative_back_path_command__ + self.__path_separator__) or path.startswith(self.__relative_path_command__ + self.__path_separator__):
                return True
            else:
                return False

    def load(self, source: str or bytes or dict or list, url_parameters: dict or list or bytes = None, url_headers: dict = None, url_body: Any = None, url_user_auth: Any = None, url_request_method: str = 'GET', url_raise_for_status: bool = False, create: bool = False, encoding: str = 'utf-8', encoding_errors: str = 'ignore', decode_html_entities: bool = False) -> 'T4Json':
        """This method loads the JSON data. It can receive a File Path, URL, or JSON String."""
        from os.path import exists as file_path_exists

        if isinstance(source, (dict, list)):
            self.load_object(source)
        elif file_path_exists(source):
            self.load_file(file_path=source, create=create, encoding=encoding, encoding_errors=encoding_errors,
                           decode_html_entities=decode_html_entities)
        elif source.startswith('http'):
            self.load_from_url(url=source, parameters=url_parameters, headers=url_headers, body=url_body,
                               user_auth=url_user_auth, request_method=url_request_method,
                               raise_for_status=url_raise_for_status, encoding=encoding,
                               encoding_errors=encoding_errors, decode_html_entities=decode_html_entities)
        else:
            self.load_from_string(string=source, encoding=encoding, encoding_errors=encoding_errors,
                                  decode_html_entities=decode_html_entities)

        return self

    def load_file(self, file_path: str, create: bool = False, encoding: str = 'utf-8', encoding_errors: str = 'ignore', decode_html_entities: bool = False) -> 'T4Json':
        """Loads the JSON data from a specified file."""

        try:
            with open(file_path, 'r', encoding=encoding, errors=encoding_errors) as file:
                if decode_html_entities:
                    self.load_from_string(string=file.read(), decode_html_entities=decode_html_entities)
                else:
                    data: dict or list = json.load(file)
            self.close()
            self.__data__: dict = {self.__root__: data}
            return self
        except FileNotFoundError:
            if create:
                with open(file_path, 'w', encoding=encoding, errors=encoding_errors) as new_file:
                    json.dump({}, new_file)
                self.load_file(file_path=file_path, create=create, encoding=encoding, encoding_errors=encoding_errors)
            else:
                raise LoadFileError(
                    'File does not exist - Set the <create> argument to True so that if a file does not exist it will '
                    'be created.')
        except Exception:
            raise LoadFileError(
                'There was an error retrieving the JSON data from file. It may be corrupted or <encoding> could be incorrect.')

    def load_from_string(self, string: str or bytes, encoding: str = 'utf-8', encoding_errors: str = 'ignore', decode_html_entities: bool = False) -> 'T4Json':
        """Loads JSON data from a string."""

        try:
            if isinstance(string, bytes):
                string: str = string.decode(encoding=encoding, errors=encoding_errors)
            if decode_html_entities:
                data: dict or list = json.loads(self.__decode_html_entities__(string))
            else:
                data: dict or list = json.loads(string)

            self.close()
            self.__data__: dict = {self.__root__: data}  # deserialize JSON data into object type dict
            return self
        except Exception:
            raise LoadStringError

    def load_from_url(self, url: str, parameters: dict or list or bytes = None, headers: dict = None, body: Any = None, user_auth: Any = None, request_method: str = 'GET', raise_for_status: bool = False, encoding: str = 'utf-8', encoding_errors: str = 'ignore', decode_html_entities: bool = False) -> 'T4Json':
        """Loads JSON data from the specified URL."""
        from requests import request

        try:
            with request(method=request_method, url=url, params=parameters, headers=headers, auth=user_auth, json=body) as response:
                if raise_for_status:
                    response.raise_for_status()

            try:
                if decode_html_entities:
                    data: dict or list = json.loads(self.__decode_html_entities__(response.content.decode(encoding=encoding, errors=encoding_errors)))
                else:
                    data: dict or list = json.loads(response.content.decode(encoding=encoding, errors=encoding_errors))
            except Exception:
                raise LoadURLError

            self.close()
            self.__data__: dict = {self.__root__: data}
            return self
        except Exception as e:
            raise LoadURLError(e.__str__())

    def load_object(self, value: dict or list) -> 'T4Json':
        """Receives whatever is passed to *value* as the new JSON data to work with."""

        self.__file_path__: str or None = None
        return self.new(value)

    def save(self, indent: int or str = None, sort_keys: bool = None, only_ascii: bool = None, separators: tuple = None,
             encoding: str = 'utf-8', encoding_errors: str = 'strict') -> 'T4Json':
        """Saves the currently opened file if a file is opened."""

        if self.__file_path__ is not None:
            if indent is None:
                indent: int or str or None = self.indentation
            if sort_keys is None:
                sort_keys: bool or None = self.sort_keys
            if only_ascii is None:
                only_ascii: bool = self.only_ascii
            if separators is None:
                separators: tuple = self.__json_separators__
            with open(self.__file_path__, 'w', encoding=encoding, errors=encoding_errors) as file:
                json.dump(obj=self.__data__[self.__root__], fp=file, skipkeys=True, indent=indent, sort_keys=sort_keys,
                          ensure_ascii=only_ascii, separators=separators)
            return self

    def save_as(self, file_path: str, overwrite: bool = False, indent: int or str = None, sort_keys: bool = None,
                only_ascii: bool = None, separators: tuple = None, encoding: str = 'utf-8',
                encoding_errors: str = 'strict') -> 'T4Json':
        """Saves the current JSON data as a new file."""
        from os.path import exists as file_path_exists

        if indent is None:
            indent: int or str or None = self.indentation
        if sort_keys is None:
            sort_keys: bool or None = self.sort_keys
        if only_ascii is None:
            only_ascii: bool = self.only_ascii
        if separators is None:
            separators: tuple = self.__json_separators__

        if not file_path_exists(file_path) or overwrite:
            with open(file_path, 'w', encoding=encoding, errors=encoding_errors) as file:
                json.dump(obj=self.__data__[self.__root__], fp=file, skipkeys=True, indent=indent, sort_keys=sort_keys,
                          ensure_ascii=only_ascii, separators=separators)
        else:
            raise FileExistsError('<new_file> must not already exist.\nSet the <overwrite> argument to True so that'
                                  'if a file already does exist it will be overwritten and no exception will '
                                  'be thrown.')
        return self

    def close(self) -> 'T4Json':
        """Simply closes the data that's already open and leaves you with an empty dictionary."""
        self.__file_path__: str or None = None
        return self.new({})

    @property
    def data(self) -> dict or list or str or float or int or bool or None:
        return self.__data__[self.__root__]

    def pprint(self, path: str = '', indent: int = 1, print_to_console: bool = True, ignore_errors: bool = None) -> str:
        """Pretty Prints the currently opened data."""
        from pprint import pformat
        out: str = pformat(self.read(path=path, ignore_errors=ignore_errors), indent=indent)
        if print_to_console:
            print(out)
        return out

    @staticmethod
    def __raise_error__(error: object, ignore: bool = False, from_none: bool = False) -> None:
        if not ignore:
            if from_none:
                raise error from None
            else:
                raise error

    @staticmethod
    def __decode_html_entities__(string: str) -> str:
        from html import unescape as decode_html
        return decode_html(string.replace('&quot;', r'\"'))

    def __interpret_path__(self, path: str, working_level: str = None, return_as_str: bool = False) -> list or str:
        """Receives a path as relative or absolute and then always returns the absolute version of the path as a list"""
        # parameter setup
        if working_level is None:
            working_level: str = self.__working_level__
        if path == '.':
            path: str = working_level
        elif path == '..':
            path: str = working_level.rpartition(self.__path_separator__)[0]

        # main
        back: str = self.__relative_back_path_command__ + self.__path_separator__
        working: str = self.__relative_path_command__ + self.__path_separator__
        if path.startswith(back):  # if going back

            left_count = 0
            for b in path.split(self.__path_separator__):
                if b == self.__relative_back_path_command__:
                    left_count += 1
                else:
                    break
            out: list = working_level.split(self.__path_separator__)[:-left_count] + path.split(self.__path_separator__)[left_count:]

        elif path.startswith(working):  # if work at current working level
            out: list = working_level.split(self.__path_separator__) + path.split(self.__path_separator__)[1:]

        else:  # if absolute path

            if return_as_str:
                return path
            out: list = path.split(self.__path_separator__)

        if return_as_str:
            return self.__path_separator__.join(out)
        else:
            return out

    def __walk_path__(self, path: str, ignore_path_errors: bool = None) -> tuple:
        """return the parent container along with the key in a tuple to access its value - (container, key)."""
        # parameter setup
        if ignore_path_errors is None:
            ignore_path_errors: bool = self.ignore_method_errors

        if path == '' and not self.is_path_relative(path):
            return self.__data__, self.__root__

        # path setup
        path_: list = self.__interpret_path__(path)
        error_catcher_key: str = path

        # main
        try:
            if not path_[0] == '':
                parent_of_target_level: dict or list = self.__data__[self.__root__]  # level iterator... used to assign each level as it walks down the data structure.
            else:
                parent_of_target_level: dict = self.__data__  # level iterator... used to assign each level as it walks down the data structure.

            for key in path_[:-1]:  # loop through path all the way down to the parent of the target level
                error_catcher_key: str = key  # if key does not exist this is used to catch the error
                if isinstance(parent_of_target_level, dict):  # if parent of the target level is a dictionary
                    try:
                        parent_of_target_level: dict or list = parent_of_target_level[key]
                    except KeyError:
                        parent_of_target_level: dict or list = parent_of_target_level[self.__literal_eval__(key)]
                else:  # if parent of the target level is a list
                    parent_of_target_level: dict or list = parent_of_target_level[int(key)]

            target_level_key: str = path_[-1]
            error_catcher_key: str = target_level_key

            # Return level

            def catch_invalid_path(target_key) -> Any: return parent_of_target_level[target_key]
            if isinstance(parent_of_target_level, dict):
                try:  # since the target level is not checked in the for loop check it here
                    catch_invalid_path(target_level_key)
                except KeyError:
                    target_level_key: Any = self.__literal_eval__(target_level_key)
                    catch_invalid_path(target_level_key)

                return parent_of_target_level, target_level_key
            else:  # elif - is list
                catch_invalid_path(int(target_level_key))  # since the target level is not checked in the for loop check it here
                return parent_of_target_level, int(target_level_key)

        except (KeyError, TypeError, SyntaxError):  # SyntaxError is caused by literal_eval()... like if "8f" is in path.
            self.__raise_error__(KeyPathError(f'\n`{error_catcher_key}` is a non-existent key or an invalid index.'), ignore=ignore_path_errors)
            return {'error': f'`{error_catcher_key}` is a non-existent key or an invalid index.'}, 'error'
        except ValueError:
            self.__raise_error__(KeyPathError(f'\n`{error_catcher_key}` is an invalid index.'),
                                 ignore=ignore_path_errors)
            return {'error': f'Index `{error_catcher_key}` is an invalid index.'}, 'error'
        except IndexError:
            self.__raise_error__(KeyPathError(f'\nIndex `{error_catcher_key}` is out of range.'), ignore=ignore_path_errors)
            return {'error': f'Index `{error_catcher_key}` is out of range.'}, 'error'

    def __literal_eval__(self, string: str) -> Any:
        # Basically Performs Lexical Analysis
        """
        Safely evaluate a python datatype from a string. The string may only consist of the following
        Python literal structures: strings, bytes, numbers, tuples, sets (become frozensets), booleans, and None.
        """

        # Basic single DataTypes:
        if string.replace('.', '', 1).isnumeric():  # if string is a number
            return float(string)
        elif string == 'True':
            return True
        elif string == 'False':
            return False
        elif string == 'None':
            return None

        from re import compile as regex_compile, findall as regex_findall, Pattern
        # Custom Objects defined by `self.__known_objects_for_path__`:
        if string.startswith("<class '") and string.endswith("'>"):
            # if <string> is the objects full name... then extract the name
            string: str = regex_findall('[a-zA-Z_]+', string)[-1]
        if string in self.__known_objects_for_path__:
            # if there is a custom object... then it will be returned without any further processing
            return self.__known_objects_for_path__[string]

        # Frozenset Object - prep (if needed) for Main:
        """Note:
        If the string "frozenset({...})" is in a path... since ast.literal_eval() does not understand frozensets 
        the "frozenset({...})" must be converted to "{...}"... then once ast processes it... it will be returned as a 
        frozenset.
        """
        regex_frozenset_pattern: Pattern = regex_compile(r'(frozenset\((.*?)\))')

        def frozenset_to_set_string(s: str) -> str:  # recursive function
            changes: list = regex_frozenset_pattern.findall(s)
            if not changes:
                return s
            else:
                for old, new in changes:
                    s: str = s.replace(old, new)
                return frozenset_to_set_string(s)

        if regex_frozenset_pattern.findall(string):
            string: str = frozenset_to_set_string(string)
            if string == '':
                return frozenset()
            if '{}' in string:
                string: str = string.replace('{}', '')

        # Main - a bit more complex data types like a nested frozenset:
        from ast import parse, Expression, Tuple, Set, Constant, UnaryOp, UAdd, USub, expr, AST
        string: AST or Expression = parse(string.lstrip(" \t"), mode='eval')
        if isinstance(string, Expression):
            string: expr = string.body

        def _raise_malformed_node(node) -> Any:
            msg = "malformed node or string"
            if lno := getattr(node, 'lineno', None):
                msg += f' on line {lno}'
            raise KeyError(msg + f': {node!r}')  # instead of ValueError which is the default

        def _convert_num(node) -> Any:
            if not isinstance(node, Constant) or type(node.value) not in (int, float, complex):
                _raise_malformed_node(node)
            return node.value

        def _convert_signed_num(node) -> Any:
            if isinstance(node, UnaryOp) and isinstance(node.op, (UAdd, USub)):
                operand: Any = _convert_num(node.operand)
                if isinstance(node.op, UAdd):
                    return + operand
                else:
                    return - operand
            return _convert_num(node)

        def _convert(node) -> Any:
            if isinstance(node, Constant):
                return node.value
            elif isinstance(node, Tuple):
                return tuple(map(_convert, node.elts))
            elif isinstance(node, Set):
                return frozenset(map(_convert, node.elts))  # change from set to frozenset... unlike ast.literal_eval()
            return _convert_signed_num(node)

        return _convert(string)


class LoadFileError(Exception):
    pass


class LoadURLError(Exception):
    def __init__(self, message: str = None) -> None:
        if message is None:
            super().__init__('\nEven though the data was successfully retrieved from <url>... it could not be deserialized.'
                             '\nSome things that may have gone wrong:'
                             '\n\t1. JSON data is corrupted.'
                             '\n\t2. There could be encoding issues that are corrupting the data.'
                             '\n\t3. Calling an API that does not return JSON data as its format.')


class LoadStringError(Exception):
    def __init__(self, message: str = None) -> None:
        if message is None:
            super().__init__('\nJSON data could not be loaded from <string>.'
                             '\nSome things that may have gone wrong:'
                             '\n\t1. JSON data is corrupted.'
                             '\n\t2. There could be encoding issues that are corrupting the data.')


LoadError: tuple = (LoadFileError, LoadURLError, LoadStringError)


class KeyPathError(Exception):
    pass


class AddError(Exception):
    def __init__(self, message: str = None) -> None:
        if message is None:
            super().__init__('(<value> cannot be added because <structure_path> leads to a mutable object.)'
                             ' - OR - (A single value without a corresponding key was attempting to be added to a '
                             'JSON container.)\nSet the <create> argument to True so that a list will automatically be '
                             'created including the unsupported object and the new <value>.')


class ArgumentError(Exception):  # maybe replace this for the default TypeError
    pass


def is_valid_json_data(source: str) -> bool:
    """This function returns ```True``` if the JSON data is valid. Otherwise, it returns ```False```."""

    try:
        T4Json(source=source)
        return True
    except LoadError:
        return False


def convert_to_valid_json_ready_data(value: dict or list or tuple or str or float or int or bool or None) -> dict or list or str or float or int or bool or None:
    """Converts *value* into JSON ready data. It will remove any unsupported keys and convert the keys that are not string into strings."""

    if isinstance(value, (dict, list, tuple)):
        return json.loads(json.dumps(obj=value, skipkeys=True))
    else:
        return value


def deserialize_from_string(string: str) -> dict or list or str or int or float or bool or None:
    """Loads JSON data from a *string* and returns the python data structure."""
    return json.loads(string)


def serialize_to_string(value: dict or list or str or int or float or bool or None, indent: None or int or str = None, sort_keys: bool = False, only_ascii: bool = False, separators: tuple = (', ', ': ')) -> str:
    """Returns a JSON formatted string from *value*. This string can then... for example be saved to a file."""
    return json.dumps(value, skipkeys=True, ensure_ascii=only_ascii, sort_keys=sort_keys, indent=indent, separators=separators)
