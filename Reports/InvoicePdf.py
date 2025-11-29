from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5, A4
import io
import reportlab.rl_config
from jdatetime import datetime as jdatetime
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from Setting import settings


class InvoicePdf:
    def __init__(self, pagesize=A5):
        self.pagesize = pagesize
        self.buffer = io.BytesIO()
        self.pdf = canvas.Canvas(self.buffer, self.pagesize)

    def build(self, order, packBox_invoice) -> str:
        farsi_font_path = settings.FARSI_FONT_PATH
        pdfmetrics.registerFont(TTFont("FarsiFont", farsi_font_path))

        Arial_font_path = settings.ARIAL_FONT_PATH
        pdfmetrics.registerFont(TTFont("ArialFont", Arial_font_path))
        reportlab.rl_config.canvas_basefontname = "ArialFont"

        karen_image_path = settings.BRAND_IMAGE_PATH
        self.pdf.drawImage(karen_image_path, 100, 560, 200, 25)

        # __________________Part1______________________
        self.pdf.setFont("FarsiFont", 14)

        customer_name = self.convert_to_farsi("نام مشتری:")
        self.pdf.drawRightString(380, 520, customer_name)
        farsi_name = order.customer.name
        farsi_name_display = self.convert_to_farsi(farsi_name)
        self.pdf.drawRightString(325, 520, farsi_name_display)

        mobile_string = self.convert_to_farsi("موبایل:")
        self.pdf.drawRightString(380, 495, mobile_string)
        customer_mobile = order.customer.phone
        customer_mobile_display = self.convert_to_farsi(customer_mobile)
        self.pdf.drawRightString(325, 495, customer_mobile_display)

        order_number = self.convert_to_farsi("شماره سفارش:")
        self.pdf.drawRightString(170, 520, order_number)
        self.pdf.drawString(65, 520, str(order.id))

        date_string = self.convert_to_farsi("تاریخ:")
        self.pdf.drawRightString(170, 495, date_string)
        jdate = jdatetime.fromgregorian(datetime=order.order_time)
        self.pdf.drawRightString(125, 495, str(jdate.strftime("%Y-%m-%d")))

        # _________________Part2______________________

        table = self.prepare_pdf_order_table(order)
        table.wrapOn(self.pdf, 0, 0)
        w = (420 - table._width) / 2
        table_height = table._height
        available_height = 460
        starting_y = available_height - table_height
        table.drawOn(self.pdf, w, starting_y)

        self.pdf.setFont("Helvetica-Bold", 12)

        total_y = available_height - table_height - 20
        padding = 5

        total_text_width = self.pdf.stringWidth("Total:", "Helvetica", 12)
        price_text_width = self.pdf.stringWidth(str(order.totalPrice), "Helvetica", 12)

        # Calculate the width of the border based on the content width
        border_width = total_text_width + price_text_width + (3 * padding)

        self.pdf.rect(260 - padding, total_y - padding, border_width, 10 + (2 * padding))

        self.pdf.drawString(260, total_y, "Total:")
        self.pdf.drawString(260 + total_text_width + 5, total_y, "{:,.0f}".format(order.totalPrice))

        # ___________________Part3_______________
        self.pdf.setFont("FarsiFont", 11)
        # self.pdf.drawRightString(380, total_y - 35, unit_text)
        if packBox_invoice:
            packBox_text = self.convert_to_farsi(settings.PACKBOX_MESSAGE)
            self.pdf.drawRightString(380, total_y - 35, packBox_text)
            payment_text = self.convert_to_farsi(settings.PAYMENT_MESSAGE)
            self.pdf.drawRightString(380, total_y - 50, payment_text)
        else:
            payment_text = self.convert_to_farsi(settings.PAYMENT_MESSAGE)
            self.pdf.drawRightString(380, total_y - 40, payment_text)

        self.pdf.setFont("FarsiFont", 8)
        brand_text = self.convert_to_farsi(settings.BRAND_TEXT_MESSAGE)
        self.pdf.drawRightString(380, 15, brand_text)

        footer_image = settings.FOOTER_IMAGE_PATH
        self.pdf.drawImage(footer_image, 10, 10, 130, 80)

        self.pdf.save()

        # Save the PDF to a file
        file_name = f"sales_invoice{order.id}.pdf"
        output_path = settings.OUTPUT_DIR / file_name
        with open(output_path, "wb") as file:
            file.write(self.buffer.getvalue())

        return output_path

    @classmethod
    def convert_to_farsi(cls, text):
        reshaped_name = arabic_reshaper.reshape(text)
        farsi_name_display = get_display(reshaped_name)
        return farsi_name_display

    @classmethod
    def prepare_pdf_order_table(cls, the_order):
        table_data = [["Code", "Product", "Quantity", "Price\n(Rials)"]]
        for row in the_order.rows:
            table_data.append([
                row.product.code,
                row.product.name,
                str(row.quantity),
                "{:,.0f}".format(row.rowPrice)])

        table_style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black)])

        table = Table(table_data)
        table.setStyle(table_style)
        return table
