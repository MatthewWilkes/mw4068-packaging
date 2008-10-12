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

"""Developer views for listing Documents.
"""

__authors__ = [
  '"Todd Larsen" <tlarsen@google.com>',
  ]


import soc.logic
from soc.logic.helper import access
from soc.views import simple
from soc.views import helper
import soc.views.helper.lists
import soc.views.helper.responses

import soc.models.document


DEF_SITE_DOCS_LIST_ALL_TMPL = 'soc/site/docs/list/all.html'

def all(request, template=DEF_SITE_DOCS_LIST_ALL_TMPL):
  """Show a list of all Documents (limit rows per page).
  
  Args:
    request: the standard Django HTTP request object
    template: the "sibling" template (or a search list of such templates)
      from which to construct an alternate template name (or names)

  Returns:
    A subclass of django.http.HttpResponse which either contains the form to
    be filled out, or a redirect to the correct view in the interface.
  """

  try:
    access.checkIsDeveloper(request)
  except  soc.logic.out_of_band.AccessViolationResponse, alt_response:
    return alt_response.response()

  # create default template context for use with any templates
  context = helper.responses.getUniversalContext(request)

  offset, limit = helper.lists.cleanListParameters(
      offset=request.GET.get('offset'), limit=request.GET.get('limit'))

  # Fetch one more to see if there should be a 'next' link
  docs = soc.logic.work_logic.getForLimitAndOffset(limit + 1, offset=offset)

  context['pagination_form'] = helper.lists.makePaginationForm(request, limit)

  list_templates = {'list_main': 'soc/list/list_main.html',
                    'list_pagination': 'soc/list/list_pagination.html',
                    'list_row': 'soc/site/docs/list/docs_row.html',
                    'list_heading': 'soc/site/docs/list/docs_heading.html'}
                      
  context = helper.lists.setList(
      request, context, docs, 
      offset=offset, limit=limit, list_templates=list_templates)

  return helper.responses.respond(request, template, context)
