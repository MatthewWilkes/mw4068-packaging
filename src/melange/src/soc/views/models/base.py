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

"""Helpers functions for displaying views.
"""

__authors__ = [
  '"Daniel Hans" <daniel.m.hans@gmail.com>',
  '"Sverre Rabbelier" <sverre@rabbelier.nl>',
  '"Lennard de Rijk" <ljvderijk@gmail.com>',
  '"Pawel Solyga" <pawel.solyga@gmail.com>',
  ]


import csv
import StringIO

from google.appengine.ext import db

from django import http
from django.utils import simplejson
from django.utils.translation import ugettext

from soc.logic import dicts
from soc.views import helper
from soc.views import out_of_band
from soc.views.helper import decorators
from soc.views.helper import forms
from soc.views.helper import redirects
from soc.views.helper import requests
from soc.views.helper import responses
from soc.views.sitemap import sidebar
from soc.views.sitemap import sitemap

import soc.cache.logic
import soc.logic
import soc.logic.lists
import soc.views.helper.lists
import soc.views.helper.params


class View(object):
  """Views for entity classes.

  The View class functions specific to Entity classes by relying
  on the the child-classes to define the following fields:

  self._logic: the logic singleton for this entity
  """

  DEF_CREATE_NEW_ENTITY_MSG_FMT = ugettext(
      ' You can create a new %(entity_type)s by visiting'
      ' <a href="%(create)s">Create '
      'a New %(entity_type)s</a> page.')

  DEF_CREATE_INSTRUCTION_MSG_FMT = ugettext(
      'Please select a %s for the new %s.')

  def __init__(self, params=None):
    """

    Args:
      params: This dictionary should be filled with the parameters
        specific to this entity. See the methods in this class on
        the fields it should contain, and how they are used.
    """

    self._params = helper.params.constructParams(params)
    self._logic = params['logic']

  @decorators.merge_params
  @decorators.check_access
  def public(self, request, access_type,
             page_name=None, params=None, **kwargs):
    """Displays the public page for the entity specified by **kwargs.

    Params usage:
      rights: The rights dictionary is used to check if the user has
        the required rights to view the public page for this entity.
        See checkAccess for more details on how the rights dictionary
        is used to check access rights.
      error_public: The error_public value is used as template when
        the key values (as defined by the page's url) do not
        correspond to an existing entity.
      name: The name value is used to set the entity_type in the
        context so that the template can refer to it.
      public_template: The public_template value is used as template
        to display the public page of the found entity.

    Args:
      request: the standard Django HTTP request object
      access_type : the name of the access type which should be checked
      page_name: the page name displayed in templates as page and header title
      params: a dict with params for this View
      kwargs: the Key Fields for the specified entity
    """

    # create default template context for use with any templates
    context = helper.responses.getUniversalContext(request)
    helper.responses.useJavaScript(context, params['js_uses_all'])
    context['page_name'] = page_name
    entity = None
    logic = params['logic']

    if not all(kwargs.values()):
      #TODO: Change this into a proper redirect
      return http.HttpResponseRedirect('/')

    try:
      entity = logic.getFromKeyFieldsOr404(kwargs)
    except out_of_band.Error, error:
      return helper.responses.errorResponse(
          error, request, template=params['error_public'], context=context)

    if not self._public(request, entity, context):
      redirect = params['public_redirect']
      if redirect:
        return http.HttpResponseRedirect(redirect)

    context['entity'] = entity
    context['entity_type'] = params['name']
    context['entity_type_url'] = params['url_name']

    context = dicts.merge(params['context'], context)

    template = params['public_template']

    return helper.responses.respond(request, template, context=context)

  @decorators.merge_params
  @decorators.check_access
  def admin(self, request, access_type,
             page_name=None, params=None, **kwargs):
    """Displays the admin page for the entity specified by **kwargs.

    Params usage:
      rights: The rights dictionary is used to check if the user has
        the required rights to view the admin page for this entity.
        See checkAccess for more details on how the rights dictionary
        is used to check access rights.
      name: The name value is used to set the entity_type in the
        context so that the template can refer to it.
      public_template: The public_template value is used as template
        to display the public page of the found entity.

    Args:
      request: the standard Django HTTP request object
      access_type : the name of the access type which should be checked
      page_name: the page name displayed in templates as page and header title
      params: a dict with params for this View
      kwargs: the Key Fields for the specified entity
    """

    # create default template context for use with any templates
    context = helper.responses.getUniversalContext(request)
    helper.responses.useJavaScript(context, params['js_uses_all'])
    context['page_name'] = page_name
    logic = params['logic']

    try:
      entity = logic.getFromKeyFieldsOr404(kwargs)
    except out_of_band.Error, error:
      return helper.responses.errorResponse(error, request, context=context)

    form = params['admin_form'](instance=entity)
    template = params['admin_template']

    return self._constructResponse(request, entity, context, form,
                                   params, template=template)

  @decorators.merge_params
  @decorators.check_access
  def export(self, request, access_type,
             page_name=None, params=None, **kwargs):
    """Displays the export page for the entity specified by **kwargs.

    Params usage:
      rights: The rights dictionary is used to check if the user has
        the required rights to view the export page for this entity.
        See checkAccess for more details on how the rights dictionary
        is used to check access rights.
      error_export: The error_export value is used as template when
        the key values (as defined by the page's url) do not
        correspond to an existing entity.
      Params is passed to download, refer to it's docstring for more
      details on how it uses it.

    Args:
      request: the standard Django HTTP request object
      access_type : the name of the access type which should be checked
      page_name: the page name displayed in templates as page and header title
      params: a dict with params for this View
      kwargs: the Key Fields for the specified entity
    """

    if not ('export_content_type' in params) and ('export_function' in params):
      return self.public(request, access_type, page_name=page_name,
                         params=params, **kwargs)

    # create default template context for use with any templates
    entity = None
    logic = params['logic']

    if not all(kwargs.values()):
      #TODO: Change this into a proper redirect
      return http.HttpResponseRedirect('/')

    try:
      entity = logic.getFromKeyFieldsOr404(kwargs)
    except out_of_band.Error, error:
      return helper.responses.errorResponse(
          error, request, template=params['error_export'])

    export_function = params['export_function']
    data, filename = export_function(entity)

    return self.download(request, data, filename, params)

  def download(self, request, data, filename, params):
    """Returns data as a downloadable file with the specified name.

    Params usage:
      export_template: The export_template value is used as template
        to display the export page of the found entity.
      export_content_type: The export_content_type value is used to set
        the Content-Type header of the HTTP response.  If empty (or None),
        public() is called instead.
      export_extension: The export_extension value is used as the suffix
        of the file that will be offered for download.

    Args:
      request: the standard Django HTTP request object
      data: the data that should be offered as file content
      filename: the name the file should have
      params: a dict with params for this View
    """

    context = {}
    context['data'] = data

    template = params['export_template']

    response_args = {'mimetype': params['export_content_type']}

    export_extension = params['export_extension']

    response_headers = {
        'Content-Disposition': 'attachment; filename=%s%s' % (
            filename, export_extension),
        }

    return helper.responses.respond(request, template, context=context,
                                    response_args=response_args,
                                    response_headers=response_headers)

  @decorators.check_access
  def create(self, request, access_type,
             page_name=None, params=None, **kwargs):
    """Displays the create page for this entity type.

    Params usage:
      The params dictionary is passed on to edit, see the docstring
      for edit on how it uses it.

    Args:
      request: the standard Django HTTP request object
      access_type : the name of the access type which should be checked
      page_name: the page name displayed in templates as page and header title
      params: a dict with params for this View
      kwargs: not used for create()
    """

    params = dicts.merge(params, self._params)

    # redirect to scope selection view
    if ('scope_view' in params) and ('scope_path' not in kwargs):
      view = params['scope_view'].view
      redirect = params['scope_redirect']
      return self.select(request, view, redirect,
                         params=params, page_name=page_name, **kwargs)

    context = helper.responses.getUniversalContext(request)
    helper.responses.useJavaScript(context, params['js_uses_all'])
    context['page_name'] = page_name

    if request.method == 'POST':
      return self.createPost(request, context, params)
    else:
      return self.createGet(request, context, params, kwargs)

  def createGet(self, request, context, params, seed):
    """See editGet.

    Handles generating the patch to create new entities.
    """

    self._editSeed(request, seed)

    if seed:
      # pass the seed through the  context to _constructResponse
      # it will be popped before dispatching to Django
      context['seed'] = seed
      form = params['create_form'](initial=seed)
    else:
      form = params['create_form']()

    return self._constructResponse(request, None, context, form, params)

  @decorators.mutation
  def createPost(self, request, context, params):
    """See editPost.

    Handles the creation of new entities.
    """

    form = params['create_form'](request.POST)

    if not form.is_valid():
      return self._constructResponse(request, None, context, form, params)

    _, fields = forms.collectCleanedFields(form)
    self._editPost(request, None, fields)

    logic = params['logic']
    entity = logic.updateOrCreateFromFields(fields)

    page_params = params['edit_params']
    params['suffix'] = entity.key().id_or_name()

    request.path = params['edit_redirect'] % params

    return helper.responses.redirectToChangedSuffix(
        request, None, params=page_params)

  @decorators.merge_params
  @decorators.check_access
  def edit(self, request, access_type,
           page_name=None, params=None, seed=None, **kwargs):
    """Displays the edit page for the entity specified by **kwargs.

    Params usage:
      The params dictionary is passed on to either editGet or editPost
      depending on the method type of the request. See the docstring
      for editGet and editPost on how they use it.

      rights: The rights dictionary is used to check if the user has
        the required rights to edit (or create) a new entity.
        See checkAccess for more details on how the rights dictionary
        is used to check access rights.
      name: The name value is used to construct the message_fmt of the
        raised error when there key_values do not define an existing
        entity. See DEF_CREATE_NEW_ENTITY_MSG_FMT on how the name
        (and the lower() version of it) is used.
      missing_redirect: The missing_redirect value is also used to
        construct the message_fmt mentioned above.
      error_public: The error_public value is used as the template for
        the error response mentioned above.

    Args:
      request: the standard Django HTTP request object
      access_type : the name of the access type which should be checked
      page_name: the page name displayed in templates as page and header title
      params: a dict with params for this View
      kwargs: The Key Fields for the specified entity
    """

    logic = params['logic']

    context = helper.responses.getUniversalContext(request)
    helper.responses.useJavaScript(context, params['js_uses_all'])
    context['page_name'] = page_name

    try:
      entity = logic.getFromKeyFieldsOr404(kwargs)
    except out_of_band.Error, error:
      msg = self.DEF_CREATE_NEW_ENTITY_MSG_FMT % {
          'entity_type_lower' : params['name'].lower(),
          'entity_type' : params['name'],
          'create' : params['missing_redirect']
          }
      error.message_fmt = error.message_fmt + msg
      return helper.responses.errorResponse(
          error, request, context=context)

    self._edit(request, entity, context, params)

    if request.method == 'POST':
      return self.editPost(request, entity, context, params=params)
    else:
      return self.editGet(request, entity, context, params=params)

  @decorators.merge_params
  @decorators.mutation
  def editPost(self, request, entity, context, params=None):
    """Processes POST requests for the specified entity.

    Params usage:
      The params dictionary is passed to _constructResponse when the
      form is not valid (see edit_form and create_form below). See
      the docstring of _constructResponse on how it uses it.

      edit_form: The edit_form value is used as form when there is an
        existing entity. It is provided with with the request.POST
        dictionary on construction. The collectCleanedFields method
        is called with the newly constructed form. If the form is
        not valid, it is passed as argument to _constructResponse.
      create_form: The create_form value is used in a similar way to
        edit_form, only it is used when there is no existing entity.
      edit_redirect: The edit_redirect value is used as the first part
        of the url if the form was valid. The last part of the url is
        created using the .key().id_or_name() method of the entity.
      edit_params: The edit_params dictionary is used as argument to
        redirectToChangedSuffix, it will be appended to the url in the
        standard ?key=value format.

    Args:
      request: a django request object
      entity: the entity that will be modified or created, may be None
      context: the context dictionary that will be provided to Django
      params: required, a dict with params for this View
    """

    logic = params['logic']

    form = params['edit_form'](request.POST)

    if not form.is_valid():
      return self._constructResponse(request, entity, context, form, params)

    _, fields = forms.collectCleanedFields(form)

    self._editPost(request, entity, fields)

    entity = logic.updateEntityProperties(entity, fields)

    page_params = params['edit_params']
    params['suffix'] = entity.key().id_or_name()

    request.path = params['edit_redirect'] % params

    return helper.responses.redirectToChangedSuffix(
        request, None, params=page_params)

  @decorators.merge_params
  def editGet(self, request, entity, context, params=None):
    """Processes GET requests for the specified entity.

    Params usage:
      The params dictionary is passed to _constructResponse, see the
      docstring  of _constructResponse on how it uses it.

      save_message: The save_message list is used as argument to
        getSingleIndexedParamValue when an existing entity was saved.
      edit_form: The edit_form is used as form if there is an existing
        entity. The existing entity is passed as instance to it on
        construction. If key_name is part of it's fields it will be
        set to the entity's key().id_or_name() value. It is also passed as
        argument to the _editGet method. See the docstring for
        _editGet on how it uses it.
      create_form: The create_form is used as form if there was no
        existing entity. If the seed argument is present, it is passed
        as the 'initial' argument on construction. Otherwise, it is
        called with no arguments.
      submit_msg_param_name: The submit_msg_param_name value is used
        as the key part in the ?key=value construct for the submit
        message parameter (see also save_message).

    Args:
      request: the django request object
      entity: the entity that will be edited, may be None
      context: the context dictionary that will be provided to django
      seed: if no entity is provided, the initial values for the new entity
      params: required, a dict with params for this View
    """

    # logic = params['logic']
    suffix = str(entity.key().id_or_name()) if entity else None

    # remove the params from the request, this is relevant only if
    # someone bookmarked a POST page.
    is_self_referrer = requests.isReferrerSelf(
        request, suffix=suffix, url_name=params['url_name'])

    if request.GET.get(params['submit_msg_param_name']):
      if (not entity) or (not is_self_referrer):
        return http.HttpResponseRedirect(request.path)

    # note: no message will be displayed if parameter is not present
    context['notice'] = requests.getSingleIndexedParamValue(
        request, params['submit_msg_param_name'],
        values=params['save_message'])

    # populate form with the existing entity
    form = params['edit_form'](instance=entity)

    self._editGet(request, entity, form)

    return self._constructResponse(request, entity, context, form, params)

  @decorators.merge_params
  @decorators.check_access
  def list(self, request, access_type, page_name=None,
           params=None, filter=None, order=None,
           visibility=None, context=None, **kwargs):
    """Displays the list page for the entity type.

    Args:
      request: the standard Django HTTP request object
      access_type : the name of the access type which should be checked
      page_name: the page name displayed in templates as page and header title
      params: a dict with params for this View
      filter: a dict for the properties that the entities should have

    Params usage:
      The params dictionary is passed as argument to getListContent in
      the soc.views.helper.list module. See the docstring for getListContent
      on how it uses it. The params dictionary is also passed as argument to
      the _list method. See the docstring for _list on how it uses it.
    """

    get_args = request.GET
    fmt = get_args.get('fmt')
    idx = get_args.get('idx', '')

    if fmt == 'json':
      if not (idx.isdigit() and int(idx) == 0):
        return responses.jsonErrorResponse(request, "idx not valid")

      contents = helper.lists.getListData(request, params, filter,
                                          visibility, order=order)
      json = simplejson.dumps(contents)

      return responses.jsonResponse(request, json)

    content = helper.lists.getListGenerator(request, params, idx=0)
    contents = [content]

    return self._list(request, params, contents, page_name, context=context)

  def _list(self, request, params, contents, page_name, context=None):
    """Returns the list page for the specified contents.

    Args:
      request: the standard Django HTTP request object
      params: a dict with params for this View
      contents: a list of content dicts
      page_name: the page name displayed in templates as page and header title
      context: the context for this page

    Params usage:
      list_template: The list_template value is used as template for
        to display the list of all entities for this View.
    """

    context = dicts.merge(context,
        helper.responses.getUniversalContext(request))
    helper.responses.useJavaScript(context, params['js_uses_all'])
    context['page_name'] = page_name
    context['list'] = soc.logic.lists.Lists(contents)

    context['list_msg'] = params.get('list_msg', None)
    context['no_lists_msg'] = params.get('no_lists_msg', None)

    template = params['list_template']

    return helper.responses.respond(request, template, context)

  @decorators.merge_params
  @decorators.check_access
  @decorators.mutation
  def delete(self, request, access_type,
             page_name=None, params=None, **kwargs):
    """Shows the delete page for the entity specified by **kwargs.

    Args:
      request: the standard Django HTTP request object
      access_type : the name of the access type which should be checked
      page_name: the page name displayed in templates as page and header title
      params: a dict with params for this View
      kwargs: The Key Fields for the specified entity

    Params usage:
      rights: The rights dictionary is used to check if the user has
        the required rights to delete the specified entity. See checkAccess
        for more details on how the rights dictionary is used to check access
        rights.
      name: used in the same way as in edit(), see it's docstring for
        a more detailed explanation on how it is used.
      missing_redirect: see name
      error_edit: see name
      delete_redirect: The delete_redirect value is used as the url to
        redirect to after having successfully deleted the entity.
    """

    logic = params['logic']

    try:
      entity = logic.getFromKeyFieldsOr404(kwargs)
    except out_of_band.Error, error:
      error.message_fmt = (
        error.message_fmt + self.DEF_CREATE_NEW_ENTITY_MSG_FMT % {
          'entity_type_lower' : params['name'].lower(),
          'entity_type' : params['name'],
          'create' : params['missing_redirect']})
      return helper.responses.errorResponse(
          error, request, template=params['error_edit'])

    if not logic.isDeletable(entity):
      page_params = params['cannot_delete_params']
      params['suffix'] = entity.key().id_or_name()
      request.path = params['edit_redirect'] % params

      # redirect to the edit page
      # display notice that entity could not be deleted
      return helper.responses.redirectToChangedSuffix(
          request, None, params=page_params)

    logic.delete(entity)
    redirect = params['delete_redirect']

    return http.HttpResponseRedirect(redirect)

  def select(self, request, view, redirect,
             page_name=None, params=None, filter=None):
    """Displays a list page allowing the user to select an entity.

    After having selected the Scope, the user is redirected to the
    'create a new entity' page with the scope_path set appropriately.

    Params usage:
      The params dictionary is also passed to getListContent from
        the helper.list module, please refer to its docstring also.
      The params dictionary is passed to self._list as well, refer
        to its docstring for details on how it uses it.

    Args:
      request: the standard Django HTTP request object
      view: the view for which to generate the select page
      redirect: the redirect to use
      page_name: the page name displayed in templates as page and header title
      params: a dict with params for this View
      filter: a filter that all displayed entities should satisfy
    """
    view_params = view.getParams().copy()
    view_params['list_description'] = self.DEF_CREATE_INSTRUCTION_MSG_FMT % (
        view_params['name'], self._params['name'])
    view_params['public_row_extra'] = lambda entity, *args: {
        'link': redirect(entity, view_params, *args)
    }

    return view.list(request, 'any_access', page_name=page_name,
                     params=view_params, filter=filter)

  def _getData(self, model, filter, order, logic):
    """Retrieves the pick data for this query.

    Args:
      model: the model that is being queried
      filter: the filters that apply
      logic: the logic that will be used for the query
    """

    entities = logic.getForFields(filter=filter, order=order, limit=1000)
    return entities

  @decorators.merge_params
  @decorators.check_access
  def pick(self, request, acces_type, page_name=None, params=None):
    """Displays a list page allowing the user to select an entity.

    After having selected an entity, the user is redirected to the
    return_url as specified in the GET args.

    Params usage:
      The params dictionary is passed to self.select, refer
        to its docstring for details on how it uses it.

    Args:
      request: the standard Django HTTP request object
      access_type : the name of the access type which should be checked
      page_name: the page name displayed in templates as page and header title
      params: a dict with params for this View
    """

    logic = params['logic']

    # convert to a regular dict
    filter = {}
    for key in request.GET.keys():
      # need to use getlist as we want to support multiple values
      filter[key] = request.GET.getlist(key)

    if params['cache_pick']:
      fun =  soc.cache.logic.cache(self._getData)
    else:
      fun = self._getData

    order = []
    entities = fun(logic.getModel(), filter, order, logic)

    key_order = params.get('cache_pick_order')
    data = [i.toDict(key_order) for i in entities]

    return self.json(request, data)

  def json(self, request, data, to_json=True):
    """Returns data as a json object.

    Args:
      request: the standard Django HTTP request object
      data: the data to be sent as a json object
      to_json: determines if the data should be converted to a json object
    """

    if to_json:
      json = simplejson.dumps({'data': data})
    else:
      json = data

    return responses.jsonResponse(request, json)

  def csv(self, request, data, filename, params, key_order=None):
    """Returns data as a csv file.

    If key_order is set data should be a sequence of dicts, otherwise
    data should be a sequence of lists, see csv.writer and
    csv.DictWriter for more information.
    """

    params = params.copy()
    params['export_extension'] = '.csv'
    params['export_content_type'] = 'text/csv'
    # fieldnames = params['csv_fieldnames']

    file_handler = StringIO.StringIO()

    if key_order:
      writer = csv.DictWriter(file_handler, key_order, dialect='excel')
      writer.writerow(dicts.identity(key_order))

      # encode the data to UTF-8 to ensure compatibiliy
      for row_dict in data:
        for key in row_dict.keys():
          value = row_dict[key]
          if isinstance(value, basestring):
            row_dict[key] = value.encode("utf-8")
          else:
            row_dict[key] = str(value)
        writer.writerow(row_dict)
    else:
      writer = csv.writer(file_handler, dialect='excel')

      # encode the data to UTF-8 to ensure compatibiliy
      for row in data:
        if row:
          writer.writerow(row.encode("utf-8"))
        else:
          writer.writerow(row)

    data = file_handler.getvalue()

    return self.download(request, data, filename, params)

  def _editPost(self, request, entity, fields):
    """Performs any required processing on the entity to post its edit page.

    Args:
      request: the django request object
      entity: the entity to create or update from POST contents
      fields: the new field values
    """

    references = self._params['references']
    for field_name, original_name, _ in references:
      if field_name not in fields:
        continue

      entity = fields.get('resolved_%s' % field_name)
      fields[original_name] = entity

    # If scope_logic is not defined, this entity has no scope
    if not self._params['scope_logic']:
      return

    # If this entity is unscoped, do not try to retrieve a scope
    if 'scope_path' not in fields:
      return

    if not entity:
      scope = self._params['scope_logic'].logic.getFromKeyName(
          fields['scope_path'])
      fields['scope'] = scope

  def _public(self, request, entity, context):
    """Performs any required processing to get an entity's public page.

    Should return True iff the public page should be displayed.

    Args:
      request: the django request object
      entity: the entity to make public
      context: the context object
    """

    return True

  def _edit(self, request, entity, context, params):
    """Hook for the edit View.

    Args:
      request: the Django request object
      entity: entity being edited
      context: context for the View
      params: params for the View
    """
    pass

  def _editGet(self, request, entity, form):
    """Performs any required processing on the form to get its edit page.

    Args:
      request: the django request object
      entity: the entity to get
      form: the django form that will be used for the page
    """

    # fill in the email field with the data from the entity
    if 'scope_path' in form.fields:
      form.fields['scope_path'].initial = entity.scope_path

    for field_name, _, getter in self._params['references']:
      try:
        field = getter(entity)
        form.fields[field_name].initial = field.link_id if field else None
      except db.Error:
        # TODO(Pawel.Solyga): use logging to log exception
        return

    for field, value in request.GET.iteritems():
      if field in form.fields:
        form.fields[field].initial = value

  def _editSeed(self, request, seed):
    """Performs any required processing on the form to get its edit page.

    Args:
      request: the django request object
      seed: the fields to seed the create page with
    """
    pass

  def _editContext(self, request, context):
    """Performs any required processing on the context for edit pages.

    Args:
      request: the django request object
      context: the context dictionary that will be used
    """

    pass

  def _constructResponse(self, request, entity, context,
                         form, params, template=None):
    """Updates the context and returns a response for the specified arguments.

    Args:
      request: the django request object
      entity: the entity that is used and set in the context
      context: the context to be used
      form: the form that will be used and set in the context
      params: a dict with params for this View
      template: if specified, this template is

    Params usage:
      name: The name value is used to set the entity_type
       value in the context so that the template can refer to it.
      name_plural: same as name, but used to set entity_type_plural
      name_short: same as name, but used to set entity_type_short
      url_name: same as name, but used to set entity_type_url
      edit_template: The edit_template value is used as template when
        there is an existing entity to display the edit page for the
        specified entity.
      create_template: similar to edit_template, but is used when
        there is no existing entity.
    """

    logic = params['logic']
    suffix = entity.key().id_or_name() if entity else None

    context['form'] = form
    context['entity'] = entity
    context['entity_suffix'] = suffix
    context['entity_type'] = params['name']
    context['entity_type_plural'] = params['name_plural']
    context['entity_type_short'] = params['name_short']
    context['entity_type_url'] = params['url_name']
    context['cancel_redirect'] = params.get('cancel_redirect')
    context['return_url'] = request.path
    if entity:  # when creating, the entity does not exist.
      context['is_deletable'] = logic.isDeletable(entity)

    if params.get('export_content_type') and entity:
      context['export_link'] = redirects.getExportRedirect(entity, params)

    if not template:
      if entity:
        template = params['edit_template']
      else:
        template = params['create_template']

    self._editContext(request, context)

    # remove the seed from the context before dispatching to Django
    context.pop('seed', None)

    return helper.responses.respond(request, template, context)

  def getParams(self):
    """Returns this view's params attribute.
    """

    return self._params

  @decorators.merge_params
  def getSidebarMenus(self, id, user, params=None):
    """Returns an dictionary with one sidebar entry.

    Args:
      params: a dict with params for this View

    Params usage:
      The params dictionary is passed as argument to getSidebarItems
      from the soc.views.sitemap.sidebar module, see the docstring
      of _getSidebarItems on how it uses it.
    """

    return sidebar.getSidebarMenus(id, user, params=params)

  @decorators.merge_params
  def getDjangoURLPatterns(self, params=None):
    """Retrieves a list of sidebar entries for this view

    Params usage:
      The params dictionary is passed to the getDjangoURLPatterns
      function in the soc.views.sitemap.sitemap module, see the
      docstring of getDjangoURLPatterns on how it uses it.

    Args:
      params: a dict with params for this View
    """

    return sitemap.getDjangoURLPatterns(params)

