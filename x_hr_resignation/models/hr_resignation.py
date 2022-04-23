# -*- coding: utf-8 -*-
import datetime
from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, Response
from dateutil.relativedelta import relativedelta


RESIGNATION_TYPE =[('new', 'New'), 
                  ('manager', 'Manager'), 
                  ('asset_management', 'Asset Management'), 
                  ('hc', 'Human Capital'), 
                  ('done', 'Done')]


RESIGNATION_TYPE_LINE =[('asset_management', 'Asset Management'), 
                        ('hc', 'Human Capital')]



class HRemploye(models.Model):
    _inherit = 'hr.employee'


    employee_id_number = fields.Char("Employee ID Number")
    checked_id = fields.Many2one("checked.received", string="Checked")
    # marital_status_id = fields.Many2one("marital.status","Marital Status")







class HrResignation(models.Model):
    _name = 'hr.resignation'
    _inherit = 'mail.thread'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string="Employee", help='Name of the employee for whom the request is creating')
    employee_id_number = fields.Char('Employee ID')
    job_id = fields.Many2one('hr.job','Position Title', copy=False)
    department_id = fields.Many2one('hr.department', string="Department",
                                    help='Department of the employee')
    manager_id = fields.Many2one('hr.employee','Manager')
    hire_date = fields.Date('Hire Date')
    resignation_current_date = fields.Date('Resignation Letter Date')
    termination_date = fields.Date('Termination Date')
    resignation_reason = fields.Many2one('resignation.reason','Resignation Reason')
    

    state = fields.Selection(selection=RESIGNATION_TYPE, string='Status', default='new', track_visibility="always")
    attachment_number = fields.Integer('Number of Attachments', compute='_compute_attachment_number')

    company_facility_equipment_ids = fields.One2many('company.facility.equipment.line','resignation_id','Company Facility Equipment')
    it_security_access_ids = fields.One2many('it.security.access.line','resignation_id','IT Security Access')
    settlement_balance_of_loan_ids = fields.One2many('settlement.balance.of.loan.line','resignation_id','Settlement Balance Of Loan')
    hc_operations_ids = fields.One2many('hc.operations.line','resignation_id','HC Operations')
    transfer_job_ids = fields.One2many('transfer.job.line','resignation_id','Transfer Job')
    approval_history_ids = fields.One2many('approval.history','resignation_id','Approval History')
    


    @api.onchange('employee_id')
    def get_company_facility_equipment(self):
        cfe = self.env['company.facility.equipment'].search([('active_line','=',True)])
        competency = []
        for x in cfe:
            competency.append((0,0, {
                        "item_id": x.id,
                        }))
        if not self.company_facility_equipment_ids:
            self.company_facility_equipment_ids = competency


    @api.onchange('employee_id')
    def get_it_security_access(self):
        cfe = self.env['it.security.access'].search([('active_line','=',True)])
        competency = []
        for x in cfe:
            competency.append((0,0, {
                        "item_id": x.id,
                        }))

        if not self.it_security_access_ids:
            self.it_security_access_ids = competency


    @api.onchange('employee_id')
    def get_settlement_balance_of_loan(self):
        cfe = self.env['settlement.balance.of.loan'].search([('active_line','=',True)])
        competency = []
        for x in cfe:
            competency.append((0,0, {
                        "item_id": x.id,
                        }))

        if not self.settlement_balance_of_loan_ids:
            self.settlement_balance_of_loan_ids = competency


    @api.onchange('employee_id')
    def get_hc_operations(self):
        cfe = self.env['hc.operations'].search([('active_line','=',True)])
        competency = []
        for x in cfe:
            competency.append((0,0, {
                        "item_id": x.id,
                        }))

        if not self.hc_operations_ids:
            self.hc_operations_ids = competency


    def get_date_manager(self):
        for ap in self.approval_history_ids:
            if ap.state == "manager":
                res = ap.date + relativedelta(hours=7)
                return res

    def get_date_hc(self):
        for ap in self.approval_history_ids:
            if ap.state == "hc":
                res = ap.date + relativedelta(hours=7)
                return res

    def get_date_employee(self):
        for ap in self.approval_history_ids:
            if ap.state == "done":
                res = ap.date + relativedelta(hours=7)
                return res



    def get_management_mail(self):
        email = []
        for ln in self.company_facility_equipment_ids:
            if ln.checked == 'asset_management':
                email = ln.employee_id.work_email
        for ln in self.it_security_access_ids:
            if ln.checked == 'asset_management':
                email = ln.employee_id.work_email
        for ln in self.settlement_balance_of_loan_ids:
            if ln.checked == 'asset_management':
                email = ln.employee_id.work_email
        for ln in self.hc_operations_ids:
            if ln.checked == 'asset_management':
                email = ln.employee_id.work_email
        return email

    def get_management_mail_cc(self):
        email = "Human.Capital@xapiens.id,"
        for ln in self.company_facility_equipment_ids:
            if ln.checked != 'asset_management':
                email += ln.employee_id.work_email + ","
        for ln in self.it_security_access_ids:
            if ln.checked != 'asset_management':
                email += ln.employee_id.work_email + ","
        for ln in self.settlement_balance_of_loan_ids:
            if ln.checked != 'asset_management':
                email += ln.employee_id.work_email + ","
        for ln in self.hc_operations_ids:
            if ln.checked != 'asset_management':
                email += ln.employee_id.work_email + ","
        return email

    def get_management_name(self):
        name = []
        for ln in self.company_facility_equipment_ids:
            if ln.checked == 'asset_management':
                name = ln.employee_id.name
        for ln in self.it_security_access_ids:
            if ln.checked == 'asset_management':
                name = ln.employee_id.name
        for ln in self.settlement_balance_of_loan_ids:
            if ln.checked == 'asset_management':
                name = ln.employee_id.name
        for ln in self.hc_operations_ids:
            if ln.checked == 'asset_management':
                name = ln.employee_id.name
        return name



    def get_mail_hc(self):
        email = []
        for ln in self.company_facility_equipment_ids:
            if ln.checked == 'hc':
                email = ln.employee_id.work_email
        for ln in self.it_security_access_ids:
            if ln.checked == 'hc':
                email = ln.employee_id.work_email
        for ln in self.settlement_balance_of_loan_ids:
            if ln.checked == 'hc':
                email = ln.employee_id.work_email
        for ln in self.hc_operations_ids:
            if ln.checked == 'hc':
                email = ln.employee_id.work_email
        return email


    def get_mail_hc_cc(self):
        email = "Human.Capital@xapiens.id,"
        for ln in self.company_facility_equipment_ids:
            if ln.checked != 'hc':
                email += ln.employee_id.work_email + ","
        for ln in self.it_security_access_ids:
            if ln.checked != 'hc':
                email += ln.employee_id.work_email + ","
        for ln in self.settlement_balance_of_loan_ids:
            if ln.checked != 'hc':
                email += ln.employee_id.work_email + ","
        for ln in self.hc_operations_ids:
            if ln.checked != 'hc':
                email += ln.employee_id.work_email + ","
        return email


    def get_name_hc(self):
        name = []
        for ln in self.company_facility_equipment_ids:
            if ln.checked == 'hc':
                name = ln.employee_id.name
        for ln in self.it_security_access_ids:
            if ln.checked == 'hc':
                name = ln.employee_id.name
        for ln in self.settlement_balance_of_loan_ids:
            if ln.checked == 'hc':
                name = ln.employee_id.name
        for ln in self.hc_operations_ids:
            if ln.checked == 'hc':
                name = ln.employee_id.name
        return name






    def send_mail_manager(self):
        email = self.manager_id.work_email
        template = self.env.ref('x_hr_resignation.template_mail_submits_resignation')
        template.email_to = email
        template.send_mail(self.id, force_send=True)


    def _compute_attachment_number(self):
        attachment_data = self.env['ir.attachment'].read_group([('res_model', '=', 'hr.resignation'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for expense in self:
            expense.attachment_number = attachment.get(expense.id, 0)

    def get_url(self):
        self.ensure_one()
        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
        message_body = base_url
        return message_body

    @api.onchange('employee_id')
    def get_data_employee(self):
        employee = self.employee_id
        self.employee_id_number = employee.employee_id_number
        self.job_id = employee.job_id.id
        self.department_id = employee.department_id.id
        self.manager_id = employee.parent_id.id


    def action_get_attachment_view(self):
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('base', 'action_attachment')
        res['domain'] = [('res_model', '=', 'hr.resignation'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'hr.resignation', 'default_res_id': self.id}
        return res


    def action_submitted(self):
        fc = 0
        wc = 0
        for ls in self.company_facility_equipment_ids:
            if ls.checked == 'asset_management':
                fc += 1
            if ls.checked == 'hc':
                wc += 1
        for wk in self.it_security_access_ids:
            if wk.checked == 'asset_management':
                fc += 1
            if wk.checked == 'hc':
                wc += 1
        for ah in self.settlement_balance_of_loan_ids:
            if ah.checked == 'asset_management':
                fc += 1
            if ah.checked == 'hc':
                wc += 1
        for ms in self.hc_operations_ids:
            if ms.checked == 'asset_management':
                fc += 1
            if ms.checked == 'hc':
                wc += 1
        if fc > 1 or wc > 1 or fc < 1 or wc < 1:
            raise UserError(_('Please Check Human Resource And Asset Management !!'))
        state = 'manager'
        email = self.manager_id.work_email
        template = self.env.ref('x_hr_resignation.template_mail_submits_resignation')
        template.email_to = email
        template.send_mail(self.id, force_send=True)
        user = self.env.user
        wkj = [(0,0,{
            'state' : "Submitted",
            'comment' : " ",
            'user_id' : user.id
            })]

        self.approval_history_ids = wkj
        self.state = state


    def action_resignation(self):
        return {
                'name' : _("Approve With Comment"),
                'view_type' : 'form',
                'res_model' : 'approval.state.wizard',
                'view_mode' : 'form',
                'type':'ir.actions.act_window',
                'target': 'new',
            }

    def action_resignation_reject(self):
        return {
                'name' : _("Reject With Comment"),
                'view_type' : 'form',
                'res_model' : 'approval.state.reject.wizard',
                'view_mode' : 'form',
                'type':'ir.actions.act_window',
                'target': 'new',
            }

class ApprovalHistory(models.Model):
    _name = "approval.history"
    _rec_name = "state"
    _description = "Role history approval"

    resignation_id = fields.Many2one('hr.resignation','Resignation')
    state = fields.Char(string='Status', track_visibility="always")
    user_id = fields.Many2one("res.users","User")
    comment = fields.Char("Comment")
    date = fields.Datetime("Date", default=fields.Datetime.now())


class CheckedReceived(models.Model):
    _name = 'checked.received'
    _rec_name = 'name'

    name = fields.Char(string="Name")
    employee_id = fields.One2many("hr.employee",'checked_id',string="Employee")


class CompanyFacilityEquipmentLine(models.Model):
    _name = 'company.facility.equipment.line'
    _rec_name = 'sequence'

    
    sequence = fields.Integer("Sequence")
    item_id = fields.Many2one("company.facility.equipment","Item")
    description = fields.Char("Description")
    amount = fields.Integer("Amount")
    settlement_date = fields.Date("Settlement Date")
    checked_id = fields.Many2one('checked.received','Checked And Received By', copy=False)
    employee_id = fields.Many2one('hr.employee', string="Name")
    resignation_id = fields.Many2one('hr.resignation','Resignation')
    checked = fields.Selection(selection=RESIGNATION_TYPE_LINE, string="Send Mail By", track_visibility="always")



class ItSecurityAccessLine(models.Model):
    _name = 'it.security.access.line'
    _rec_name = 'sequence'


    sequence = fields.Integer("Sequence")
    item_id = fields.Many2one("it.security.access","Item")
    description = fields.Char("Description")
    amount = fields.Integer("Amount")
    settlement_date = fields.Date("Settlement Date")
    checked_id = fields.Many2one('checked.received','Checked And Received By', copy=False)
    employee_id = fields.Many2one('hr.employee', string="Name")
    resignation_id = fields.Many2one('hr.resignation','Resignation')
    checked = fields.Selection(selection=RESIGNATION_TYPE_LINE, string="Send Mail By", track_visibility="always")


class SettlementBalanceOfLoanLine(models.Model):
    _name = 'settlement.balance.of.loan.line'
    _rec_name = 'sequence'


    sequence = fields.Integer("Sequence")
    item_id = fields.Many2one("settlement.balance.of.loan","Item")
    description = fields.Char("Description")
    amount = fields.Integer("Amount")
    settlement_date = fields.Date("Settlement Date")
    checked_id = fields.Many2one('checked.received','Checked And Received By', copy=False)
    employee_id = fields.Many2one('hr.employee', string="Name")
    resignation_id = fields.Many2one('hr.resignation','Resignation')
    checked = fields.Selection(selection=RESIGNATION_TYPE_LINE, string="Send Mail By", track_visibility="always")


class HcOperationsLine(models.Model):
    _name = 'hc.operations.line'
    _rec_name = 'sequence'

    sequence = fields.Integer("Sequence")
    item_id = fields.Many2one("hc.operations","Item")
    description = fields.Char("Description")
    amount = fields.Integer("Amount")
    settlement_date = fields.Date("Settlement Date")
    checked_id = fields.Many2one('checked.received','Checked And Received By', copy=False)
    employee_id = fields.Many2one('hr.employee', string="Name")
    resignation_id = fields.Many2one('hr.resignation','Resignation')
    checked = fields.Selection(selection=RESIGNATION_TYPE_LINE, string="Send Mail By", track_visibility="always")



class TransferJobLine(models.Model):
    _name = 'transfer.job.line'
    _rec_name = 'sequence'

    sequence = fields.Integer("Sequence")
    item_id = fields.Many2one("transfer.job","Kind Of Job")
    employee_id = fields.Many2one('hr.employee', string="Receiver")
    veryfied_by_manager = fields.Boolean(string="Veryfied By Manager")
    resignation_id = fields.Many2one('hr.resignation','Resignation')




class CompanyFacilityEquipment(models.Model):
    _name = 'company.facility.equipment'
    _rec_name = 'name'


    name = fields.Char("Item")
    active_line = fields.Boolean("Active On Line")


class ItSecurityAccess(models.Model):
    _name = 'it.security.access'
    _rec_name = 'name'

    name = fields.Char("Item")
    active_line = fields.Boolean("Active On Line")


    
class SettlementBalanceOfLoan(models.Model):
    _name = 'settlement.balance.of.loan'
    _rec_name = 'name'

    name = fields.Char("Item")
    active_line = fields.Boolean("Active On Line")

class HcOperations(models.Model):
    _name = 'hc.operations'
    _rec_name = 'name'

    name = fields.Char("Item")
    active_line = fields.Boolean("Active On Line")


class TransferJob(models.Model):
    _name = 'transfer.job'
    _rec_name = 'name'

    name = fields.Char("Kind Of Job")



class ResignationReason(models.Model):
    _name = 'resignation.reason'
    _rec_name = 'name'

    name = fields.Char("Reason")




class MaritalStatus(models.Model):
    _name = 'marital.status'
    _rec_name = 'name'

    name = fields.Char("Name")


