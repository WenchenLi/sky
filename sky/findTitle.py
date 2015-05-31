try:
    from .training import Training
    from .helper import *
except SystemError:
    from training import Training    
    from helper import *

def metaPrinter(tr):
    for meta in tr.xpath('//meta'):
        print(lxml.html.tostring(meta))

def getNthInTree(tr, ele): 
    it = 0
    for x in tr.iter(): 
        it += 1
        if x == ele: 
            break
    else:
        return None
    return it

def getDepth(ele):
    return len(list(ele.iterancestors()))

def getTitle2(tree, returnBest = True):
    xpaths = ['//title', '//*[contains(@property, "title")]', '//*[contains(@name, "title")]', '//*[contains(@id, "title")]', '//*[@*="title"]', '//*[contains(@class, "title")]', '//*[@title]', '//h1', '//h2', '//h3', '//h4']
    titles = []
    for xp in xpaths:
        xres = tree.xpath(xp)
        if xres and len(xres[0].text_content().strip()) > 2:
            title = {}
            title['nthInTree'] = getNthInTree(tree, xres[0])
            title['depth'] = getDepth(xres[0])
            title['numElementsInXpath'] = len(xres)
            title['text'] = xres[0].text_content().strip()
            title['textLength'] = len(title['text'])
            title['isSub'] = False
            title['isSuper'] = False
            title['wordSet'] = set(x for x in title['text'].split() if len(x) > 1)
            title['wordSetLength'] = len(title['wordSet'])
            title['xpath'] = xp
            titles.append(title)
    scores = []
    for title in titles:
        scores.append(title['nthInTree'] * title['depth'] * title['numElementsInXpath']) 

    if not returnBest:
        return titles, scores
    
    for t, s in zip(titles, scores):
        if s == min(scores):
            for title, score in zip(titles, scores):
                
                if t != title:
                    if len(t['wordSet'] & title['wordSet']) / len(t['wordSet']) > 0.3 and t['wordSetLength'] > title['wordSetLength']:
                        break
            else:
                title, score = t, s
            return title, score        

def getTitle(tree, returnBest = True):
    xpaths = ['//title', '//*[contains(@property, "title")]', '//*[contains(@name, "title")]', '//*[contains(@id, "title")]', '//*[@*="title"]', '//*[contains(@class, "title")]', '//*[@title]', '//h1', '//h2', '//h3', '//h4']
    titles = []
    for xp in xpaths:
        xres = tree.xpath(xp)
        if xres and len(xres[0].text_content().strip()) > 2:
            title = {}
            title['text'] = xres[0].text_content().strip()
            title['wordSet'] = set(x for x in title['text'].split() if len(x) > 1)
            title['wordSetLength'] = len(title['wordSet'])
            title['xpath'] = xp
            titles.append(title)

    if not returnBest:
        return titles

    t = titles[0]
    for title in titles[1:]:
        if len(t['wordSet'] & title['wordSet']) / len(t['wordSet']) > 0.3 and t['wordSetLength'] > title['wordSetLength']: 
            break
    else:
        title = t
    return title['text']


# tr = Training("nieuwsdumper-testcase1", "/Users/pascal/GDrive/virtual-python/sky/sky/tests/").load()
# tr2 = Training("marktplaats-testcase1", "/Users/pascal/GDrive/virtual-python/sky/sky/tests/").load()
# tr3 = Training("betterdoctor-doctor-referalls", "/Users/pascal/GDrive/virtual-python/sky/sky/tests/").load()

    
# train = [tr, tr2, tr3]            
# for t in train:
#     for tree in t.trees:
#         print(getTitle(tree))
            





            
