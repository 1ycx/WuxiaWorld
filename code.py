import os
import requests as req
from bs4 import BeautifulSoup as bs
from ebooklib import epub

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
print("\r\nNovel URL Set")

# Get & Pass To BS4
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
strpage = req.get(novelURL, headers=headers)
soup = bs(strpage.text, "html5lib")

# Seperating Parts From Soup
aboutNovel = soup.select_one('div.novel-index')
synopsis = soup.select('div.fr-view')[1]
about = soup.new_tag('div')

# Book Title
title = soup.select('.novel-body > h2')[0].get_text()
book.set_title(title)

# Get All Chapter Links
links = []
for a in soup.findAll("li", class_="chapter-item"):
    href = link = a.findNext("a")["href"]
    if "https" not in link:
        href = ww + link
    links.append(href)


# Chapter Links
length = len(links)
start, end = 0, length
print("\r\nTitle - " + str(title))
print("\r\nTotal No. Of Chapters = " + str(length))
print("\r\nPlease Note That No. Of Chapters Shown May Not Match The Actual Numbering")
print("Because Some Chapters Maybe Numbered As 187-A, 187-B, 187-C Although Being")
print("3 Different HTML Pages.")
print("\r\nEnter 1 - To Download All Chapters")
print("\r\nEnter 2 - To Download A Part, Like 0-100 Or 400-650")
check = int(input("\r\nEnter Your Choice : "))
if check == 2:
    print("\r\n**Note : To Download From First Chapter, Enter \"First Chapter\"")
    print("         Value As \"0\", Not \"1\"")
    start = int(input("\r\nEnter First Chapter : "))
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
    print("#### Sorry, Cover Image Load Failed ####")
    print("########### So, Skipping It ############")
    print("########################################")
    aboutNovel = soup.select_one('div[class="media-body"]')
    book.spine = ['nav']
    spine_loc = 1

else:
    if "https" not in src:
        src = ww + src
    img_name = src.split('/')[-1].split('?')[0]
    r = req.get(src, headers=headers)
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
    if not insert_loc:
        tag.append(element)
    else:
        tag.insert(insert_loc, element)

counter, err = start - 1, []

for i in range(start, end+1):

    try:

        if i == length:
            break

        #####################
        # Sets the adress here
        strpage = req.get(links[i], headers=headers)

        # Modifies the HTML received
        s = bs(strpage.text, "html5lib")
        #chapterTitle = "Chapter : " + str(i)
        chapterTitle = ''
        for idx in range(0, 20):
            chapterTitle = s.select('h4')[idx].get_text()
            if "Chapter" in chapterTitle:
                break
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

        print("Parsed Chapter", i)
        counter += 1

    except KeyboardInterrupt as e:
        print("Keyboard Interrupt")
        print(e)
        break

    except IndexError as e:
        print(e)
        print("Possibly Incorrect Link For Chapter", i)
        print("Skipping Chapter", i)
        err.append(i)

    except Exception as e:
        print(e)
        err.append(i)

if counter < 0: counter = 0

# About Novel
about.append(aboutNovel)
html_gen("hr", '', about)
html_gen("h3", "Chapters", about)
html_gen("p", "Total = " + str(counter), about)
html_gen("p", "No. Of Chapters That Raised Exceptions = " + str(len(err)), about)
if len(err) != 0:
    html_gen("p", "And They Are : ", about)
    for e in err:
        html_gen("li", str(e), about)
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
style = 'p { text-align : left; }'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# Adds CSS File
book.add_item(nav_css)

# Location Where File Will Be Saved
# Default Location Will Be The Place Where This Script Is Located
# To Change,
# 1 - Add The Location Inside The Empty pathToLocation
#   Example 1 - Windows :
#       pathToLocation = 'C:\\Users\\Adam\\Documents\\'
#       Notice The Extra \ To Be Added Along With Every Original - This Is Compulsory For Every \
#   Example 2 - Unix/POSIX Based(OS X, Linux, Free BSD etc) :
#       pathToLocation = '/home/Adam/Documents/'
#       Notice That No Extra / Are Added Along With Original
# OR
# 2 - Move This Script To, And Run From The Location To Be Saved
pathToLocation = ''
downloadDetails = title + '_' + str(start) + '_' + str(counter) + '.epub'
saveLocation = pathToLocation + downloadDetails


print("Saving . . .")

# Saves Your EPUB File
epub.write_epub(saveLocation, book, {})

# Location File Got Saved
if pathToLocation == '':
    print("Saved at", os.getcwd(), 'as', downloadDetails)
    # Example : Saved at /home/Adam/Documents as "The Strongest System_0_3.epub"
else :
    print("Saved at", saveLocation)
