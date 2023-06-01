import re
import json

class Parser:
    def __init__(self, xml) -> None:
        self.xml = xml

    def parse(self):
        self.xml = self.xml.strip()
        self.xml = re.sub(r'<!--[\s\S]*?-->', '', self.xml)  
        return self.document()      

    def document(self):
        return {
            "declaration": self.declaration(),
            "root": self.tag()
        }


    def declaration(self):
        m = self.match_func(r"^<\?xml\s*")
        if not m:
            return

        # tag
        node = {
            "attributes": {}
        }

        # attributes
        while not (self.eos() or self.is_func('?>')):
            attr = self.attribute_func()
            if not attr:
                return node
            node["attributes"][attr["name"]] = attr["value"]

        self.match_func(r"\?>\s*")

        return node


    def tag(self):
        m = self.match_func(r'^<([\w\-:.]+)\s*')
        if not m:
            return

        # name
        node = {
            "name": m[1],
            "attributes": {},
            "children": []
        }

        # attributes
        while not (self.eos() or self.is_func('>') or self.is_func('?>') or self.is_func('/>')):
            attr = self.attribute_func()
            if not attr:
                return node
            node["attributes"][attr["name"]] = attr["value"]

        # self closing tag
        if self.match_func(r"^\s*\/>\s*"):
            return node

        self.match_func(r"\??>\s*")

        # content
        node["content"] = self.content()

        # children
        child = None
        while child := self.tag():
            node["children"].append(child)

        # closing
        self.match_func(r'^<([\w\-:.]+)\s*')

        return node


    def content(self):
        m = self.match_func(r"^([^<]*)")
        if m:
            return m[1]
        return ''
    
    def attribute_func(self):
        m = self.match_func(r'([\w:-]+)\s*=\s*("[^"]*"|\'[^\']*\'|\w+)\s*')
        if not m:
            return
        return {"name": m.group(1), "value": self.strip_func(m.group(2))}

    def strip_func(self, val):
        return re.sub(r"^['\"]|['\"]$", "", val)

    def match_func(self, pattern):
        m = re.match(pattern, self.xml)
        if not m:
            return
        self.xml = self.xml[m.end():]
        
        return m

    def eos(self):
        return len(self.xml) == 0

    def is_func(self, prefix):
        return self.xml.startswith(prefix)


content = '''
<?xml version="1.0" encoding="UTF-8"?>


<CATALOG>
	<CD>
		<TITLE>Empire Burlesque</TITLE>
		<ARTIST>Bob Dylan</ARTIST>
		<COUNTRY>USA</COUNTRY>
		<COMPANY>Columbia</COMPANY>
		<PRICE>10.90</PRICE>
		<YEAR>1985</YEAR>
	</CD>
	<CD>
		<TITLE>Hide your heart</TITLE>
		<ARTIST>Bonnie Tyler</ARTIST>
		<COUNTRY>UK</COUNTRY>
		<COMPANY>CBS Records</COMPANY>
		<PRICE>9.90</PRICE>
		<YEAR>1988</YEAR>
	</CD>
</CATALOG>
'''

xml_parser = Parser(content)

output = xml_parser.parse()
print(output)

with open("output.json", "w") as file:
    # Write the content to the file
    file.write(json.dumps(output))