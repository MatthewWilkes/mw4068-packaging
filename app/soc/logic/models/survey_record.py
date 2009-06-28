#!/usr/bin/python2.5
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

"""SurveyRecord (Model) query functions.
"""

__authors__ = [
  '"Lennard de Rijk" <ljvderijk@gmail.com>',
  ]


from google.appengine.ext import db

from soc.logic.models import work
from soc.models.survey_record import SurveyRecord
from soc.models.survey_record import ProjectSurveyRecord
from soc.models.survey_record import GradingProjectSurveyRecord


class Logic(work.Logic):
  """Logic methods for listing results for Surveys.
  """

  def __init__(self, model=SurveyRecord,
               base_model=None, scope_logic=None):
    """Defines the name, key_name and model for this entity.
    """

    super(Logic, self).__init__(model=model, base_model=base_model,
                                scope_logic=scope_logic)

  def updateSurveyRecord(self, user, survey, survey_record, fields):
    """ Create a new survey record, or get an existing one.

    params:
      user = user taking survey
      survey = survey entity
      survey_record = existing record, if one exists
      fields = submitted responses to survey fields
    """

    if survey_record:
      create = False
      for prop in survey_record.dynamic_properties():
        delattr(survey_record, prop)
    else:
      create = True
      Record = self.getModel()
      survey_record = Record(user=user, survey=survey)

    schema = eval(survey.survey_content.schema)

    for name, value in fields.items():
      # TODO(ajaksu) logic below can be improved now we have different models
      if name == 'project':
        project = student_project.StudentProject.get(value)
        survey_record.project = project
      elif name == 'grade':
        survey_record.grade = GRADES[value]
      else:
        pick_multi = name in schema and schema[name]['type'] == 'pick_multi'
        if pick_multi and hasattr(fields, 'getlist'): # it's a multidict
          setattr(survey_record, name, ','.join(fields.getlist(name)))
        else:
          setattr(survey_record, name, value)

    # if creating evaluation record, set SurveyRecordGroup
    db.put(survey_record)
    return survey_record


logic = Logic()
# TODO separate project and grading logic into own class to overwrite methods
project_logic = Logic(model=ProjectSurveyRecord)
grading_logic = Logic(model=GradingProjectSurveyRecord)


def updateSurveyRecord(user, survey, survey_record, fields):
  """Create a new survey record, or get an existing one.

  params:
    user = user taking survey
    survey = survey entity
    survey_record = existing record, if one exists
    fields = submitted responses to survey fields
  """

  # TODO(ajaksu) We should use class information here, but being careful about
  # compatibility with existent records should the class change.
  if hasattr(survey_record, 'grade'):
    record_logic = grading_logic
  elif hasattr(survey_record, 'project'):
    record_logic = grading_logic
  else:
    record_logic = logic

  return record_logic.updateSurveyRecord(user, survey, survey_record, fields)
