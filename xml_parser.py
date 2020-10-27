import xml.etree.ElementTree as ET


class XmlParser:
    def __init__(self, xml_file):
        self.tags = list()
        self.__parse_xml(xml_file)

    def __parse_xml(self, xml_file):
        root = ET.parse(xml_file).getroot()
        for element in root.findall('seller'):
            product = element.find('product')

            self.tags.append({
                'seller_name': element.find('seller_name').text,
                'product_name': product.find('name').text,
                'link': product.find('link').text,
                'div': product.find('div_name').text,
                'status': product.find('status').text,
                'tag': product.find('tag').text,
                'in_stock': product.find('in_stock').text,
                'out_stock': product.find('out_stock').text
            })
