"""
Python XML Parser
1. Tkinter GUI
2. Remove duplicates from an xml
3. Create backup of the original
"""

import re
import sys
import ntpath
import xml.dom.minidom
from tkinter import filedialog
from tkinter import Frame, Tk, BOTH, Text, Menu, END

ntpath.basename("a/b/c")
global_file = ""


class BrowseFile(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("XML Parser")
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu2 = Menu(menubar)
        fileMenu.add_command(label="Add File", command=self.onOpen)
        fileMenu.add_command(label="Exit", command=self.onExit)
        fileMenu2.add_command(label="Remove Duplicates",
                              command=self.clearFrame)
        menubar.add_cascade(label="File", menu=fileMenu)
        menubar.add_cascade(label="Action", menu=fileMenu2)

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)

    def onExit(self):
        sys.exit()

    def onOpen(self):
        ftypes = [('XML Files', '*.xml')]
        dlg = filedialog.Open(self, filetypes=ftypes)
        fl = dlg.show()

        # destroying old frame & creating new - incase of a new file
        self.txt.destroy()
        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)

        self.txt.insert(END, "File - " + fl + "\n\n")

        if fl != '':
            text = self.readFile(fl)
            self.txt.insert(END, text)

    def readFile(self, filename):
        global global_file
        global_file = filename

        f = open(filename, "r")
        text = f.read()
        f.close()
        return text

    def clearFrame(self):
        global global_file

        if (global_file == ""):
            self.txt.destroy()
            self.txt = Text(self)
            self.txt.pack(fill=BOTH, expand=1)
            self.txt.insert(END, "Choose a valid XML file first\n")
            return
        else:
            self.txt.destroy()
            self.txt = Text(self)
            self.txt.pack(fill=BOTH, expand=1)
            #self.txt.insert(END, "Processing File....\n")

            res = self.removeDuplicateEntries(global_file)
            self.txt.insert(END, res + "\n")

    def createBackup(self, filename):
        backup_xml = self.path_get(filename)
        new_backupXML = backup_xml.split(".")
        backup_xml = new_backupXML[0]+"_Backup"+".xml"

        with open(filename) as rFile:
            with open(backup_xml, "w") as wFile:
                for line in rFile:
                    wFile.write(line)

            rFile.close()
        return "Backup created successfully"

    def path_get(self, filename):
        head, tail = ntpath.split(filename)
        return tail or ntpath.basename(head)

    def removeDuplicateEntries(self, filename):
        backupRet = self.createBackup(filename)
        # print(backupRet)
        self.txt.insert(END, backupRet + "\n")
        xmlfile_name = self.path_get(filename)
        # print(xmlfile_name)

        with open(filename, 'r') as filehandle:
            documentXML = xml.dom.minidom.parse(filehandle)
            references = []

            for indexNode in documentXML.getElementsByTagName('primary-node-here'):
                # print("indexNode: %s" % indexNode.toxml())
                subNode = indexNode.childNodes[0]
                # print("page number : %s" % subNode.toxml())
                if subNode.nodeType == 3:
                    pageNumber = subNode.nodeValue

                indexNodeFollows = indexNode.nextSibling
                if indexNodeFollows.nodeName == "node-followed-by-primary-node-here":
                    # print("indexNodeFollows: %s" % indexNodeFollows.toxml())
                    firstSubNode = indexNodeFollows.childNodes[0]
                    description = firstSubNode.nodeValue
                    if description is not None:
                        # print("subnode  : %s" % description)

                        # look for succeeding nodes with the same description value
                        for similarNode in documentXML.getElementsByTagName('node-followed-by-primary-node-here'):
                            firstChildNode = similarNode.childNodes[0]
                            description2 = firstChildNode.nodeValue
                            if description == description2:
                                indexNodePrevious = similarNode.previousSibling
                                indexNodePreviousSubNode = indexNodePrevious.childNodes[0]
                                if indexNodePreviousSubNode.nodeType == 3:
                                    pageNumber2 = indexNodePreviousSubNode.nodeValue
                                    if (int(pageNumber) < int(pageNumber2)):
                                        print("subnode  : %s" % description)
                                        print(
                                            "similar index entry on page %s detected" % pageNumber2)
                                        #self.txt.insert(END, "subnode  : %s" % description + "\n")
                                        #self.txt.insert(END, "similar index entry on page %s detected" % pageNumber2 + "\n")

                                        # create an entry to remember which indexes to remove
                                        entry = {
                                            "pageNumber": pageNumber,
                                            "description": description
                                        }
                                        references.append(entry)

            # close the connection to that file
            filehandle.close()

        # print entries to be removed:
        for entry in references:
            print("%6s: %s" % (entry["pageNumber"], entry["description"]))

            indexItem = documentXML.getElementsByTagName("index-node-here")[0]
            # print(indexItem.childNodes)
            for child in indexItem.childNodes:
                if child.nodeName == "node-followed-by-primary-node-here":
                    childNodePrevious = child.previousSibling
                    if childNodePrevious.nodeName == "primary-node-here":
                        # print("examining primary node")
                        # print(childNodePrevious.toxml())
                        pageNumber2 = childNodePrevious.childNodes[0].nodeValue
                        # print("comparing %s with %s" % (pageNumber2, entry["pageNumber"]))
                        if int(pageNumber2) == int(entry["pageNumber"]):
                            indexItem.removeChild(child)
                            indexItem.removeChild(childNodePrevious)

        with open(xmlfile_name, 'w') as filehandle:
            filehandle.write(documentXML.toxml(encoding="utf-8"))
            filehandle.close()

        # removing line spaces
        with open(xmlfile_name) as xmlfile:
            lines = [line for line in xmlfile if line.strip() is not ""]
            xmlfile.close()
        with open(xmlfile_name, "w") as xmlfile:
            xmlfile.writelines(lines)
            xmlfile.close()

        return "Duplicates removed successfully"


def main():
    root = Tk()
    ex = BrowseFile(root)
    root.mainloop()


if __name__ == '__main__':
    main()
