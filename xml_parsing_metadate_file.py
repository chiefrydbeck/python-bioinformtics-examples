## Based on http://code.activestate.com/recipes/410469/ 
##and http://stackoverflow.com/questions/3207219/how-to-list-all-files-of-a-directory-in-python 
##SHOULD STAND IN A FOLDER CONTAINING PACBIO PROJECTFOLDERS WHEN USING THIS SCRIPT
import xml.etree.ElementTree as ElementTree
from glob import glob
from os.path import join
from os import getcwd
from os import walk

class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself 
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a 
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})
## end of http://code.activestate.com/recipes/410469/
                
#ask for project folder names
pacBioProjFolders = raw_input('Enter the project folder names: ')
pbf = pacBioProjFolders.split()
print " "
print "ProjectFolder SMRTcell SampleID"
#for each folder
for  pacBioProjFold in pbf:
    #get the subfolders
    f = []
    #counter needed to get SMRTcell foldername corresponding to metadatafile
    counter = 0
    # get list of subfolder names (SMRTcell folders); using package walk
    for (dirpath, dirnames, filenames) in walk(pacBioProjFold):
        f.extend(dirnames)
        break
     #get list of absolute file paths to metadatfiles (this assumes one metadata file/SMRTcell folder);using glob 
    filenames = glob(join(getcwd(), pacBioProjFold, '*','*metadata.xml')) 
    # for each metadata absolute file path print SMRTcellFolder[counter] and metadata filename
    for fn in filenames:
        with open (fn) as fh:
            xml_string = fh.read()
            root = ElementTree.XML(xml_string.replace('http://pacificbiosciences.com/PAP/Metadata.xsd',''))
            xmldict = XmlDictConfig(root)
            print pacBioProjFold, dirnames[counter], xmldict["Sample"]["Name"]
            counter += 1
    print " "
 



