#!/usr/bin/env python2.5
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

"""This module contains the Organization Model.
"""

__authors__ = [
  '"Pawel Solyga" <pawel.solyga@gmail.com>',
]


from google.appengine.ext import db

from django.utils.translation import ugettext

import soc.models.group


class Organization(soc.models.group.Group):
  """Organization details.
  """

  #: Optional development mailing list.     
  dev_mailing_list = db.StringProperty(required=False,
    verbose_name=ugettext('Development Mailing List'))
  dev_mailing_list.help_text = ugettext(
    'Mailing list email address, URL to sign-up page, etc.')

  contrib_template = db.TextProperty(required=False, verbose_name=ugettext(
      'Application template'))
  contrib_template.help_text = ugettext(
      'This template can be used by contributors, such as students'
      ' and other non-member participants, when they apply to contribute'
      ' to the organization.')

  ideas = db.LinkProperty(required=False, verbose_name=ugettext('Ideas list'))
  ideas.help_text = ugettext(
      'The URL to the ideas list of your organization.')
  ideas.example_text = ugettext('For instance a link to a Melange public '
      'document or some other URL')

