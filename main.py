from PyPDF2 import PdfMerger
import subprocess as sp
import os, os.path
import shutil
import glob


os.chdir(os.getcwd()+'/Files')

# function that merges pdfs
def merge_pdfs(root, pdf_names):
    merger = PdfMerger()
    is_added = False
    for pdf in sorted(list(set(pdf_names))):
        if (not pdf=="merged.pdf") and pdf.endswith(".pdf"):
            is_added = True
            merger.append(open(os.path.join(root, pdf), 'rb'))
    back_root = ""
    for i in range(len(root.split("/"))):
        if not i==len(root.split("/"))-1:
            back_root += root.split("/")[i]+"/"
    if is_added:
        merger.write(os.path.join(back_root, root.split("/")[-1]+".pdf"))
        merger.close()
        return True
    return False

def remove_thing(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)

def del_directory(path):
    for i in glob.glob(os.path.join(path, '*')):
        remove_thing(i)
    remove_thing(path)

def walk(path):
    lis = []
    for root, dirs, files in os.walk(path):
        if (len(dirs)==0) and (not len(files)==0):
            lis.append(root)
            continue
        for dir in dirs:
            for i in walk(os.path.join(root, dir)):
                lis.append(i)
    return(sorted(list(set(lis))))

x=False
counter = 0
for i in walk('.'):
    try:
        res = merge_pdfs(i, os.listdir(i))
        if res:
            Path = i[1:]
            print('files in :', (os.getcwd()+Path)[:40]+'...'*(len(os.getcwd()+Path)>40))
            del_directory(os.getcwd()+Path)
            print("Merge successful\n")
            counter += 1
            if x:
                print("\n"*1)
                x=True
    except:
        print("\n\nAn issue occurred while merging pdfs")
        exit(1)

print("\n")
print(counter, "PDFs merged")

