from odoo import api, fields, models, _
from datetime import datetime, time, timedelta
from odoo.http import request, Response



class ApprovalStateWizard(models.TransientModel):
	_name = 'approval.state.wizard'
	_description ="Approve state Wizard"


	name = fields.Text("Comment", required=True)








	def action_generate(self):
		docs = self.env['hr.resignation'].browse(self.env.context.get('active_id'))
		if docs.state == 'manager':
			state = 'asset_management'
			email = docs.sudo().get_management_mail()
			email_cc = docs.sudo().get_management_mail_cc()
			template = self.env.ref('x_hr_resignation.template_mail_approve_resignation')
			template.email_to = email
			template.email_cc = email_cc
			template.send_mail(self._context.get('active_id'), force_send=True)

		if docs.state == 'asset_management':
			state = 'hc'
			email = docs.sudo().get_mail_hc()
			email_cc = docs.sudo().get_mail_hc_cc()
			template = self.env.ref('x_hr_resignation.template_mail_approve_resignation_hc')
			template.email_to = email
			template.email_cc = email_cc
			template.send_mail(self._context.get('active_id'), force_send=True)

		if docs.state == 'hc':
			state = 'done'
			docs.sudo().employee_id.active = False
			docs.sudo().employee_id.user_id.active = False
			mail_hc = self.env.ref('x_hr_resignation.template_mail_approve_resignation_done')
			mail_hc.email_to = docs.employee_id.work_email
			mail_hc.sudo().send_mail(self._context.get('active_id'), force_send=True)

		if docs.state == 'hc':
			email = docs.get_mail_hc()
			template = self.env.ref('x_hr_resignation.template_mail_approve_resignation_done')
			template.email_to = email
			template.send_mail(self._context.get('active_id'), force_send=True)

		user = self.env.user
		wkj = [(0,0,{
			'state' : "Approved",
			'comment' : self.name,
			'user_id' : user.id
			})]

		docs.approval_history_ids = wkj
		docs.state = state
			
		


class ApprovalStateRejectWizard(models.TransientModel):
	_name = 'approval.state.reject.wizard'
	_description ="Approve reject state Wizard"


	name = fields.Text("Comment", required=True)



	def action_reject_generate(self):
		docs = self.env['hr.resignation'].browse(self.env.context.get('active_id'))
		user = self.env.user
		wkj = [(0,0,{
			'state' : "Reject",
			'comment' : self.name,
			'user_id' : user.id
			})]

		docs.approval_history_ids = wkj
		docs.state = 'new'
