import xml.etree.ElementTree as ET


def main():
    file_name = 'sample.xml'
    tree = ET.parse(file_name)

    # you can also read data from a string:
    # with open(file_name, 'r') as fr:
    #    file_as_string = fr.read()
    #    tree = ET.fromstring(file_as_string)

    # the root node (which is catalog in this case) has a tag and a dictionary of attributes
    root = tree.getroot()

    # access root node
    # this returns the entire catalog node, which is the entire xml content
    print(root.tag)

    # return root node attributes (which is empty in this case)
    print(root.attrib)

    # this returns the 1st book
    # root[0] -> 1st book node
    # root[0][0] -> 1st element from the 1st book node
    print(root[0][0].text)

    # how about findind the price node in the 1st book node?
    # and assume we don't know what its index is
    print(root[0].find('price').text)

    # note: find('child_node_name') may raise an AttributeError
    # exception if the node doesn't exist
    # print(root[0].find('nosuchnode').text)

    # You should make sure the node exists like:
    node = root[0].find('nosuchnode')
    if node:
        print(node.text)

    # Let's do something more interesting, print each book's author, price and isbn number
    book_nodes = root.findall('book')

    for book_node in book_nodes:
        # use find() or child_node[idx] to access childe node
        # .text will return node text value
        # .attrib returns all attributes as a dict,
        # attrib['attribute_name'] returns a specific attribute value
        # you can also use attrib.get('attribute_name') in case attribute isn't always available
        print('Author: {author}, Price: {price} ISBN: {isbn}').format(author=book_node.find('author').text,
                                                                      price=book_node.find('price').text,
                                                                      isbn=book_node.attrib['isbn'])

    # what about the most expensive book?
    max_book_price = max(map(lambda book: book.find('price').text, book_nodes))
    print('most expensive book {max_price}'.format(max_price=max_book_price))


if __name__ == '__main__':
    main()
