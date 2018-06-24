import os
import cfscrape
import requests
from bs4 import BeautifulSoup as bs
from ebooklib import epub

# Create Scraper Object
scraper = cfscrape.create_scraper()

# Create The EPUB File
book = epub.EpubBook()
book.set_language('en')

# WW Link - Don't Change
ww = 'https://www.wuxiaworld.com'

# Enter The Novel URL Here
novelURL =  'https://www.wuxiaworld.com/novel/ancient-strengthening-technique/'
while novelURL == '':
    print("Novel URL Not Provided Inside The Script.")
    novelURL = str(input("Please Enter Novel URL : "))
print("Novel URL Set")

# Scraper + Passing To Beautiful Soup
strpage = scraper.get(novelURL).content 
soup = bs(strpage, "html5lib")

# Seperating Parts From Soup
aboutNovel = soup.select_one('div[class="media media-novel-index"]')
synopsis = soup.select('div[class="fr-view"]')[1]
about = soup.new_tag('div')

# Book Title
title = soup.select('h4')[0].get_text()
book.set_title(title)

# Get All Chapter Links
links = []
for a in soup.findAll("li", class_="chapter-item"):
    href = a.findNext("a")["href"]
    link = href
    if "https" not in link:
        href = ww + link
    links.append(href)


# Chapter Links
length = len(links)
start = 0
end = length
print("Total No. Of Chapters = " + str(length))
print("Please Note That No. Of Chapters Shown May Not Match The Actual Numbering")
print("Because Some Chapters Maybe Numbered As 187-A, 187-B, 187-C Although Being")
print("3 Different HTML Pages.")
print("Enter 1 - To Download All Chapters")
print("Enter 2 - To Download A Part, Like 0-100 Or 400-650")
check = int(input("Enter Your Choice : "))
if check == 2:
    print("Please Note That To Download From First Chapter, Enter \"First Chapter\"") 
    print("Value As \"0\", Not \"1\"")
    start = int(input("Enter First Chapter : "))
    end   = int(input("Enter Last Chapter  : "))
elif check == 1:
    print("Okay, All Available Chpaters Will Be Downloaded.")
else :
    print("Invalid Choice. All Available Chapters Will Be Downloaded.")

# Cover Image
# Please Note That Cover Doesn't Get Downloaded Sometimes Due To Soup Element Not Getting Data In Time Or Some Other Reason With Soup
# If Image Is Not Downloaded Then It Won't Be Added, No Problemo
try:
    src = aboutNovel.img['src']

except Exception:
    print("########################################")
    print("####### Image Exception Called #########")
    print("## Sorry, Cover Image Download Failed ##")
    print("########### So, Skipping It ############")
    print("########################################")
    aboutNovel = soup.select_one('div[class="media-body"]')
    book.spine = ['nav']
    spine_loc = 1

else:
    if "https" not in src:
        src = ww + src
    img_name = src.split('/')[-1].split('?')[0]
    r = requests.get(src)
    with open(img_name, 'wb') as f:  
        f.write(r.content)
    print("Image File : "+img_name)
    image = open(img_name, 'rb').read()
    book.set_cover(file_name=img_name, content=image, create_page=True)
    book.spine = ['cover', 'nav']
    for img in aboutNovel.select('img'):
        img.decompose()
    spine_loc = 2

def html_gen(elem, val, tag, insert_loc=None):
    element = soup.new_tag(elem)
    element.string = val
    if insert_loc == None:
        tag.append(element)
    else:
        tag.insert(insert_loc, element)

counter = 0
err = []

for i in range(start, end+1):
    
    try:
    
     if i == length:
        break

     #####################
     # Sets the adress here 
     strpage = scraper.get(links[i]).content 

     # Modifies the HTML received
     s = bs(strpage, "html5lib")    
     #chapterTitle = "Chapter : " + str(i)
     chapterTitle = s.select('h4')[1].get_text()
     div = s.select_one('div[class="fr-view"]')
     test_p0 = div.select('p')[0].get_text()
     test_p1 = div.select('p')[1].get_text()

     if "Chapter" not in test_p0 and "Chapter" not in test_p1:
      html_gen("h4", chapterTitle, div, 1)

     for a in div.select("a"):
      a.decompose()

     # Creates a chapter
     c2 = epub.EpubHtml(title=chapterTitle, file_name='chap_'+str(i)+'.xhtml', lang='hr')
     c2.content = div.encode("utf-8")
     book.add_item(c2)


     # Add to table of contents
     book.toc.append(c2)    

     # Add to book ordering
     book.spine.append(c2)

     print("Parsed Chapter " + str(i))
     counter = counter + 1

    except KeyboardInterrupt as e:
     print("Keyboard Interrupt")
     print(e)
     break
    
    except IndexError as e:
     print(e)
     print("Possibly Incorrect Link For Chapter " + str(i))
     print("Skipping Chapter " + str(i))
     err.append(i)
    
    except Exception as e:
     print(e)
     err.append(i)

# About Novel
html_gen("h3", "About Novel : ", about)
about.append(aboutNovel)
html_gen("hr", '', about)
html_gen("h3", "Chapters", about)
html_gen("p", "Total = " + str(counter), about)
html_gen("p", "No. Of Chapters That Raised Exceptions = " + str(len(err)), about)
if len(err) != 0:
    html_gen("p", "And They Are : ", about)
    for i in err:
        html_gen("li", i, about)
html_gen("hr", '', about)
synopsis.findNext('p').decompose()
html_gen("h3", "Synopsis :", about)
about.append(synopsis)

# Create About Novel Page
aboutNovelTitle = "About Novel"
c1 = epub.EpubHtml(title=aboutNovelTitle, file_name='About_novel'+'.xhtml', lang='hr')
c1.content = about.encode('utf-8')
book.add_item(c1)
book.toc.insert(0, c1)
book.spine.insert(spine_loc, c1)
print("Created \"About Novel\" Page")

# Add Navigation Files
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# Defines CSS Style
style = 'p {text-align: left;}'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# Adds CSS File
book.add_item(nav_css)

# Location Where File Will Be Saved
# Default Location Will Be The Place Where This Script Is Located
# To Change, 
# 1 - Add The Location Inside The Empty pathToLocation
#   Example 1.1 - Windows : 
#       pathToLocation = 'C:\\Users\\Adam\\Documents\\'
#       Notice The Extra \ To Be Added Along With Every Original - This Is Compulsory For Every \
#   Example 1.2 - Linux : 
#       pathToLocation = '/home/Adam/Documents/'   
#       Notice That No Extra / Are Added Along With Original  
# OR 
# 2 - Move This Script And To, And Run From The Location To Be Saved
pathToLocation = ''
saveLocation = pathToLocation + title + '_' + str(start) + '_' + str(i) + '.epub'

print("Saving . . .")

# Saves Your EPUB File
epub.write_epub(saveLocation, book, {})

# Location File Got Saved
if pathToLocation == '':
 print("Saved at " + str(os.getcwd()) + ' as "' + title + '_' + str(start) + '_' + str(i) + '.epub"')
else :
 print("Saved at " + saveLocation)

