"""
Clever Badge maker

Creates a Kindergarten.pdf file with all K student badges 
 in an easlily cuttable format.
In folder PrettyBadges leaves a PDF for each student in case of lost badge.

Create folder PrettyBadges in directory with script.

Need to download clever badges from Clever and unzip Kindergarten folder to this folder

Have a jpg of your logo in folder with script. 
Name of this file is contained in config.ini

Have a csv of your student data available.
The path and file name of the csv are in the config.ini

The csv needs these headers:
StudentID, LastName, FirstName, Homeroom Teacher, GradeLevel
The grade level needs to be KF in csv file for badges to be printed.

"""


import os
import configparser
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch, mm
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.flowables import BalancedColumns
from reportlab.platypus.frames import ShowBoundaryValue
from reportlab.lib.enums import TA_JUSTIFY,TA_LEFT,TA_CENTER,TA_RIGHT

badgePath = 'Kindergarten\\student_pngs\\'

config = configparser.ConfigParser()
config.read('config.ini')
bad_chars = [';', ':', '!', "*","-","'",".","(",")"] #list of what is to be removed from user string

dataFrame =  pd.read_csv(config['hostpath']['hostPath'] + \
                        config['hostpath']['fileName'])

class CleverBadge(Flowable):
    """
    Creates a badge with infor and logo
    """
    def __init__(self, x=0,y=0,width = 3.5*inch, height=3.5*inch, name='Student Name', teacher='Teacher name', badge='Kindergarten\\student_pngs\\sample-123456.png'):
        Flowable.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.teacher = teacher
        self.badge = badge
        self.styles = getSampleStyleSheet()

    def coord(self, x, y, unit = 1):
        """
        position in canvas object
        """
        x, y = x *unit, self.height - y * unit
        return x, y

    def draw(self):
        """
        draw badge
        """
        self.canv.rect(self.x, self.y, self.width, self.height)
        qrCode =  Image(self.badge, width=2*inch, height=2*inch)
        qrCode.wrapOn(self.canv, self.width, self.height)
        qrCode.drawOn(self.canv, *self.coord(self.x+.75,3.4,inch))
        myImage =  Image(config['image']['imagefile'], width=1*inch, height=1*inch)
        myImage.hAlign = 'CENTER'
        myImage.wrapOn(self.canv, self.width, self.height)
        myImage.drawOn(self.canv, *self.coord(self.x+1.25,1.4,inch))
        

        
        p = Paragraph(self.name, style=self.styles["Title"])

        
        p.wrapOn(self.canv, self.width, self.height)
        p.drawOn(self.canv, *self.coord(self.x, .4, inch))
        p = Paragraph(self.teacher, style=self.styles["Normal"])
        p.wrapOn(self.canv, self.width, self.height)
        p.drawOn(self.canv, *self.coord(self.x+.2, 3.4, inch))


#start a doc for the whole grade
docFullGrade = BaseDocTemplate("Kindergarten.pdf",leftMargin=.5, rightMargin=.25, pagesize=letter)
frame1 = Frame(.5*inch,docFullGrade.bottomMargin,3.5*inch,docFullGrade.height,rightPadding=0,leftPadding=0,bottomPadding=0,topPadding=0,id='col1')
frame2 = Frame(4*inch,docFullGrade.bottomMargin,3.5*inch,docFullGrade.height,rightPadding=0,leftPadding=0,bottomPadding=0,topPadding=0,id='col2')

docFullGrade.addPageTemplates([PageTemplate(id='TwoCol',frames=[frame1,frame2]), ])

#start a story for the whole grade
story=[]
    
for index, student in dataFrame.iterrows():
    if student['GradeLevel'] == 'KF':

        studentStory =[]
        lastNameLower = student['LastName'].lower()
        for bad in bad_chars:
            lastNameLower = lastNameLower.replace(bad, '')
        lastNameLower = lastNameLower.replace(' ','_')
        badgePNG = badgePath + lastNameLower + '-' + str(student['StudentID']) + '.png'
        filename = "PrettyBadges\\" + student['Homeroom Teacher'] + student['LastName'] + ".pdf"
        studentName = student['FirstName'] + ' ' + student['LastName']
        teacherName = student['Homeroom Teacher']

        box = CleverBadge(name=studentName, teacher=teacherName, badge=badgePNG)

        story.append(box)

        studentDoc = SimpleDocTemplate(filename,pagesize=letter)
        studentStory.append(box)
        studentDoc.build(studentStory)


docFullGrade.build(story)
