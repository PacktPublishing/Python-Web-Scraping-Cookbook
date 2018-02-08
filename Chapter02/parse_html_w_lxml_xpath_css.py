from lxml import html

def get_file(file):
    with open(file, 'r') as fr:
        contents = fr.read()
        return contents

def main():
    sample_html = 'sample.html'
    html_string = get_file(sample_html)
    doc = html.fromstring(html_string)

    # Select w/ xpath
    quotes = doc.xpath('//div[@id="all-quotes"]/div[@class="quote"]')

    print 'With Xpath:'
    print '-' * 10
    for quote in quotes:
        # strip() to remove \n
        quote_text = quote.text.strip()
        author = quote.xpath('span[@class="author"]')[0].text
        print 'quote: {quote} by {author}'.format(quote=quote_text, author=author)

    print '\n'
    print 'With Css selector:'
    print '-' * 10
    quotes = doc.cssselect('div.quote')
    for quote in quotes:
        quote_text = quote.text.strip()
        author = quote.cssselect('span')[0].text
        print 'quote: {quote} by {author}'.format(quote=quote_text, author=author)

if __name__ == '__main__':
    main()
