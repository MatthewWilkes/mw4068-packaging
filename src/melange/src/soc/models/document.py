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

"""This module contains the Document Model."""

__authors__ = [
  '"Madhusudan.C.S" <madhusudancs@gmail.com>',
  '"Pawel Solyga" <pawel.solyga@gmail.com>',
  '"Sverre Rabbelier" <sverre@rabbelier.nl>',
]


from google.appengine.ext import db

from django.utils.translation import ugettext

import soc.models.linkable
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

  DOCUMENT_ACCESS = ['admin', 'restricted', 'member', 'user']

  #: field storing the prefix of this document
  prefix = db.StringProperty(default='user', required=True,
      choices=['site', 'club', 'sponsor',
               'program', 'ghop_program', 'gsoc_program',
               'org', 'ghop_org', 'gsoc_org',
               'user'],
      verbose_name=ugettext('Prefix'))
  prefix.help_text = ugettext(
      'Indicates the prefix of the document,'
      ' determines which access scheme is used.')

  #: field storing the required access to read this document
  read_access = db.StringProperty(default='public', required=True,
      choices=DOCUMENT_ACCESS + ['public'],
      verbose_name=ugettext('Read Access'))
  read_access.help_text = ugettext(
      'Indicates the state of the document, '
      'determines the access scheme.')

  #: field storing the required access to write to this document
  write_access = db.StringProperty(default='admin', required=True,
      choices=DOCUMENT_ACCESS,
      verbose_name=ugettext('Write Access'))
  write_access.help_text = ugettext(
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

  #: Reference to Document containing the contents of the "/home" page
  home_for = db.ReferenceProperty(
    reference_class=soc.models.linkable.Linkable,
    collection_name='home_docs')
  home_for.help_text = ugettext(
      'The Precense this document is the home document for.')
