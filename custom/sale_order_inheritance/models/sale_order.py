from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # PO Information
    po_path = fields.Char(string="PO Path", help="Path to Purchase Order document")
    po_number = fields.Char(string="PO Number", help="Purchase Order Number")
    
    # General Information
    note = fields.Text(string="Note", help="General notes for the order")
    
    # Print Legal with default value
    print_legal = fields.Selection([
        ('dayone', 'Dayone'),
        ('davone', 'Davone'),
        ('other', 'Other')
    ], string="Print Legal", default='davone', help="Print Legal company (default: Davone)")
    
    # Order Classification
    order_type = fields.Selection([
        ('standard', 'Standard'),
        ('express', 'Express'),
        ('bulk', 'Bulk Order'),
        ('custom', 'Custom')
    ], string="Order Type", help="Type of order")
    
    order_status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], string="Order Status", default='draft', help="Current status of the order")
    
    # Delivery Information
    delivery_address = fields.Text(string="Delivery Address", help="Complete delivery address")
    delivery_code = fields.Char(string="Delivery Code", help="Unique delivery identifier")
    
    # Receiver Information
    receiver_info_1 = fields.Char(string="Receiver Info 1", help="Primary receiver information")
    receiver_info_2 = fields.Char(string="Receiver Info 2", help="Secondary receiver information")
    receiver_info_3 = fields.Char(string="Receiver Info 3", help="Tertiary receiver information")
    
    # Receiving Notes
    receiving_note = fields.Text(string="Receiving Note", help="Special notes for delivery/receiving")
