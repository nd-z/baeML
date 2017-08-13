from modules.webcrawler import WebCrawler

crawler = WebCrawler()

keywords = ['government']
links = crawler.crawl('http://www.bing.com/news/search?q=government+&go=Submit&qs=bs&form=QBLH', keywords)
print links
paragraphs = crawler.grabContent(links[3])

paragraphs = WebCrawler.normalizeParagraphs(paragraphs)
paragraphs = WebCrawler.replace_nonalpha(paragraphs)

print paragraphs