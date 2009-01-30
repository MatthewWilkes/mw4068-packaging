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

"""This module contains the Document Model."""

__authors__ = [
  '"Pawel Solyga" <pawel.solyga@gmail.com>',
  '"Sverre Rabbelier" <sverre@rabbelier.nl>',
]


from google.appengine.ext import db

from django.utils.translation import ugettext

import soc.models.work


class Document(soc.models.work.Work):
  """Model of a Document.
  
  Document is used for things like FAQs, front page text, etc.

  The specific way that the properties and relations inherited from Work
  are used with a Document are described below.

    work.title:  the title of the Document

    work.reviews:  reviews of the Document by Reviewers

    work.content:  the rich-text contents of the Document
  """

  URL_NAME = 'document'

  #: field storing the prefix of this document
  prefix = db.StringProperty(default='user',
      choices=['site','sponsor','program', 'club', 'organization', 'user'],
      verbose_name=ugettext('Prefix'))
  prefix.help_text = ugettext(
      'Indicates the prefix of the document,'
      ' determines which access scheme is used.')

  #: field storing the access status of this document
  # wiki = any user can read and write the document
  # public = any user can read, only restricted can write
  # member = member can read, only restricted can write
  # restricted = restricted can read, only admin can write
  # admin = admin can read, only admin can write
  #
  # example meanings for an organisations:
  # admin = ['org_admin']
  # restricted = ['org_admin', 'org_mentor']
  # member = ['org_admin', 'org_mentor', 'org_student']
  # public = anyone
  # wiki = anyone
  access_status = db.StringProperty(default='restricted', required=True,
      choices=['admin','restricted', 'member', 'public', 'wiki'],
      verbose_name=ugettext('Access type'))
  access_status.help_text = ugettext(
      'Indicates the state of the document, '
      'determines the access scheme.')

  #: field storing whether a link to the Document should be featured in
  #: the sidebar menu (and possibly elsewhere); FAQs, Terms of Service,
  #: and the like are examples of "featured" Document
  is_featured = db.BooleanProperty(
      verbose_name=ugettext('Is Featured'))
  is_featured.help_text = ugettext(
      'Field used to indicate if a Work should be featured, for example,'
      ' in the sidebar menu.')
