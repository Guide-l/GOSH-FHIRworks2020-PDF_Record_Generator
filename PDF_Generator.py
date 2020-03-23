from reportlab.pdfgen import canvas
from fhir_parser import FHIR
from tkinter import *
from tkinter import messagebox



class TemplateGenerator:

    def __init__(self, pdf):
        self.pdf = pdf

    def createTemplate(self):
        leftMargin = 60

        self.pdf.setFont('Times-Bold', 30)
        self.pdf.drawCentredString(300, 770, "Patient Record")

        self.pdf.setFont('Helvetica', 12)
        self.pdf.drawString(leftMargin, 690, "Medical Record Number (ID):")
        self.pdf.line(218, 690, 530, 690)
        self.pdf.drawString(leftMargin, 660, "Patient Name:")
        self.pdf.line(137, 660, 530, 660)
        self.pdf.drawString(leftMargin, 630, "Gender:")
        self.pdf.drawString(135, 630, "M")
        self.pdf.drawString(180, 630, "F")
        self.pdf.drawString(225, 630, "Date of Birth:")
        self.pdf.line(296, 630, 530, 630)
        self.pdf.drawString(leftMargin, 600, "Address:")
        self.pdf.line(109, 600, 338, 600)
        self.pdf.drawString(340, 600, "City:")
        self.pdf.line(366, 600, 530, 600)
        self.pdf.drawString(leftMargin, 570, "State:")
        self.pdf.line(92, 570, 210, 570)
        self.pdf.drawString(212, 570, "Zip Code:")
        self.pdf.line(265, 570, 360, 570)
        self.pdf.drawString(362, 570, "Country:")
        self.pdf.line(408, 570, 530, 570)
        self.pdf.drawString(leftMargin, 540, "Phone:")
        self.pdf.line(100, 540, 530, 540)
        self.pdf.drawString(leftMargin, 510, "Marital Status:")
        self.pdf.line(138, 510, 530, 510)
        self.pdf.drawString(leftMargin, 480, "Social Security Number:")
        self.pdf.line(190, 480, 530, 480)
        self.pdf.drawString(leftMargin, 450, "Driver License:")
        self.pdf.line(141, 450, 530, 450)
        self.pdf.drawString(leftMargin, 420, "Passport Number:")
        self.pdf.line(158, 420, 530, 420)
        return self.pdf


class Filler:

    def __init__(self, patient):
        self.patient = patient

    def fill(self, pdf):

        pdf.drawCentredString(375, 692, self.patient.uuid)
        pdf.drawCentredString(335, 662, self.patient.full_name())
        if self.patient.gender == "female":
            pdf.circle(183, 634, 15, stroke=1, fill=0)
        else:
            pdf.circle(140, 634, 15, stroke=1, fill=0)
        pdf.drawCentredString(410, 632, str(self.patient.birth_date))
        address = str(self.patient.addresses[0]).splitlines()
        address_1 = address[0]
        address_2 = address[1].split(",")
        address_3 = address[2].split(",")
        pdf.drawCentredString(220, 602, address_1)
        pdf.drawCentredString(445, 602, address_2[0])
        pdf.drawCentredString(150, 572, address_2[1])
        pdf.drawCentredString(310, 572, address_3[0])
        pdf.drawCentredString(465, 572, address_3[1])
        pdf.drawCentredString(300, 542, str(self.patient.telecoms[0]).replace("home phone: ", ""))
        pdf.drawCentredString(330, 512, str(self.patient.marital_status))
        pdf.drawCentredString(370, 482, str(self.patient.identifiers[2]).replace("Social Security Number ", ""))
        pdf.drawCentredString(332, 452, str(self.patient.identifiers[3]).replace("Driver's License ", ""))
        pdf.drawCentredString(350, 422, str(self.patient.identifiers[4]).replace("Passport Number ", ""))
        return pdf


class Controller:

    def __init__(self):
        self.pdf = canvas.Canvas("Record.pdf")
        self.pdf.setTitle("Patient Record")
        fhir = FHIR()
        self.patients_lists = fhir.get_all_patients()

    def searchID(self,id):
        for patient in self.patients_lists:
            if str(patient.identifiers[0]).replace(" ","") == str(id):
                return patient
        return None

    def createDoc(self, patient):
        filler = Filler(patient)
        templateGen = TemplateGenerator(self.pdf)
        self.pdf = templateGen.createTemplate()
        self.pdf = filler.fill(self.pdf)
        self.pdf.save()
        return self.pdf

    def main(self):
        id = input("Enter patient ID: ")
        patient = self.searchID(id)
        if patient is None:
            print ("ID Not Found")
        else:
            self.createDoc(patient)


class Gui:

    def __init__(self):
        self.window = Tk()
        self.window.title("DocFiller")
        self.window.geometry('400x300')
        self.controller = Controller()

    def run(self):
        lbl = Label(self.window, text="Enter Patient ID", font=("Arial Bold", 50))
        lbl.grid(column=0, row=0)
        txt = Entry(self.window, width=30)
        txt.grid(column=0, row=1)

        def clicked():
            id = txt.get()
            if self.controller.searchID(id) is None:
                messagebox.showerror('Error', 'ID Not Found')  # shows error message
            else:
                self.controller.createDoc(self.controller.searchID(id))
                messagebox.showinfo('Saved', 'PDF record of patient: '+ id+' has been created.')

        btn = Button(self.window, text="Create PDF Record", command=clicked)

        btn.grid(column=0, row=2)

        self.window.mainloop()

gui = Gui()
gui.run()