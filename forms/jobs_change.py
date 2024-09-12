from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField


class JobsFormChange(FlaskForm):
    id = IntegerField('Job_id')
    job_title = StringField('Job Title')
    team_leader_id = StringField('Team Leader Id')
    work_size = StringField('Work Size')
    collaborators = StringField('Collaborators')
    is_job_finished = BooleanField('Is Job Finished')
    submit = SubmitField('Submit')
