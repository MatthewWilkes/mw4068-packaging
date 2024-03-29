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

"""Mentor (Model) query functions.
"""

__authors__ = [
  '"Lennard de Rijk" <ljvderijk@gmail.com>',
  ]


from google.appengine.ext import db

from soc.logic.models import role
from soc.logic.models import organization as org_logic

import soc.models.mentor
import soc.models.role


DEF_ALREADY_MENTORING_RPOJECT_MSG = "This Mentor is mentoring a Student "\
    "Project and can therefore not be resigned. Please assign another Mentor."

DEF_ALREADY_MENTORING_PROPOSAL_MSG = "This Mentor is mentoring a Student "\
    "Proposal and can therefore not be resigned. Please assign another Mentor."


class Logic(role.Logic):
  """Logic methods for the Mentor model.
  """

  def __init__(self, model=soc.models.mentor.Mentor,
               base_model=soc.models.role.Role, scope_logic=org_logic,
               role_name='mentor', disallow_last_resign=False):
    """Defines the name, key_name and model for this entity.
    """

    super(Logic, self).__init__(model=model, base_model=base_model,
                                scope_logic=scope_logic,
                                role_name=role_name,
                                disallow_last_resign=disallow_last_resign)

  def canResign(self, entity):
    """Checks if the Mentor is able to resign.

    Checks if there are no Student Proposals or Student Projects that
    have this mentor assigned to it.

    Args:
      entity: a Mentor entity

    """

    from soc.modules.gsoc.logic.models.student_project import logic as \
        student_project_logic
    from soc.modules.gsoc.logic.models.student_proposal import logic as \
        student_proposal_logic

    fields = {'mentor': entity}

    student_project_entity = student_project_logic.getForFields(fields,
                                                                unique=True)
    if student_project_entity:
      return DEF_ALREADY_MENTORING_RPOJECT_MSG

    student_proposal_entity = student_proposal_logic.getForFields(fields,
                                                                  unique=True)

    if student_proposal_entity:
      return DEF_ALREADY_MENTORING_PROPOSAL_MSG

    return super(Logic, self).canResign(entity)

  def _updateField(self, entity, entity_properties, name):
    """Called when the fields of the mentor are updated

      When status is changed to invalid, removes the Mentor from all Student
      Proposals possible mentor lists.
    """

    from soc.modules.gsoc.logic.models.student_proposal import logic \
        as student_proposal_logic

    value = entity_properties[name]

    if name == 'status' and value != entity.status and value == 'invalid':
      fields = {'org': entity.scope}

      # TODO make this work for more then 1000 entities
      proposals_query = student_proposal_logic.getQueryForFields(fields)

      # store all updated proposals
      changed = []

      for proposal in proposals_query:

        if proposal.possible_mentors.count(entity.key()):
          # remove from list and add to changed
          proposal.possible_mentors.remove(entity.key())
          changed.append(proposal)

      # store all changed proposals
      db.put(changed)

    return super(Logic, self)._updateField(entity, entity_properties, name)


logic = Logic()
