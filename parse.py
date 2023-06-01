import re

def parse(xml):
    xml = xml.strip()

    # strip comments
    xml = re.sub(r"<!--[\s\S]*?-->", '', xml)

    def document():
        return {
            'declaration': declaration(),
            'root': tag()
        }

    def declaration():
        m = match(r"^<\?xml\s*")
        if not m:
            return None

        node = {
            'attributes': {}
        }

        while not (eos() or _is('?>')):
            attr = attribute()
            if not attr:
                return node
            node['attributes'][attr['name']] = attr['value']

        match(r"\?>\s*")

        return node

    def tag():
        m = match(r"^<([\w-:.]+)\s*")
        if not m:
            return None

        node = {
            'name': m[1],
            'attributes': {},
            'children': []
        }

        while not (eos() or _is('>') or _is('?>') or _is('/>')):
            attr = attribute()
            if not attr:
                return node
            node['attributes'][attr['name']] = attr['value']

        if match(r"^\s*/>\s*"):
            return node

        match(r"\??>\s*")

        node['content'] = content()

        while True:
            child = tag()
            if not child:
                break
            node['children'].append(child)

        match(r"^</[\w-:.]+>\s*")

        return node

    def content():
        m = match(r"^([^<]*)")
        if m:
            return m[1]
        return ''

    def attribute():
        m = match(r"([\w:-]+)\s*=\s*('[^']*'|\"[^\"]*\"|\w+)\s*")
        if not m:
            return None
        return {
            'name': m[1],
            'value': strip(m[2])
        }

    def strip(val):
        return re.sub(r"^['\"]|['\"]$", '', val)

    def match(pattern):
        nonlocal xml
        m = re.match(pattern, xml)
        if not m:
            return None
        xml = xml[m.end():]
        return m.groups()

    def eos():
        return len(xml) == 0

    def _is(prefix):
        return xml.startswith(prefix)
    
    return document()



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
	<CD>
		<TITLE>Greatest Hits</TITLE>
		<ARTIST>Dolly Parton</ARTIST>
		<COUNTRY>USA</COUNTRY>
		<COMPANY>RCA</COMPANY>
		<PRICE>9.90</PRICE>
		<YEAR>1982</YEAR>
	</CD>
	<CD>
		<TITLE>Still got the blues</TITLE>
		<ARTIST>Gary Moore</ARTIST>
		<COUNTRY>UK</COUNTRY>
		<COMPANY>Virgin records</COMPANY>
		<PRICE>10.20</PRICE>
		<YEAR>1990</YEAR>
	</CD>
	<CD>
		<TITLE>Eros</TITLE>
		<ARTIST>Eros Ramazzotti</ARTIST>
		<COUNTRY>EU</COUNTRY>
		<COMPANY>BMG</COMPANY>
		<PRICE>9.90</PRICE>
		<YEAR>1997</YEAR>
	</CD>
	<CD>
		<TITLE>One night only</TITLE>
		<ARTIST>Bee Gees</ARTIST>
		<COUNTRY>UK</COUNTRY>
		<COMPANY>Polydor</COMPANY>
		<PRICE>10.90</PRICE>
		<YEAR>1998</YEAR>
	</CD>
	<CD>
		<TITLE>Sylvias Mother</TITLE>
		<ARTIST>Dr.Hook</ARTIST>
		<COUNTRY>UK</COUNTRY>
		<COMPANY>CBS</COMPANY>
		<PRICE>8.10</PRICE>
		<YEAR>1973</YEAR>
	</CD>
	<CD>
		<TITLE>Maggie May</TITLE>
		<ARTIST>Rod Stewart</ARTIST>
		<COUNTRY>UK</COUNTRY>
		<COMPANY>Pickwick</COMPANY>
		<PRICE>8.50</PRICE>
		<YEAR>1990</YEAR>
	</CD>
	<CD>
		<TITLE>Romanza</TITLE>
		<ARTIST>Andrea Bocelli</ARTIST>
		<COUNTRY>EU</COUNTRY>
		<COMPANY>Polydor</COMPANY>
		<PRICE>10.80</PRICE>
		<YEAR>1996</YEAR>
	</CD>
	<CD>
		<TITLE>When a man loves a woman</TITLE>
		<ARTIST>Percy Sledge</ARTIST>
		<COUNTRY>USA</COUNTRY>
		<COMPANY>Atlantic</COMPANY>
		<PRICE>8.70</PRICE>
		<YEAR>1987</YEAR>
	</CD>
</CATALOG>
'''

print(parse(content))
