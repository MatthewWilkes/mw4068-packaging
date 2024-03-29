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

"""Views for Jobs.
"""

__authors__ = [
    '"Sverre Rabbelier" <sverre@rabbelier.nl>',
  ]


from django import forms

from soc.logic import dicts
from soc.logic.models.job import logic as job_logic
from soc.views.helper import access
from soc.views.helper import decorators
from soc.views.helper import widgets
from soc.views.models import base


class View(base.View):
  """View methods for the Job model.
  """

  def __init__(self, params=None):
    """Defines the fields and methods required for the base View class
    to provide the user with list, public, create, edit and delete views.

    Params:
      params: a dict with params for this View
    """

    rights = access.Checker(params)

    new_params = {}
    new_params['rights'] = rights
    new_params['logic'] = job_logic

    new_params['name'] = "Job"

    new_params['no_create_raw'] = True
    new_params['no_create_with_scope'] = True
    new_params['no_create_with_key_fields'] = True

    new_params['extra_dynaexclude'] = ['key_data', 'text_data']

    new_params['edit_dynaproperties'] = {
      'task': forms.CharField(widget=widgets.PlainTextWidget()),
      }

    new_params['public_field_prefetch'] = ['priority_group']
    new_params['public_field_extra'] = lambda entity: {
        "id": entity.key().id_or_name(),
        "priority_group": entity.priority_group.name,
    }
    new_params['public_field_keys'] = ["id", "task_name", "priority_group"]
    new_params['public_field_names'] = ["ID", "Name", "Priority Group"]

    params = dicts.merge(params, new_params)

    super(View, self).__init__(params=params)


view = View()

delete = decorators.view(view.delete)
edit = decorators.view(view.edit)
list = decorators.view(view.list)
public = decorators.view(view.public)
