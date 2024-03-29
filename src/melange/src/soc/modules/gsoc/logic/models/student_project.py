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

"""Student Project (Model) query functions.
"""

__authors__ = [
  '"Lennard de Rijk" <ljvderijk@gmail.com>',
  ]


from google.appengine.ext import db

from soc.logic.models import base

from soc.modules.gsoc.logic.models import organization as org_logic

import soc.models.linkable

import soc.modules.gsoc.models.student_project


class Logic(base.Logic):
  """Logic methods for the Student Project model.
  """

  def __init__(self,
               model=soc.modules.gsoc.models.student_project.StudentProject,
               base_model=soc.models.linkable.Linkable, 
               scope_logic=org_logic):
    """Defines the name, key_name and model for this entity.
    """

    super(Logic, self).__init__(model=model, base_model=base_model,
                                scope_logic=scope_logic)

  def canChangeMentors(self, entity):
    """Returns true iff the Project's mentors may be changed.
    """
    project_status = entity.status
    org_status = entity.scope.status

    return project_status == 'accepted' and org_status == 'active'

  def updateProjectsForGradingRecords(self, record_entities):
    """Updates StudentProjects using a list of GradingRecord entities.

    Args:
      record_entities: List of GradingRecord entities to process.
    """

    projects_to_update = []

    for record_entity in record_entities:

      project_entity = record_entity.project

      if project_entity.status in ['withdrawn', 'invalid']:
        # skip this project
        continue

      # get the key from the GradingRecord entity since that gets stored
      record_key = record_entity.key()

      passed_evals = project_entity.passed_evaluations
      failed_evals = project_entity.failed_evaluations

      # try to remove this GradingRecord from the existing list of evals
      if record_key in passed_evals:
        passed_evals.remove(record_key)

      if record_key in failed_evals:
        failed_evals.remove(record_key)

      # get the grade_decision from the GradingRecord
      grade_decision = record_entity.grade_decision

      # update GradingRecord lists with respect to the grading_decision
      if grade_decision == 'pass':
        passed_evals.append(record_key)
      elif grade_decision == 'fail':
        failed_evals.append(record_key)

      if project_entity.status != 'completed':
        # Only when the project has not been completed should the status be
        # updated to reflect the new setting of the evaluations.

        if len(failed_evals) == 0:
          # no failed evaluations present
          new_status = 'accepted'
        else:
          new_status = 'failed'
      else:
          new_status = project_entity.status

      # update the necessary fields and store it before updating
      project_entity.passed_evaluations = passed_evals
      project_entity.failed_evaluations = failed_evals
      project_entity.status = new_status

      projects_to_update.append(project_entity)

    # batch put the StudentProjects that need to be updated
    db.put(projects_to_update)


logic = Logic()
