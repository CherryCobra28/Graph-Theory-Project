from reportlab.pdfgen import canvas
import os



def writter(filename,text, image):
    pdf = canvas.Canvas(filename)
    pdf.setTitle(filename)
    textobj = pdf.beginText(40,680)
    for line in text:
        textobj.textLine(line)
    pdf.drawText(textobj)
    pdf.drawImage(image,0,25)
    pdf.save()

def main():
    files = os.listdir('.')
    textfiles = [f for f in files if f.endswith('.txt')]
    images = [f for f in files if f.endswith('.png')]
    fileim = tuple(zip(textfiles, images))
    for textfile, image in fileim:
        filename = textfile.replace('.txt','.pdf').replace('01','02')
        print(filename)
        with open(textfile) as textf:
            lines = textf.readlines()
            lines = [line.strip('\n') for line in lines ]
        writter(filename,lines,image)    
    
    
    
if __name__ == '__main__':
    main()