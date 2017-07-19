from modules.webcrawler import WebCrawler

crawler = WebCrawler()

keywords = ['global', 'warming']
links = crawler.crawl('http://www.bing.com/search?q=global+warming&go=Submit&qs=bs&form=QBLH', keywords)
#print links
paragraphs = crawler.grabContent(links[3])

paragraphs = WebCrawler.normalizeParagraphs(paragraphs)
paragraphs = WebCrawler.replace_nonalpha(paragraphs)

print paragraphs