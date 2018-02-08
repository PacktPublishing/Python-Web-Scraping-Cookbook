from bs4 import BeautifulSoup


def read_xml(xml_file):
    with open(xml_file, 'r') as fr:
        contents = fr.read()
        return contents


def main():
    file_name = 'sample.xml'
    contents = read_xml(file_name)
    bs4 = BeautifulSoup(contents, features="xml")

    # access root node
    # this returns the entire catalog node, which is the entire xml content
    #print(bs4.catalog)

    # this returns the 1st book, even if there are two books available
    #print(bs4.catalog.book)

    # alternatively, we can access the 1st book node with
    # print(bs4.findAll('book')[0])
    # and of course you can access the 2nd element with
    # print(bs4.findAll('book')[2])
    # IndexError will be raised if you try to access an non-existent node

    # Let's do something more interesting, print each book's author, price and isbn number
    book_nodes = bs4.findAll('book')
    for book_node in book_nodes:
        # use '.' to access childe node, it will return the matching xml
        # we can use .text to return the value for the node
        # bracket to access attribute '[attribute_name]'
        print('Author: {author}, Price: {price} ISBN: {isbn}').format(author=book_node.author.text,
                                                                      price=book_node.price.text,
                                                                      isbn=book_node['isbn'])

    # what about the most expensive book?
    max_book_price = max(map(lambda book: book.price.text, book_nodes))
    print('most expensive book {max_price}'.format(max_price=max_book_price))


if __name__ == '__main__':
    main()
