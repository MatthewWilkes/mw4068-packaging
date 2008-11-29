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

"""Views for the User's own profiles.
"""

__authors__ = [
    '"Sverre Rabbelier" <sverre@rabbelier.nl>',
    '"Pawel Solyga" <pawel.solyga@gmail.com>',
  ]


from google.appengine.api import users

from django import forms
from django.utils.translation import ugettext_lazy

from soc.logic import dicts
from soc.logic import validate
from soc.logic.models import user as user_logic
from soc.views import helper
from soc.views import out_of_band
from soc.views.helper import access
from soc.views.models import base

import soc.models.linkable
import soc.models.user
import soc.logic.models.user
import soc.views.helper


class UserForm(helper.forms.BaseForm):
  """Django form displayed when creating or editing a User.
  """
  class Meta:
    """Inner Meta class that defines some behavior for the form.
    """
    #: db.Model subclass for which the form will gather information
    model = soc.models.user.User

    #: list of model fields which will *not* be gathered by the form
    exclude = ['account', 'former_accounts', 'is_developer']

  def clean_link_id(self):
    link_id = self.cleaned_data.get('link_id')
    if not validate.isLinkIdFormatValid(link_id):
      raise forms.ValidationError("This link ID is in wrong format.")

    user = soc.logic.models.user.logic.getForFields({'link_id': link_id},
                                          unique=True)

    # Get the currently logged in user account
    current_account = users.get_current_user()

    if user:
      if current_account != user.account:
        raise forms.ValidationError("This link ID is already in use.")

    return link_id


class View(base.View):
  """View methods for the User model.
  """

  DEF_USER_ACCOUNT_INVALID_MSG_FMT = ugettext_lazy(
    'The <b><i>%(email)s</i></b> account cannot be used with this site, for'
    ' one or more of the following reasons:'
    '<ul>'
    ' <li>the account is invalid</li>'
    ' <li>the account is already attached to a User profile and cannot be'
    ' used to create another one</li>'
    ' <li>the account is a former account that cannot be used again</li>'
    '</ul>')

  def __init__(self, original_params=None):
    """Defines the fields and methods required for the base View class
    to provide the user with list, public, create, edit and delete views.

    Params:
      original_params: a dict with params for this View
    """

    rights = {}
    rights['unspecified'] = [access.deny]
    rights['any_access'] = [access.allow]
    rights['editSelf'] = [access.checkIsLoggedIn]
    rights['roles'] = [access.checkIsUser]
    rights['signIn'] = [access.checkNotLoggedIn]

    params = {}
    params['rights'] = rights
    params['logic'] = soc.logic.models.user.logic

    params['name'] = "User"
    params['name_short'] = "User"
    params['name_plural'] = "Users"
    params['url_name'] = "user"
    params['module_name'] = "user_self"
    
    params['sidebar_heading'] = 'Users'

    params = dicts.merge(original_params, params)

    base.View.__init__(self, params=params)

  EDIT_SELF_TMPL = 'soc/user/edit_self.html'

  def edit(self, request, page_name=None, params=None, **kwargs):
    """Displays User self edit page for the entity specified by **kwargs.

    Args:
      request: the standard Django HTTP request object
      page_name: the page name displayed in templates as page and header title
      params: a dict with params for this View
      kwargs: The Key Fields for the specified entity
    """

    try:
      self.checkAccess('editSelf', request)
    except out_of_band.Error, error:
      return error.response(request, template=self.EDIT_SELF_TMPL)

    new_params = {}
    new_params['edit_template'] = self.EDIT_SELF_TMPL

    params = dicts.merge(params, new_params)
    params = dicts.merge(params, self._params)

    account = users.get_current_user()
    properties = {'account': account}

    user = soc.logic.models.user.logic.getForFields(properties, unique=True)

    # create default template context for use with any templates
    context = helper.responses.getUniversalContext(request)

    if request.method == 'POST':
      form = UserForm(request.POST)

      if form.is_valid():
        new_link_id = form.cleaned_data.get('link_id')
        properties = {
          'link_id': new_link_id,
          'name': form.cleaned_data.get("name"),
          'account': account,
        }

        # check if user account is not in former_accounts
        # if it is show error message that account is invalid
        if soc.logic.models.user.logic.isFormerAccount(account):
          msg = self.DEF_USER_ACCOUNT_INVALID_MSG_FMT % {
            'email': account.email()}
          error = out_of_band.Error(msg)
          return error.response(request, template=self.EDIT_SELF_TMPL,
                                context=context)

        user = soc.logic.models.user.logic.updateOrCreateFromFields(
            properties, {'link_id': new_link_id})

        # redirect to /user/profile?s=0
        # (causes 'Profile saved' message to be displayed)
        return helper.responses.redirectToChangedSuffix(
            request, None, params=params['edit_params'])
    else: # request.method == 'GET'
      if user:
        # is 'Profile saved' parameter present, but referrer was not ourself?
        # (e.g. someone bookmarked the GET that followed the POST submit)
        if (request.GET.get(self.DEF_SUBMIT_MSG_PARAM_NAME)
            and (not helper.requests.isReferrerSelf(request))):
          # redirect to aggressively remove 'Profile saved' query parameter
          return http.HttpResponseRedirect(request.path)

        # referrer was us, so select which submit message to display
        # (may display no message if ?s=0 parameter is not present)
        context['notice'] = (
            helper.requests.getSingleIndexedParamValue(
                request, self.DEF_SUBMIT_MSG_PARAM_NAME,
                values=params['save_message']))

        # populate form with the existing User entity
        form = UserForm(instance=user)
      else:
        if request.GET.get(self.DEF_SUBMIT_MSG_PARAM_NAME):
          # redirect to aggressively remove 'Profile saved' query parameter
          return http.HttpResponseRedirect(request.path)

        # no User entity exists for this Google Account, so show a blank form
        form = UserForm()

    context['form'] = form

    template = params['edit_template']

    return helper.responses.respond(request, template, context)
  
  def _editGet(self, request, entity, form):
    """See base.View._editGet().
    """
    # fill in the email field with the data from the entity
    form.fields['email'].initial = entity.account.email()

  def _editPost(self, request, entity, fields):
    """See base.View._editPost().
    """
    # fill in the account field with the user created from email
    fields['account'] = users.User(fields['email'])

  def getSidebarLinks(self, request):
    """Returns an dictionary with the user sidebar entry.
    """

    params = {}
    params['sidebar_heading'] = "User (self)"
    params['sidebar'] = [
        (users.create_login_url(request.path), 'Sign In', 'signIn'),
        ('/' + self._params['url_name'] + '/edit', 'Profile', 'editSelf'),
        ('/' + self._params['url_name'] + '/roles', 'Roles', 'roles'),
        ]

    return super(View, self).getSidebarLinks(request, params)

  def getDjangoURLPatterns(self):
    """See base.View.getDjangoURLPatterns().
    """

    patterns = []
    patterns += [(r'^' + self._params['url_name'] + '/edit$',
                   'soc.views.models.user_self.edit')]

    page_name = "Requests Overview"
    patterns += [(r'^' + self._params['url_name'] + '/roles$',
                   'soc.views.models.request.list_self',
                   {'page_name': page_name}, page_name)]

    return patterns


view = View()

edit = view.edit
