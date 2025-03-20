from odoo import models, fields, api
import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class WebsiteCourseEnrollment(models.Model):
    _name = 'website.course.enrollment'
    _description = 'Course Enrollment'

    name = fields.Char(string="Student Name", required=True)
    email = fields.Char(string="Email")
    course_id = fields.Many2one('product.template', string="Course")
    progress = fields.Float(string="Progress", default=0.0)
    certificate_generated = fields.Boolean(string="Certificate Generated", default=False)
    certificate_pdf = fields.Binary(string="Certificate PDF", attachment=True)

    def generate_certificate(self):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.drawString(100, 750, f"Certificate of Completion")
        pdf.drawString(100, 700, f"This certifies that {self.name} has successfully completed the course: {self.course_id.name}.")
        pdf.save()
        buffer.seek(0)
        self.certificate_pdf = base64.b64encode(buffer.read())
        self.certificate_generated = True
        buffer.close()