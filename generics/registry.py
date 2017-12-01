# Copyright © 2017, Dylan Baker

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library.

import inspect
import typing

# TODO: Any should be replaced, it should be a a class, function, or string
SIGNATURE_TYPE = typing.TypeVar('Signature', typing.Any, None)


class Registry:

    """Class that tracks each function and all possible implementations of that
    generic function.
    """

    registry: typing.Dict[SIGNATURE_TYPE, typing.Callable] = {}

    def __init__(self) -> None:
        self.registry = {}

    def get(self, module: str, name: str, signature: SIGNATURE_TYPE) -> typing.Callable[[typing.Any], typing.Any]:
        """Get a function given a signature, or default. If Default is None
        then a TypeError will be raised.
        """
        try:
            return self.registry[(module, name, signature)]
        except KeyError:
            if self.default is not None:
                return self.default
            raise TypeError(f'Function {name} does not have an implemenation '
                            f'for signature {signature}')

    def register(self, func: typing.Callable[[typing.Any], typing.Any]):
        """Register a new generic for a function."""
        annotations = tuple(x for x in func.__annotations__.items())
        key = (inspect.getsourcefile(func), func.__qualname__, annotations)

        if key in self.registry:
            # XXX: What kind of exception should this raise?
            raise Exception

        self.registry[key] = func
