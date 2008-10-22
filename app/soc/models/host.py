#!/usr/bin/python2.5
#
# Copyright 2008 the Melange authors.
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

"""This module contains the Host Model."""

__authors__ = [
  '"Todd Larsen" <tlarsen@google.com>',
  '"Sverre Rabbelier" <sverre@rabbelier.nl>',
]


from google.appengine.ext import db

import soc.models.role
import soc.models.sponsor


class Host(soc.models.role.Role):
  """Host details for a specific Program.
  """

  KEY_FIELDS = ['sponsor_ln', 'user_ln']

  #: A 1:1 relationship associating a Host with specific
  #: Sponsor details and capabilities. The back-reference in
  #: the Sponsor model is a Query named 'host'.  
  sponsor = db.ReferenceProperty(reference_class=soc.models.sponsor.Sponsor,
                                 required=True, collection_name='hosts')

  def _get_link_name(self):
    return self.sponsor.link_name

  def _set_link_name(self, value):
    self.sponsor.link_name = value

  sponsor_ln = property(_get_link_name, _set_link_name)

