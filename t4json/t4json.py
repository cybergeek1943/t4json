import json
from requests.auth import AuthBase, HTTPBasicAuth, HTTPDigestAuth, HTTPProxyAuth


class T4Json:

    __slots__: tuple = (
        '__file_path', 'ignore_method_errors', 'indentation', 'sort_keys', 'only_ascii', '__json_separators',
        '__path_separator', '__relative_path_command', '__relative_back_path_command',
        '__working_level', '__root', '__data')

    def __init__(self, source: str = None, url_parameters: dict | list | bytes = None,
                 url_headers: dict | list | bytes = None, url_user_auth: any = None, create: bool = False,
                 encoding: str = 'utf-8', encoding_errors: str = 'ignore', decode_html_entities: bool = False):
        self.__file_path: str | None = None  # used throughout the class to open, write and read to JSON files

        # user_settings
        self.ignore_method_errors: bool = False
        self.indentation: int | str | None = 4
        self.sort_keys: bool = False
        self.only_ascii: bool = False

        # off limit __vars__
        self.__json_separators: tuple = (', ', ': ')  # index 0 is for items and index 1 is for pairs keys and values.
        self.__path_separator: str = '\\\\'
        self.__relative_path_command: str = '.'
        self.__relative_back_path_command: str = '..'
        self.__working_level: str = ''
        self.__root: str = ''

        self.__data: dict = {self.__root: {}}

        if source is not None:
            self.load(source=source, url_parameters=url_parameters, url_headers=url_headers,
                      url_user_auth=url_user_auth, create=create, encoding=encoding, encoding_errors=encoding_errors,
                      decode_html_entities=decode_html_entities)

    def add(self, value: dict | list | str | float | int | bool | None, path: str = '', existing_keys: str = 'pass', create: bool = False, index: int | str | None = None, integrate_list_with_list: bool = False, ignore_errors: bool = None) -> None:
        """Adds *value* to the base... or elsewhere if specified by *path*."""

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors
        existing_keys: str = existing_keys.lower()

        # main
        try:
            data_: tuple = self.__walk_path__(path=path)
            data: dict | list | str | float | int | bool | None = data_[0][data_[1]]
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
                        self.add(value=duplicates[k], path=f'{path}{self.__path_separator}{k}',
                                 existing_keys=existing_keys, create=True, index=index, integrate_list_with_list=False)
                elif existing_keys == 'integrate':
                    duplicates: dict = {}
                    for k, v in value.items():
                        if k in data:
                            duplicates.update({k: v})
                        else:
                            data.update({k: v})
                    for k in duplicates:
                        self.add(value=duplicates[k], path=f'{path}{self.__path_separator}{k}', existing_keys=existing_keys,
                                 create=True, index=index, integrate_list_with_list=True, ignore_errors=ignore_errors)
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

        except (AttributeError, TypeError):
            if create:
                if path == '':
                    self.__data[self.__root] = [self.__data[self.__root]]
                    self.add(value=value, path='', existing_keys=existing_keys, create=create, index=index,
                             integrate_list_with_list=integrate_list_with_list, ignore_errors=ignore_errors)
                else:
                    self.change_value(path, [self.read(path=path)])
                    self.add(value=value, path=path, existing_keys=existing_keys, create=create, index=index,
                             integrate_list_with_list=integrate_list_with_list, ignore_errors=ignore_errors)
            else:
                self.__raise_error__(AddError, ignore_errors)
        except KeyPathError:
            self.__raise_error__(KeyPathError, ignore_errors)

    def change_value(self, path: str, new_value: dict | list | str | float | int | bool | None,
                     ignore_errors: bool = None) -> None:
        """Changes the value of the key/index that *path* leads to."""

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors

        # main
        try:
            data: tuple = self.__walk_path__(path=path)
            data[0][data[1]] = new_value

            if self.is_path_relative(path):
                path: str = self.__interpret_path__(path, return_as_str=True)  # in-case <path> is relative
            if self.__working_level.startswith(path):
                if self.__path_separator in path:
                    self.set_working_level(self.__path_separator.join(path.split(self.__path_separator)[:-1]))
                else:
                    self.set_working_level(path='')
        except KeyPathError:
            self.__raise_error__(KeyPathError, ignore_errors)

    def change_key(self, path: str, new_key: str | int | float | bool | None, existing_key: str = 'error',
                   ignore_errors: bool = None) -> None:
        """Changes the key that *path* leads to."""

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors
        if path == '':
            self.__raise_error__(error=KeyPathError, ignore=ignore_errors)
            return
        new_key: str = str(new_key)
        path: str = self.__interpret_path__(path, return_as_str=True)  # in-case <path> is relative

        # main
        try:
            if not (path.endswith(self.__path_separator + new_key) or path == new_key):  # De Morgan's law - boolean logic
                data: tuple = self.__walk_path__(path=path)

                if new_key not in data[0]:
                    data[0][new_key] = data[0].pop(data[1])  # replaces key in dict with new key while keeping the value

                    if self.__working_level.startswith(path):
                        new_working_level = self.__working_level.split(self.__path_separator)
                        new_working_level[len(path.split(self.__path_separator)) - 1] = new_key
                        self.set_working_level(path=self.__path_separator.join(new_working_level))

                else:  # if a key does already exist with the same name
                    if existing_key in ('combine', 'integrate', 'replace', 'pass'):

                        if self.__path_separator in path:
                            new_path: str = self.__interpret_path__(
                                f'{self.__relative_back_path_command}{self.__path_separator}{new_key}',
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
                            return

                        if self.__working_level.startswith(new_path) or self.__working_level.startswith(path):
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

        except (IndexError, TypeError):
            self.__raise_error__(
                IndexError('The path you entered leads to a list... Use a path that leads to a JSON object/dict pair.'),
                ignore_errors)
        except KeyPathError:
            self.__raise_error__(KeyPathError, ignore_errors)

    def move_from_to(self, from_path: str, to_path: str, only_contents: bool = False, existing_keys: str = 'combine',
                     create: bool = False, index: int | str | None = None, integrate_list_with_list: bool = False,
                     ignore_errors: bool = None) -> None:
        """Moves data from *from_path* to *to_path*."""

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors

        # main
        try:
            if not to_path.startswith(from_path):
                out: dict | str | list | int | float | bool | None = self.delete(from_path)

                if only_contents:
                    self.add(value=out[0], path=to_path, existing_keys=existing_keys, create=create, index=index,
                             integrate_list_with_list=True)
                else:
                    if isinstance(out[1], str):
                        self.add(value={out[1]: out[0]}, path=to_path, existing_keys=existing_keys, create=create,
                                 index=index, integrate_list_with_list=integrate_list_with_list)
                    else:
                        self.add(value=out[0], path=to_path, existing_keys=existing_keys, create=create, index=index,
                                 integrate_list_with_list=integrate_list_with_list)

            else:
                self.__raise_error__(error=ArgumentError('Cannot move the current level - <from_path> - further into itself.'), ignore=ignore_errors)
        except KeyPathError:
            self.__raise_error__(error=KeyPathError, ignore=ignore_errors)

    def copy_from_to(self, from_path: str, to_path: str, only_contents: bool = False, existing_keys: str = 'combine',
                     create: bool = False, index: int | str | None = None, integrate_list_with_list: bool = False,
                     ignore_errors: bool = None) -> None:
        """Copy's data from *from_path* to *to_path*."""

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors

        # main
        try:
            if not to_path.startswith(from_path):
                data: tuple = self.__walk_path__(path=from_path)

                if only_contents:
                    self.add(value=data[0][data[1]], path=to_path, existing_keys=existing_keys, create=create, index=index,
                             integrate_list_with_list=True)
                else:
                    if isinstance(data[1], str):  # if the key is a string I know that it must be for a pair
                        self.add(value={data[1]: data[0][data[1]]}, path=to_path, existing_keys=existing_keys, create=create, index=index,
                                 integrate_list_with_list=integrate_list_with_list)
                    else:  # if the key is an integer I know it must be an index to a list
                        self.add(value=data[0][data[1]], path=to_path, existing_keys=existing_keys, create=create, index=index,
                                 integrate_list_with_list=integrate_list_with_list)
            else:
                self.__raise_error__(error=ArgumentError('Cannot copy the current level - <from_path> - further into itself.'), ignore=ignore_errors)
        except KeyPathError:
            self.__raise_error__(error=KeyPathError, ignore=ignore_errors)

    def delete(self, path: str, ignore_errors: bool = None) -> tuple | None:
        """Deletes the pair or item wherever *path* leads."""

        # For <self.move_from_to()> the output of this method must always be in the format of: (<value>, <key>)... the deleted key and value.
        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors
        if self.is_path_relative(path):
            path: str = self.__interpret_path__(path=path, return_as_str=True)  # in-case <path> is relative
        if path == '':
            self.__raise_error__(KeyPathError, ignore_errors)
            return

        # main
        try:
            data: tuple = self.__walk_path__(path=path)
            out: dict | str | list | int | float | bool | None = data[0].pop(data[1])

            if self.__working_level.startswith(path):
                if self.__path_separator in path:
                    self.set_working_level(self.__path_separator.join(path.split(self.__path_separator)[:-1]))
                else:
                    self.set_working_level(path='')

            return out, data[1]
        except KeyPathError:
            self.__raise_error__(KeyPathError, ignore_errors)

    def delete_empty_containers(self, path: str = '', ignore_errors: bool = None) -> None:
        """Deletes any keys with empty containers as values. *path* can be used to select the level where this will take place"""

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors

        # main
        try:
            data_: tuple = self.__walk_path__(path=path)
            data: dict | list = data_[0][data_[1]]

            if isinstance(data, dict):
                for k in list(data):
                    if isinstance(data[k], (dict, list)):
                        if len(data[k]) == 0:
                            self.delete(path=f'{path}{self.__path_separator}{k}')
            if isinstance(data, list):
                def recursive_func() -> None:
                    try:
                        for i, v in enumerate(data):
                            if isinstance(v, (dict, list)):
                                if len(v) == 0:
                                    self.delete(path=f'{path}{self.__path_separator}{i}')
                    except IndexError:
                        recursive_func()
                recursive_func()

        except KeyPathError:
            self.__raise_error__(error=KeyPathError, ignore=ignore_errors, from_none=True)

    def overwrite(self, new: dict | str | list | tuple | int | float | bool | None) -> None:
        """Overwrites/replaces all the current data with *new*"""

        self.__data[self.__root] = new
        self.set_working_level('')

    def wipe(self) -> None:
        """Removes all data and leaves you with an empty dict."""

        self.overwrite({})

    def clear(self) -> None:
        """Removes all data and leaves you with an empty dict."""

        self.wipe()

    def format(self, indentation: int | str | None = 4, sort_keys: bool = True, only_ascii: bool = False) -> None:
        """This method formats the JSON file to make it look nice."""

        self.set_indentation(indentation)
        self.set_sort_keys(sort_keys)
        self.set_only_ascii(only_ascii)

    def flatten(self, path: str = '', chain_key: bool = False, chain_include_index: bool = False,
                chain_key_separator: str = '_', flatten_opposite_container_type: bool = True,
                pull_pairs_from_lists: bool = True, pull_lists_from_pairs: bool = False,
                existing_keys: str = 'integrate', list_index: int | str | None = None,
                delete_empty_containers: bool = True, ignore_errors: bool = None) -> None:
        """This method flattens nested data."""

        # parameter setup
        if chain_key and chain_key_separator == self.__path_separator:
            raise ArgumentError(f'The argument <chained_keys_separator> cannot be the same as the current path separator: "{self.__path_separator}".')
        if self.is_path_relative(path):
            path: str = self.__interpret_path__(path=path, return_as_str=True)
        self.set_working_level(path='')

        # main
        try:
            data: tuple = self.__walk_path__(path)
            container: dict | list = data[0][data[1]]
            if isinstance(container, dict):
                def recursive_func() -> None:
                    for key in container:
                        if isinstance(container[key], dict):

                            if chain_key:
                                for key_ in list(container[key]):
                                    self.change_key(
                                        path=f'{path}{self.__path_separator}{key}{self.__path_separator}{key_}',
                                        new_key=f'{key}{chain_key_separator}{key_}', existing_key='integrate')

                            self.move_from_to(f'{path}{self.__path_separator}{key}', to_path=path, only_contents=True,
                                              existing_keys=existing_keys, index=list_index)
                            recursive_func()
                            break
                        if flatten_opposite_container_type and isinstance(container[key], list):
                            for index, value in enumerate(container[key]):
                                if isinstance(value, list):
                                    if list_index == 'hold':
                                        self.move_from_to(
                                            from_path=f'{path}{self.__path_separator}{key}{self.__path_separator}{index}',
                                            to_path=f'{path}{self.__path_separator}{key}', only_contents=True,
                                            existing_keys=existing_keys, index=index, integrate_list_with_list=True)
                                    else:
                                        self.move_from_to(
                                            from_path=f'{path}{self.__path_separator}{key}{self.__path_separator}{index}',
                                            to_path=f'{path}{self.__path_separator}{key}', only_contents=True,
                                            existing_keys=existing_keys, index=list_index, integrate_list_with_list=True)
                                    recursive_func()
                                    return
                                elif pull_pairs_from_lists and isinstance(container[key][index], dict):

                                    if chain_key:
                                        if chain_include_index:
                                            for key_ in list(container[key][index]):
                                                self.change_key(
                                                    path=f'{path}{self.__path_separator}{key}{self.__path_separator}{index}{self.__path_separator}{key_}',
                                                    new_key=f'{key}{chain_key_separator}{index}{chain_key_separator}{key_}', existing_key='integrate')
                                        else:
                                            for key_ in list(container[key][index]):
                                                self.change_key(
                                                    path=f'{path}{self.__path_separator}{key}{self.__path_separator}{index}{self.__path_separator}{key_}',
                                                    new_key=f'{key}{chain_key_separator}{key_}', existing_key='integrate')

                                    self.move_from_to(
                                        from_path=f'{path}{self.__path_separator}{key}{self.__path_separator}{index}',
                                        to_path=path, only_contents=True, existing_keys=existing_keys, index=list_index)
                                    recursive_func()
                                    return

                recursive_func()
            elif isinstance(container, list):
                def recursive_func() -> None:
                    if list_index == 'hold':
                        for index, value in enumerate(container):
                            if isinstance(value, list):
                                self.move_from_to(from_path=f'{path}{self.__path_separator}{index}', to_path=path,
                                                  only_contents=True, existing_keys=existing_keys, index=index)
                                recursive_func()
                                break
                    else:
                        for index, value in enumerate(container):
                            if isinstance(value, list):
                                self.move_from_to(from_path=f'{path}{self.__path_separator}{index}', to_path=path,
                                                  only_contents=True, existing_keys=existing_keys, index=list_index)
                                recursive_func()
                                break

                recursive_func()
                if flatten_opposite_container_type:
                    for i, v in enumerate(container):
                        if isinstance(v, dict):
                            self.flatten(path=f'{path}{self.__path_separator}{i}', chain_key=chain_key,
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
                                                from_path=f'{path}{self.__path_separator}{index}{self.__path_separator}{key}',
                                                to_path=path, only_contents=True, index=list_index)
                                            recursive_func()
                                            break

                        recursive_func()

            if delete_empty_containers:
                self.delete_empty_containers()
        except KeyPathError:
            self.__raise_error__(error=KeyPathError, ignore=ignore_errors)

    @property
    def data(self) -> dict | list | str | float | int | bool | None:
        return self.__data[self.__root]

    def read(self, path: str = '', ignore_errors: bool = None) -> dict | str | list | int | float | bool | None:
        """Returns the value of wherever *path* leads."""

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors

        # main
        try:
            data: tuple = self.__walk_path__(path=path)
            return data[0][data[1]]
        except KeyPathError:
            self.__raise_error__(KeyPathError, ignore_errors)

    def pair(self, path: str, as_dictionary: bool = False, ignore_errors: bool = None) -> tuple | dict:
        """Returns a pair in the form of a tuple (<key>, <value>) or dictionary pair {<key>: <value>}
        from wherever *path* leads."""

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors

        # main
        try:
            data: tuple = self.__walk_path__(path=path)
            if as_dictionary:
                return {data[1]: data[0][data[1]]}
            else:
                return data[1], data[0][data[1]]
        except KeyPathError:
            self.__raise_error__(KeyPathError, ignore_errors)

    def pairs(self, path: str = '', as_dictionaries: bool = False, ignore_errors: bool = None) -> list:
        """Returns a list of tuples of (key, value) pairs - [(key, value), (key, value)..] of the selected level.
        This method is very similar to the items() method of dict."""

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors

        # main
        try:
            data_: tuple = self.__walk_path__(path=path)
            data: dict | str | list | int | float | bool | None = data_[0][data_[1]]
            if isinstance(data, dict):
                if as_dictionaries:
                    return [{k: v} for k, v in data.items()]
                else:
                    return list(data.items())
        except KeyPathError:
            self.__raise_error__(KeyPathError, ignore_errors)

    def key(self, path: str, ignore_errors: bool = None) -> str | int | float | bool | None:
        """Returns the key of the value that *path* leads to. If the value is in a list the values index will be
        returned as an integer."""

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors

        # main
        try:
            return self.__walk_path__(path=path)[1]
        except KeyPathError:
            self.__raise_error__(KeyPathError, ignore_errors)

    def keys(self, path: str = '', ignore_errors: bool = None) -> list:
        """Returns a list of all the of keys in the location that is specified by *path*. If *path* leads
        to a non-container value than it will return the key of that value."""

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors

        # main
        try:
            data: tuple = self.__walk_path__(path=path)
            if isinstance(data[0][data[1]], dict):
                return list(data[0][data[1]])
            elif isinstance(data[0][data[1]], list):
                return [i for d in data[0][data[1]] if isinstance(d, dict) for i in d]
        except KeyPathError:
            self.__raise_error__(KeyPathError, ignore_errors)

    def values(self, path: str = '', only_values_of_pairs: bool = True,
               ignore_errors: bool = None) -> list:
        """Returns a list of all the of values in the location that is specified by *path*. If *path* leads
        to a non-container value than that value will simply be returned."""

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors

        # main
        try:
            data_: tuple = self.__walk_path__(path=path)
            data: dict | str | list | int | float | bool | None = data_[0][data_[1]]
            if isinstance(data, dict):
                return list(data.values())
            elif isinstance(data, list):
                if only_values_of_pairs:
                    return [i for d in data if isinstance(d, dict) for i in d.values()]
                else:
                    return [d for d in data if not isinstance(d, dict)] + [i for d in data if isinstance(d, dict) for i in d.values()]
        except KeyPathError:
            self.__raise_error__(KeyPathError, ignore_errors)

    def all_keys(self, path: str = '', search_lists: bool = True, as_paths: bool = False, ignore_errors: bool = None) -> list:
        """Returns a list of all the keys past a certain point which is specified by *path*. This method only returns0
         keys that have a non-container value"""

        from copy import deepcopy
        data: T4Json = T4Json()

        try:
            data.new(deepcopy(self.read(path=path)))

            if isinstance(data.__data[data.__root], dict):
                if not as_paths:
                    data.flatten(flatten_opposite_container_type=search_lists, pull_pairs_from_lists=search_lists,
                                 pull_lists_from_pairs=True)
                else:
                    current_path_separator: str = data.__path_separator
                    data.set_path_separator_properties(separator='_')
                    data.flatten(chain_key=as_paths, chain_include_index=True, chain_key_separator=current_path_separator,
                                 flatten_opposite_container_type=search_lists, pull_pairs_from_lists=search_lists,
                                 pull_lists_from_pairs=True)
            elif isinstance(data.__data[data.__root], list):
                data.flatten()
                out: T4Json = T4Json()
                for d in data.__data[data.__root]:
                    if isinstance(d, dict):
                        out.add(value=d, existing_keys='combine')
                data.new(out.__data[data.__root])
                if not as_paths:
                    data.flatten(flatten_opposite_container_type=search_lists, pull_pairs_from_lists=search_lists,
                                 pull_lists_from_pairs=True)
                else:
                    current_path_separator: str = data.__path_separator
                    data.set_path_separator_properties(separator='_')
                    data.flatten(chain_key=as_paths, chain_include_index=True, chain_key_separator=current_path_separator,
                                 flatten_opposite_container_type=search_lists, pull_pairs_from_lists=search_lists,
                                 pull_lists_from_pairs=True)

            return list(data.__data[data.__root])

        except (KeyPathError, AddError):
            data.__raise_error__(ValueError('there was a problem while searching through the JSON data.'),
                                 ignore_errors)
        except AttributeError:
            pass

    def all_values(self, path: str = '', search_lists: bool = True, ignore_errors: bool = None) -> list:
        """Returns a list of all the of values in the location that is specified by *path*. If *path* leads to a
        non-container value than that value will simply be returned."""

        from copy import deepcopy
        data: T4Json = T4Json()

        try:
            data.new(deepcopy(self.read(path=path)))

            if isinstance(data.__data[data.__root], dict):
                data.flatten(flatten_opposite_container_type=search_lists, pull_pairs_from_lists=search_lists,
                             pull_lists_from_pairs=True)
            elif isinstance(data.__data[data.__root], list):
                data.flatten()
                out: T4Json = T4Json()
                for d in data.__data[data.__root]:
                    if isinstance(d, dict):
                        out.add(value=d, existing_keys='combine')
                data.new(out.__data[data.__root])
                data.flatten(flatten_opposite_container_type=search_lists, pull_pairs_from_lists=search_lists,
                             pull_lists_from_pairs=True)

            return list(data.__data[data.__root].values())

        except (KeyPathError, AddError):
            data.__raise_error__(ValueError('there was a problem while searching through the JSON data.'),
                                 ignore_errors)
        except AttributeError:
            pass

    def all_pairs(self, path: str = '', search_lists: bool = True, as_dictionaries: bool = False, ignore_errors: bool = None) -> list:
        """Returns a list of tuples of all (key, value) pairs as - [(key, value), (key, value)..] past a point
        specified by *path*."""

        from copy import deepcopy
        data: T4Json = T4Json()

        try:
            data.new(deepcopy(self.read(path=path)))

            if isinstance(data.__data[data.__root], dict):
                data.flatten(flatten_opposite_container_type=search_lists, pull_pairs_from_lists=search_lists,
                             pull_lists_from_pairs=True)
            elif isinstance(data.__data[data.__root], list):
                data.flatten()
                out: T4Json = T4Json()
                for d in data.__data[data.__root]:
                    if isinstance(d, dict):
                        out.add(value=d, existing_keys='combine')
                data.new(out.__data[data.__root])
                data.flatten(flatten_opposite_container_type=search_lists, pull_pairs_from_lists=search_lists,
                             pull_lists_from_pairs=True)

            return data.pairs(as_dictionaries=as_dictionaries)

        except (KeyPathError, AddError):
            data.__raise_error__(ValueError('there was a problem while searching through the JSON data.'),
                                 ignore_errors)
        except AttributeError:
            pass

    def search(self, key: str, path: str = '', search_list: bool = True,
               ignore_errors: bool = None) -> list | dict | str | int | float | bool | None:
        """Searches through all the JSON data or (past a certain point specified by *path*) for *key*. If there are
        multiple keys with the same name spread throughout the data, a list of their all there values will be returned."""

        from copy import deepcopy

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors

        # main
        data: T4Json = T4Json()
        try:
            data.new(deepcopy(self.read(path=path)))

            if isinstance(data.__data[data.__root], dict):
                data.flatten(flatten_opposite_container_type=search_list, pull_pairs_from_lists=search_list,
                             pull_lists_from_pairs=True)
            elif isinstance(data.__data[data.__root], list):
                data.flatten()
                out: T4Json = T4Json()
                for d in data.__data[data.__root]:
                    if isinstance(d, dict):
                        out.add(value=d, existing_keys='combine')
                data.new(out.__data[data.__root])
                data.flatten(flatten_opposite_container_type=search_list, pull_pairs_from_lists=search_list,
                             pull_lists_from_pairs=True)

            return data.read(path=key)

        except (KeyPathError, AddError, AttributeError):
            data.__raise_error__(ValueError('there was a problem while searching through the JSON data.'),
                                 ignore_errors)
        except AttributeError:
            pass

    def json_string(self, path: str = '', indent: int | str = None, sort_keys: bool = None, only_ascii: bool = None,
                    separators: tuple = None, ignore_errors: bool = None) -> str:
        """Returns a JSON formatted string. This string can then... for example be saved to a file."""

        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors
        if indent is None:
            indent: int | str | None = self.indentation
        if sort_keys is None:
            sort_keys: bool | None = self.sort_keys
        if only_ascii is None:
            only_ascii: bool = self.only_ascii
        if separators is None:
            separators: tuple = self.__json_separators
        return json.dumps(self.read(path=path, ignore_errors=ignore_errors), skipkeys=True, indent=indent,
                          sort_keys=sort_keys, ensure_ascii=only_ascii, separators=separators)

    def set_working_level(self, path: str = '', ignore_errors: bool = None) -> None:
        """Sets the working level within a nested data structure."""

        # parameter setup
        if ignore_errors is None:
            ignore_errors: bool = self.ignore_method_errors

        # main
        try:
            if self.is_path_relative(path):
                path: str = self.__interpret_path__(path, return_as_str=True)

            if isinstance(self.read(path=path), (dict, list)):
                self.__working_level: str = path
            else:
                self.__working_level: str = self.__path_separator.join(path.split(self.__path_separator)[:-1])
        except KeyPathError:
            self.__raise_error__(error=KeyPathError, ignore=ignore_errors)

    def set_indentation(self, indentation: int | str | None) -> None:
        """Sets the indentation of the JSON file which will be applied when it is saved/serialized."""
        self.indentation: int | str | None = indentation

    def set_sort_keys(self, boolean: bool) -> None:
        """Keys will be sorted in alphabetical/numerical order. This will be applied when the file is saved/serialized."""
        self.sort_keys: bool = boolean

    def set_only_ascii(self, boolean: bool) -> None:
        """Any non-ascii characters will be escaped/encoded. This will be applied when the file is saved/serialized."""
        self.only_ascii: bool = boolean

    def set_ignore_errors(self, boolean: bool) -> None:
        """Any non-critical errors (such as the path being incorrect) will be ignored."""
        self.ignore_method_errors: bool = boolean

    def set_path_separator_properties(self, separator: str = None, relative: str = None, relative_back: str = None) -> None:
        """Sets the path separator and relative path navigation properties."""

        # parameter setup
        if separator is None:
            separator: str = self.__path_separator
        if relative is None:
            relative: str = self.__relative_path_command
        if relative_back is None:
            relative_back: str = self.__relative_back_path_command

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
            self.__path_separator: str = separator

    def set_json_separators(self, item_separator: str = None, key_value_separator: str = None) -> None:
        """Sets the pair and item separator properties for the JSON data when it is saved/serialized.
        The most compact arguments would be ("," and ":") instead of the default (", " and ": ")."""

        if item_separator is None:
            item_separator: str = self.__json_separators[0]
        if key_value_separator is None:
            key_value_separator: str = self.__json_separators[1]

        self.__json_separators: tuple = (item_separator, key_value_separator)

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
        return self.__working_level

    def get_indentation(self) -> int | str | None:
        """Returns the indentation property. An int, str or None can be expected."""
        return self.indentation

    def get_path_separator_properties(self) -> tuple:
        """Returns the current path separator properties."""
        return self.__path_separator, self.__relative_path_command, self.__relative_back_path_command

    def reset_settings(self) -> None:
        """Resets any settings that have been changed... back to their original default values."""

        # user_settings
        self.ignore_method_errors: bool = False
        self.indentation: int | str | None = 4
        self.sort_keys: bool = False
        self.only_ascii: bool = False

        # off limit __vars__
        self.__json_separators: tuple = (', ', ': ')  # index 0 is for items and index 1 is for JSON objects
        self.__path_separator: str = '\\\\'
        self.__relative_path_command: str = ''
        self.__relative_back_path_command: str = '..'
        self.__working_level: str | None = None

    def is_path_existent(self, path) -> bool:
        """Checks to see if *path* exist in the currently opened data structure. True is return if it
        does exist... and False otherwise."""

        try:
            self.__walk_path__(path)
            return True
        except KeyPathError:
            return False

    def is_path_relative(self, path: str = '') -> bool:
        """Checks to see if *path* is a relative path. True is returned if it is... and False otherwise."""

        if path == '':
            return False
        else:
            if path in ('.', '..'):
                return True
            elif path.startswith(self.__relative_back_path_command + self.__path_separator) or path.startswith(self.__relative_path_command + self.__path_separator):
                return True
            else:
                return False

    def load(self, source: str, url_parameters: dict | list | bytes = None, url_headers: any = None, url_user_auth: any = None, create: bool = False, encoding: str = 'utf-8', encoding_errors: str = 'ignore', decode_html_entities: bool = False) -> None:
        """This method loads the JSON data. It can receive a File Path, URL, or JSON String."""
        from os.path import exists as file_path_exists
        if file_path_exists(source):
            self.load_file(file_path=source, create=create, encoding=encoding, encoding_errors=encoding_errors,
                           decode_html_entities=decode_html_entities)
        elif source.startswith('http'):
            self.load_from_url(url=source, url_parameters=url_parameters, url_headers=url_headers, url_user_auth=url_user_auth,
                               encoding=encoding, encoding_errors=encoding_errors,
                               decode_html_entities=decode_html_entities)
        else:
            self.load_from_string(string=source, encoding=encoding, encoding_errors=encoding_errors,
                                  decode_html_entities=decode_html_entities)

    def load_file(self, file_path: str, create: bool = False, encoding: str = 'utf-8', encoding_errors: str = 'ignore', decode_html_entities: bool = False) -> None:
        """Loads the JSON data from a specified file."""

        try:
            with open(file_path, 'r', encoding=encoding, errors=encoding_errors) as file:
                if decode_html_entities:
                    self.load_from_string(string=file.read(), decode_html_entities=decode_html_entities)
                else:
                    data: dict | list = json.load(file)
            self.__data: dict = {self.__root: data}  # deserialize JSON data into object type dict
            self.set_working_level('')
            self.__file_path: str = file_path
        except FileNotFoundError:
            if create:
                with open(file_path, 'w', encoding=encoding, errors=encoding_errors) as new_file:
                    json.dump({}, new_file)
                self.load_file(file_path=file_path, create=create, encoding=encoding, encoding_errors=encoding_errors)
            else:
                raise LoadFileError(
                    'File does not exist - Set the <create> argument to True so that if a file does not exist it will '
                    'be created.')
        except BaseException:
            raise LoadFileError(
                'There was an error retrieving the JSON data from file. It may be corrupted or <encoding> could be incorrect.')

    def load_from_string(self, string: str | bytes, encoding: str = 'utf-8', encoding_errors: str = 'ignore', decode_html_entities: bool = False) -> None:
        """Loads JSON data from a string."""

        try:
            if isinstance(string, bytes):
                string: str = string.decode(encoding=encoding, errors=encoding_errors)
            if decode_html_entities:
                data: dict | list = json.loads(self.__decode_html_entities(string))
            else:
                data: dict | list = json.loads(string)
            self.__data: dict = {self.__root: data}  # deserialize JSON data into object type dict
            self.set_working_level('')
            self.__file_path: str | None = None
        except BaseException:
            raise LoadStringError

    def load_from_url(self, url: str, url_parameters: dict | list | bytes = None, url_headers: dict = None, url_user_auth: any = None, encoding: str = 'utf-8', encoding_errors: str = 'ignore', decode_html_entities: bool = False) -> None:
        """Loads JSON data from the specified URL."""
        from requests import get as geturl

        try:
            if decode_html_entities:
                data: dict | list = json.loads(self.__decode_html_entities(geturl(url=url, params=url_parameters, auth=url_user_auth).content.decode(encoding=encoding, errors=encoding_errors)))
            else:
                data: dict | list = json.loads(geturl(url=url, params=url_parameters, headers=url_headers, auth=url_user_auth).content.decode(encoding=encoding, errors=encoding_errors))
            self.__data: dict = {self.__root: data}  # deserialize JSON data into object type dict
            self.set_working_level('')
            self.__file_path: str | None = None
        except BaseException:
            raise LoadURLError

    def save(self, indent: int | str = None, sort_keys: bool = None, only_ascii: bool = None, separators: tuple = None,
             encoding: str = 'utf-8', encoding_errors: str = 'strict') -> None:
        """Saves the currently opened file if a file is opened."""

        if self.__file_path is not None:
            if indent is None:
                indent: int | str | None = self.indentation
            if sort_keys is None:
                sort_keys: bool | None = self.sort_keys
            if only_ascii is None:
                only_ascii: bool = self.only_ascii
            if separators is None:
                separators: tuple = self.__json_separators
            with open(self.__file_path, 'w', encoding=encoding, errors=encoding_errors) as file:
                json.dump(obj=self.__data[self.__root], fp=file, skipkeys=True, indent=indent, sort_keys=sort_keys,
                          ensure_ascii=only_ascii, separators=separators)

    def save_as(self, file_path: str, overwrite: bool = False, indent: int | str = None, sort_keys: bool = None,
                only_ascii: bool = None, separators: tuple = None, encoding: str = 'utf-8',
                encoding_errors: str = 'strict') -> None:
        """Saves the current JSON data as a new file."""
        from os.path import exists as file_path_exists

        if indent is None:
            indent: int | str | None = self.indentation
        if sort_keys is None:
            sort_keys: bool | None = self.sort_keys
        if only_ascii is None:
            only_ascii: bool = self.only_ascii
        if separators is None:
            separators: tuple = self.__json_separators

        if not file_path_exists(file_path) or overwrite:
            with open(file_path, 'w', encoding=encoding, errors=encoding_errors) as file:
                json.dump(obj=self.__data[self.__root], fp=file, skipkeys=True, indent=indent, sort_keys=sort_keys,
                          ensure_ascii=only_ascii, separators=separators)
        else:
            raise FileExistsError('<new_file> must not already exist.\nSet the <overwrite> argument to True so that'
                                  'if a file already does exist it will be overwritten and no exception will '
                                  'be thrown.')

    def new(self, value: dict | str | list | tuple | int | float | bool | None) -> None:
        """Receives whatever is passed to *value* as the new JSON data to work with."""

        self.__data[self.__root] = value
        self.set_working_level('')
        self.__file_path: str | None = None

    def close(self) -> None:
        """Simply closes the data that's already open and leaves you with an empty dictionary."""

        self.new({})
        self.__file_path: str | None = None

    @staticmethod
    def __raise_error__(error: object, ignore: bool = False, from_none: bool = False) -> None:
        if not ignore:
            if from_none:
                raise error from None
            else:
                raise error

    @staticmethod
    def __decode_html_entities(string: str) -> str:
        from html import unescape as decode_html
        return decode_html(string.replace('&quot;', r'\"'))

    def __interpret_path__(self, path: str, working_level: str = None, return_as_str: bool = False) -> list | str:
        """Receives a path as relative or absolute and then always returns the absolute version of the path as a list"""
        # parameter setup
        if working_level is None:
            working_level: str = self.__working_level
        if path == '.':
            path: str = self.__working_level
        elif path == '..':
            path: str = self.__working_level.rpartition(self.__path_separator)[0]

        # main
        back: str = self.__relative_back_path_command + self.__path_separator
        working: str = self.__relative_path_command + self.__path_separator
        try:
            if path.startswith(back):  # if going back

                left_count = 0
                for b in path.split(self.__path_separator):
                    if b == self.__relative_back_path_command:
                        left_count += 1
                    else:
                        break
                out: list = working_level.split(self.__path_separator)[:-left_count] + path.split(self.__path_separator)[left_count:]

            elif path.startswith(working):  # if work at current working level
                out: list = working_level.split(self.__path_separator) + path.split(self.__path_separator)[1:]

            else:  # if absolute path

                if return_as_str:
                    return path
                out: list = path.split(self.__path_separator)

            if return_as_str:
                return self.__path_separator.join(out)
            else:
                return out
        except AttributeError:
            raise KeyPathError

    def __walk_path__(self, path: str) -> tuple:
        """return the parent container along with the key in a tuple to access its value - (container, key)."""

        # parameter setup
        if path == '' and not self.is_path_relative(path):
            return self.__data, self.__root

        # path setup
        path_: list = self.__interpret_path__(path)

        # functions
        def alien_key(k: str) -> float | bool | None:
            try:
                return float(k)
            except ValueError:
                if k == 'True':
                    return True
                elif k == 'False':
                    return False
                elif k == 'None':
                    return None
                else:
                    raise KeyError

        # main
        try:
            if not path_[0] == '':
                parent_of_target_level: dict | list = self.__data[self.__root]  # level iterator... used to assign each level as it walks down the data structure.
            else:
                parent_of_target_level: dict = self.__data  # level iterator... used to assign each level as it walks down the data structure.

            for key in path_[:-1]:  # loop through path all the way down to the parent of the target level
                if isinstance(parent_of_target_level, dict):  # if parent of the target level is a dictionary
                    try:
                        parent_of_target_level: dict | list = parent_of_target_level[key]
                    except KeyError:
                        parent_of_target_level: dict | list = parent_of_target_level[alien_key(key)]
                else:  # if parent of the target level is a list
                    parent_of_target_level: dict | list = parent_of_target_level[int(key)]

            target_level_key: str = path_[-1]
            # Return level

            def catch_invalid_path(target_key) -> any: return parent_of_target_level[target_key]
            if isinstance(parent_of_target_level, dict):
                try:  # since the target level is not checked in the for loop check it here
                    catch_invalid_path(target_level_key)
                except KeyError:
                    try:
                        catch_invalid_path(float(target_level_key))
                        target_level_key: float = float(target_level_key)
                    except ValueError:
                        if target_level_key == 'True':
                            catch_invalid_path(True)
                            target_level_key: bool = True
                        elif target_level_key == 'False':
                            catch_invalid_path(False)
                            target_level_key: bool = False
                        elif target_level_key == 'None':
                            catch_invalid_path(None)
                            target_level_key: None = None
                        else:
                            raise KeyError

                return parent_of_target_level, target_level_key
            else:  # elif - is list
                catch_invalid_path(int(target_level_key))  # since the target level is not checked in the for loop check it here
                return parent_of_target_level, int(target_level_key)
        except (KeyError, ValueError, TypeError, IndexError):
            raise KeyPathError


class LoadFileError(Exception):
    def __init__(self, message: str = None) -> None:
        if message is None:
            super().__init__('JSON data could not be loaded.'
                             '\nSome things that may have gone wrong:'
                             '\n\t1. A file that does not exist was attempting to be loaded. - Set the <create> '
                             'argument to True so that if a file does not exist it will be created.'
                             '\n\t2. JSON data could be corrupted.'
                             '\n\t3. There could be encoding issues that are corrupting the data.')


class LoadURLError(Exception):
    def __init__(self, message: str = None) -> None:
        if message is None:
            super().__init__('JSON data could not be retrieved from <url>.'
                             '\nSome things that may have gone wrong:'
                             '\n\t1. Access was denied, URL does not exist or there are connection issues.'
                             '\n\t2. JSON data could be corrupted.'
                             '\n\t3. There could be encoding issues that are corrupting the data.')


class LoadStringError(Exception):
    def __init__(self, message: str = None) -> None:
        if message is None:
            super().__init__('JSON data could not be loaded from <string>.'
                             '\nSome things that may have gone wrong:'
                             '\n\t1. JSON data is corrupted.'
                             '\n\t2. There could be encoding issues that are corrupting the data.')


LoadError: tuple = (LoadFileError, LoadURLError, LoadStringError)


class KeyPathError(Exception):
    def __init__(self, message: str = None) -> None:
        if message is None:
            super().__init__('\n<path> is an invalid structure path.\nSome things that may have gone wrong:'
                             '\n\t1. The path may lead to a list... Integer characters must be used as an index to '
                             'gain access to any list within the data structure.\n\t2. The path may not exist.'
                             '\n\t3. Keys within the JSON file may contain the same characters used as the path '
                             'separator properties... if that is the case change the path separator properties using '
                             '<self.set_path_separator_properties()>.\n\t4. The path separator properties may have '
                             'been typed incorrectly or changed.\n\t5. There may be a key being used that is not supported.')


class AddError(Exception):
    def __init__(self, message: str = None) -> None:
        if message is None:
            super().__init__('(<value> cannot be added because <structure_path> leads to a mutable object.)'
                             ' - OR - (A non-JSON object/pair was attempting to be add to a JSON container.)'
                             '\nSet the <create> argument to True so that a list will automatically be created '
                             'including the unsupported object and the new <value>.')


class ArgumentError(Exception):
    pass


def is_valid_json_data(source: str) -> bool:
    """This function returns ```True``` if the JSON data is valid. Otherwise, it returns ```False```."""

    try:
        T4Json(source=source)
        return True
    except LoadError:
        return False


def convert_to_valid_json_ready_data(value: dict | list | tuple | str | float | int | bool | None) -> dict | list | str | float | int | bool | None:
    """Converts *value* into JSON ready data. It will remove any unsupported keys and convert the keys that are not string into strings."""

    if isinstance(value, (dict, list, tuple)):
        return json.loads(json.dumps(obj=value, skipkeys=True))
    else:
        return value


def deserialize_from_string(string: str) -> dict | list | str | int | float | bool | None:
    """Loads JSON data from a *string* and returns the python data structure."""
    return json.loads(string)


def serialize_to_string(value: dict | list | str | int | float | bool | None, indent: None | int | str = None, sort_keys: bool = False, only_ascii: bool = False, separators: tuple = (', ', ': ')) -> str:
    """Returns a JSON formatted string from *value*. This string can then... for example be saved to a file."""
    return json.dumps(value, skipkeys=True, ensure_ascii=only_ascii, sort_keys=sort_keys, indent=indent, separators=separators)
