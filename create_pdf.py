import argparse
import PyPDF2
import re
from os import path
import os

def tyfq(shorthand):
    res = re.match(r"^(ab|AB|BC|bc|)(\d{2}|\d{4})(a|b|A|B|#)([1-6])$",shorthand)
    if (res is None):
        return None
    t,y,f,q = res.groups()
    if len(y) ==2:
        if y[0] == '9':
            y = '19'+y
        else:
            y = '20' + y
    # y = ('20' + y) if ((y[0]!=9) and (len(y)<=2)) else (('19'+y) if len(y) <= 2 else y)
    # print(y)
    q = int(q)
    f = f.upper()
    t = t.upper()
    f = 'A' if f=='#' else f
    t = 'AB' if t=='' else t

    if (y == '1998' and t=='BC'):
        q += 2
    elif (y == '1998' and t=='AB'):
            q += 1 if (q > 2) else 0

    return t,y,f,q

def frq_file(s):
    rr = tyfq(s)
    if rr is None:
        return None
    t,y,f,q = rr
    # print(t,y,f,q)
    p = path.join("FRQs",t,y,f"{f}.pdf")
    if (path.exists(p) and path.isfile(p)):
        return p,q
    
    return None

def get_question(f):
    ff = frq_file(f)
    if ff is None:
        return None
    p,q = ff

    if p is not None:
        with open(p, 'rb') as file:
            fr = PyPDF2.PdfReader(file)
            frq_page = int(q)
            if (frq_page < len(fr.pages)):  
                page = fr.pages[frq_page]
                pw = PyPDF2.PdfWriter()
                pw.add_page(page)
                return pw
    return None

def frqs_pdf(frqs,outfile):
    pw = PyPDF2.PdfWriter()
    # creating an object
    for p,q in [frq_file(f) for f in frqs if frq_file(f) is not None]:
        if p is not None: 
            with open(p, 'rb') as file:
                fileReader = PyPDF2.PdfReader(file)
                frq_page = int(q)
                if (frq_page < len(fileReader.pages)):  
                    page = fileReader.pages[frq_page]
                    pw.add_page(page)
    with open(outfile, 'wb') as fo:
        pw.write(fo)

parser = argparse.ArgumentParser(
                    prog='FRQ PDF Creator',
                    description='Takes a list of FRQs and produces a PDF containing all of the questions',
                    epilog='By NifleySnifley')      
parser.add_argument("-o","--output", type=str, required=True) 
parser.add_argument('-i',"--infile", type=argparse.FileType('r'), required=False)
parser.add_argument("frqs", nargs='*')

if __name__=="__main__":
    args = parser.parse_args()
    # print(args)

    if (args.infile is not None):
        args.frqs = [line.strip().split()[0] for line in args.infile.readlines()]

    frqs_pdf(args.frqs, args.output)
