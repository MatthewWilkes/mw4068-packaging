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

"""Views for Documents.
"""

__authors__ = [
    '"Sverre Rabbelier" <sverre@rabbelier.nl>',
    '"Lennard de Rijk" <ljvderijk@gmail.com>',
    '"Pawel Solyga" <pawel.solyga@gmail.com>',
  ]


from django import forms

from soc.logic import cleaning
from soc.logic import dicts
from soc.logic.models.document import logic as document_logic
from soc.logic.models.user import logic as user_logic
from soc.views.helper import access
from soc.views.helper import decorators
from soc.views.helper import redirects
from soc.views.helper import widgets
from soc.views.models import base


class View(base.View):
  """View methods for the Document model.
  """

  def __init__(self, params=None):
    """Defines the fields and methods required for the base View class
    to provide the user with list, public, create, edit and delete views.

    Params:
      params: a dict with params for this View
    """

    rights = access.Checker(params)
    rights['any_access'] = ['allow']
    rights['show'] = ['checkIsDocumentReadable']
    rights['create'] = ['checkIsUser']
    rights['edit'] = ['checkIsDocumentWritable']
    rights['delete'] = ['checkIsDocumentWritable']
    rights['list'] = ['checkDocumentList']
    rights['pick'] = ['checkDocumentPick']

    new_params = {}
    new_params['logic'] = document_logic
    new_params['rights'] = rights

    new_params['name'] = "Document"
    new_params['pickable'] = True

    new_params['export_content_type'] = 'text/text'
    new_params['export_extension'] = '.html'
    new_params['export_function'] = lambda x: (x.content, x.link_id)
    new_params['delete_redirect'] = '/'

    new_params['no_create_raw'] = True
    new_params['no_create_with_scope'] = True
    new_params['no_create_with_key_fields'] = True
    new_params['no_list_raw'] = True
    new_params['sans_link_id_create'] = True
    new_params['sans_link_id_list'] = True

    new_params['create_dynafields'] = [
        {'name': 'link_id',
         'base': forms.fields.CharField,
         'label': 'Document Link ID',
         },
        ]

    new_params['create_extra_dynaproperties'] = {
        'content': forms.fields.CharField(
            widget=widgets.FullTinyMCE(attrs={'rows': 25, 'cols': 100})),
        'scope_path': forms.fields.CharField(widget=forms.HiddenInput,
                                             required=True),
        'prefix': forms.fields.CharField(widget=widgets.ReadOnlyInput(),
                                        required=True),
        'clean_content': cleaning.clean_html_content('content'),
        'clean_link_id': cleaning.clean_link_id('link_id'),
        'clean_scope_path': cleaning.clean_scope_path('scope_path'),
        'clean': cleaning.validate_document_acl(self, True),
        }
    new_params['extra_dynaexclude'] = ['author', 'created', 'home_for',
                                       'modified_by', 'modified']

    new_params['edit_extra_dynaproperties'] = {
        'doc_key_name': forms.fields.CharField(widget=forms.HiddenInput),
        'created_by': forms.fields.CharField(
            widget=widgets.ReadOnlyInput(), required=False),
        'last_modified_by': forms.fields.CharField(
            widget=widgets.ReadOnlyInput(), required=False),
        'clean': cleaning.validate_document_acl(self),
        }

    new_params['public_field_prefetch'] = ['author']
    new_params['public_field_extra'] = lambda entity: {
        'path': entity.scope_path + '/' + entity.link_id,
        'author_id': entity.author.link_id,
    }
    new_params['public_field_keys'] = ["path", "title", "link_id",
                                       "is_featured", "author_id", "created",
                                       "modified"]
    new_params['public_field_names'] = ["Path", "Title", "Link ID", "Featured",
                                        "Created By", "Created On", "Modified"]

    params = dicts.merge(params, new_params)

    super(View, self).__init__(params=params)

  def list(self, request, access_type, page_name=None, params=None,
           filter=None, order=None, **kwargs):
    """See base.View.list.
    """

    return super(View, self).list(request, access_type, page_name=page_name,
                                  params=params, filter=kwargs)

  def _public(self, request, entity, context):
    """Performs any processing needed for the Document's public page.

    For args see base.View._public().
    """

    # check if the current user is allowed to visit the edit page
    rights = self._params['rights']

    allowed_to_edit = False
    try:
      # use the IsDocumentWritable check because we have no django args
      rights.checkIsDocumentWritable({'key_name': entity.key().name(),
                                      'prefix': entity.prefix,
                                      'scope_path': entity.scope_path,
                                      'link_id': entity.link_id},
                                     'key_name')
      allowed_to_edit = True
    except:
      pass

    if allowed_to_edit:
      # add the document edit redirect to the context
      context['edit_redirect'] = redirects.getEditRedirect(
          entity, {'url_name': 'document'})

    return super(View, self)._public(request, entity, context)

  def _edit(self, request, entity, context, params):
    """Hook for edit View.

    Adds the title of the document to the edit View.

    For args see base.View._edit().
    """

    context['page_name'] = "%s titled '%s'" % (context['page_name'],
                                               entity.title)

    return super(View, self)._edit(request, entity, context, params)

  def _editPost(self, request, entity, fields):
    """See base.View._editPost().
    """

    user = user_logic.getForCurrentAccount()

    if not entity:
      fields['author'] = user
    else:
      fields['author'] = entity.author

    fields['modified_by'] = user

    super(View, self)._editPost(request, entity, fields)

  def _editGet(self, request, entity, form):
    """See base.View._editGet().
    """

    form.fields['created_by'].initial = entity.author.name
    form.fields['last_modified_by'].initial = entity.modified_by.name
    form.fields['doc_key_name'].initial = entity.key().id_or_name()

    super(View, self)._editGet(request, entity, form)

  def getMenusForScope(self, entity, params):
    """Returns the featured menu items for one specific entity.

    A link to the home page of the specified entity is also included.

    Args:
      entity: the entity for which the entry should be constructed
      params: a dict with params for this View.
    """

    filter = {
        'prefix' : params['document_prefix'],
        'scope_path': entity.key().id_or_name(),
        'is_featured': True,
        }

    entities = self._logic.getForFields(filter)

    submenus = []

    # add a link to the home page
    submenu = (redirects.getHomeRedirect(entity, params), 'Home', 'allow')
    submenus.append(submenu)

    # add a link to all featured documents
    for entity in entities:
      #TODO only if a document is readable it might be added
      submenu = (redirects.getPublicRedirect(entity, self._params),
                 entity.short_name, 'show')
      submenus.append(submenu)

    return submenus


view = View()

admin = decorators.view(view.admin)
create = decorators.view(view.create)
edit = decorators.view(view.edit)
delete = decorators.view(view.delete)
list = decorators.view(view.list)
public = decorators.view(view.public)
export = decorators.view(view.export)
pick = decorators.view(view.pick)
