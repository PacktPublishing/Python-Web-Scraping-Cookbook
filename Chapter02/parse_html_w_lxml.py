from lxml import html

def get_file(file):
    with open(file, 'r') as fr:
        contents = fr.read()
        return contents

def main():
    sample_html = 'sample.html'
    html_string = get_file(sample_html)
    doc = html.fromstring(html_string)

    # Select the 'all-quotes' elements
    # note this will match any tag with id 'all-quotes',
    # e.g: <h1 id="all-quots">..</h1>, and <div id="all-quotes">..</div>
    # only one element (<div id="all-quotes">..</div>) will return this case,
    # but it will return all matched elements if possible
    all_quotes_div = doc.get_element_by_id('all-quotes')

    # html Element
    print doc

    # div Element
    print all_quotes_div

    # next we will pull all the <dic class="quotes">...</div> elements,
    # doc is the 'html' element, or the root element
    # all_quotes_div is the 'div' element, a child element of 'doc' node
    # because all qoute elements are nested inside all_quotes_div, selecting 'quote' elements from doc or all_quotes_div have no difference
    # quote_elements = doc.find_class('quote')
    #
    quote_elements = all_quotes_div.find_class('quote')

    for quote_element in quote_elements:
        print quote_element.text_content()

    # Select w/ xpath
    #quotes = doc.xpath('//div')

    #for quote in quotes:
        #print quote.text

    #quotes = doc.cssselect('div.quote')

    #for quote in quotes:
        #quote_text = quote.text
        #author = quote.cssselect('span')[0].text.strip()
        #print 'quote: {quote} by {author}'.format(quote=quote_text, author=author)

if __name__ == '__main__':
    main()
