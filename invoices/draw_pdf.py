#!/usr/bin/python
# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Image
from django.utils.translation import ugettext as _
from django.utils.formats import date_format

from django.conf import settings

def template_pdf(mycanvas, invoice):
    """ Draws the invoice """
    mycanvas.translate(0, 29.7 * cm)
    mycanvas.setFont('Times-Roman', 11)

    mycanvas.saveState()
    logo_filename = "%s/%s" % (settings.MEDIA_ROOT, invoice.heading_type.logo_filename.name)
    mycanvas.drawInlineImage(str(logo_filename), 3 * cm, -4 * cm, 400, 80)
    mycanvas.restoreState()

    mycanvas.saveState()
    textobject = mycanvas.beginText(1 * cm, -27 * cm)
    for line in invoice.heading_type.heading_note():
        textobject.textLine(line)
    mycanvas.drawText(textobject)
    mycanvas.restoreState()

    mycanvas.saveState()
    mycanvas.setFont('Times-Roman', 11)
    textobject = mycanvas.beginText(13 * cm, -5.5 * cm)
    textobject.textLine(u'%(place)s, %(date)s' % { 'place': invoice.heading_type.address.town, 'date': date_format(invoice.date)})
    mycanvas.drawText(textobject)
    textobject = mycanvas.beginText(11 * cm, -6.5 * cm)
    textobject.setFont('Times-Bold', 11)
    textobject.textLine(invoice.heading_type.usual_title_respect)
    mycanvas.drawText(textobject)
    textobject = mycanvas.beginText(13 * cm, -6.5 * cm)
    textobject.textLine(u'%s' % invoice.customer)
    textobject.setFont('Times-Roman', 11)
    textobject.textLine(u'%s' % invoice.customer)
    textobject.textLine(u'%s' % invoice.customer.address)
    if invoice.customer.tax_code:
        textobject.textLine(u'%s' % invoice.customer.tax_code)
    elif invoice.customer.vat_code:
        textobject.textLine(u'%s' % invoice.customer.vat_code)
    mycanvas.drawText(textobject)
    mycanvas.restoreState()

    # Info
    textobject = mycanvas.beginText(1 * cm, -10 * cm)
    textobject.setFont('Times-Bold', 11)
    textobject.textLine(_('Invoice n. %(id)s') % {'id': invoice.id})
    mycanvas.drawText(textobject)

    textobject = mycanvas.beginText(1 * cm, -10.5 * cm)
    textobject.setFont('Times-Roman', 11)
    textobject.textLine(_('Payment condition: %(payment)s') % {'payment': invoice.payment_type})
    mycanvas.drawText(textobject)
    textobject = mycanvas.beginText(1 * cm, -11.7 * cm)
    textobject.setFont('Times-Roman', 11)
    textobject.textLine(_('For the selling of'))
    mycanvas.drawText(textobject)

    # Items
    data = [[_('Pieces'),
             _('Description'),
             _('Tax Rate'),
             _('Unit price'),
             _('Amount'),
         ]]

    for voice in invoice.voice_set.all():
        data.append([
            voice.pieces,
            voice.description,
            '%s%%' % voice.vat,
            '%s €' % voice.unit_price_novat,
            '%s €' % voice.amount_novat,
        ])
    data.append([u'', u'', u'', _('Amount nett'), u'%s €' % invoice.amount_novat])
    table = Table(data, colWidths=[1.5 * cm, 8 * cm, 2 * cm, 3 * cm, 3 * cm])
    table.setStyle([
        ('FONT', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
        ('GRID', (0, 0), (-1, -2), 1, (0.7, 0.7, 0.7)),
        ('GRID', (-2, -1), (-1, -1), 1, (0.7, 0.7, 0.7)),
        ('ALIGN', (-2, 0), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
    ])
    tw, th, = table.wrapOn(mycanvas, 15 * cm, 19 * cm)
    table.drawOn(mycanvas, 1 * cm, -12 * cm - th)
    textobject = mycanvas.beginText(11 * cm, -14 *cm - th)
    textobject.setFont('Times-Roman', 12)
    for vat in invoice.tax_rates_used:
        textobject.textLine(_(u'Amount nett for tax rate %(vat)s%%: %(amount)s €') % {'vat': vat, 'amount': invoice.amount_by_vat(vat)})
    textobject.setFont('Times-Bold', 12)
    textobject.textLine(_(u'Invoice amount %(amount)s €') % {'amount': invoice.amount})
    mycanvas.drawText(textobject)
    mycanvas.showPage()
    mycanvas.save()

def draw_pdf(buffer, invoice):
    mycanvas = canvas.Canvas(buffer, pagesize=A4)
    template_pdf(mycanvas, invoice)

def draw_pdf_to_file(invoice, filename):
    mycanvas = canvas.Canvas(filename, pagesize=A4)
    template_pdf(mycanvas, invoice)
