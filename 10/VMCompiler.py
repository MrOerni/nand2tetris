import re
import xml.etree.ElementTree as ET
#from lxml import etree as ET
import xml.dom.minidom as minidom

from sys import argv
from sys import exit
from os import listdir
from os.path import join

keyword = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"}
symbol = {"{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"}
keyword2 = "(class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return)"
symbol2 = r"{|}|\(|\)|\[|\]|\.|,|;|\+|-|\*|/|&|\||<|>|=|~"
integerConstant = re.compile(r"[0-32767]")
StringConstant = re.compile(r"\".*?\"")
identifier = re.compile(r"[a-zA-Z_]\w*", flags=re.ASCII)
multilineComment = re.compile(r"/\*\*?.*?\*/", flags=re.DOTALL)
allElements = r"[0-32767]|\".*?\"|[a-zA-Z_]\w*|class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return|{|}|\(|\)|\[|\]|\.|,|;|\+|-|\*|/|&|\||<|>|=|~"


def main():
    inputPath = argv[1]

    for file in listdir(inputPath):
        if(file.endswith(".jack")):
            tokenize(join(inputPath, file))


def tokenize(fileName):
    root = ET.Element("tokens")

    with open(fileName, "r") as f:
        fileName = fileName.replace(".jack", "T.out.xml")
        code = "".join(map (lambda line: re.sub(r"//.*","", line), f.readlines())) #clear comments

    code = re.sub(r"\s+", " ", code) #clear tabs/newlines
    code = re.sub(multilineComment, "", code)

    elements = re.findall(allElements, code)

    for element in elements:
        if re.match(integerConstant, element):
            item = "integerConstant"
        elif re.match(StringConstant, element):
            item = "StringConstant"
        elif re.match(keyword2, element):
            item = "keyword"
        elif re.match(symbol2, element):
            item = "symbol"
        elif re.match(identifier, element):
            item = "identifier"
        else:
            print("Error:" + item)
            exit(-1)
        ET.SubElement(root, item).text = element

    with open(fileName, "w") as file:
        file.write(prettify(root))


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem)
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

if __name__ == "__main__":
	main()