#!/usr/bin/env python2.5
#
# Copyright 2009 the Melange authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module containing some basic caching functions.
"""

__authors__ = [
    '"Sverre Rabbelier" <sverre@rabbelier.nl>',
  ]


from functools import wraps


def getCacher(get, put):
  """Returns a caching decorator that uses get and put.
  """

  # TODO(SRabbelier) possibly accept 'key' instead, and define
  # get and put in terms of key, depends on further usage

  def cache(func):
    """Decorator that caches the result from func.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
      """Decorator wrapper method.
      """
      result, key = get(*args, **kwargs)
      if result:
        return result

      result = func(*args, **kwargs)

      if key:
        put(result, key, *args, **kwargs)

      return result

    return wrapper

  return cache
