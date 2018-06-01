import os
import cfscrape
import re
from bs4 import BeautifulSoup
from ebooklib import epub

# Get The Text At The Set URL
scraper = cfscrape.create_scraper()

# Create The EPUB File
book = epub.EpubBook()

#####################
# CONFIGURATIONS
#####################
title = 'Perfect_World' # The title you want to give to the book
beginning = 1 # First chapter
end = 585 # Last chapter

# Enter Address Of Novel Without Chapter Number
urlPrefix = "https://www.wuxiaworld.com/novel/perfect-world/pw-chapter-"

#####################
tableOfContents = ()

book.set_title(title)
book.set_language('en')

for i in range(beginning, end+1):
    
    try:

     #####################
     # Sets the adress here 
     strpage = scraper.get(urlPrefix+str(i)+'/').content 


     # Modifies the HTML received
     soup = BeautifulSoup(strpage, "html5lib")    
     #chapterTitle = "Chapter : " + str(i)
     chapterTitle = soup.select('h4')[1].get_text()
     div = soup.select_one('div[class="fr-view"]')
     
     for a in div.select("a"):
      a.decompose()

     # Creates a chapter
     c1 = epub.EpubHtml(title=chapterTitle, file_name='chap_'+str(i)+'.xhtml', lang='hr')
     c1.content = div.encode('ascii')
     book.add_item(c1)


     # Add to table of contents
     book.toc.append(c1)    

     # Add to book ordering
     if i == beginning:
         book.spine = ['nav', c1]
     else:
         book.spine.append(c1)


     print("Parsed Chapter " + str(i))

    except KeyboardInterrupt as e:
     print("Keyboard Interrupt")
     print(e)
     break
    
    except IndexError as e:
     print(e)
     print("Possibly Incorrect Link For Chapter " + str(i))
     print("Skipping Chapter " + str(i))
    
    except Exception as e:
     print(e)

    

book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# Defines CSS Style
style = 'p {text-align: left;}'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# Adds CSS File
book.add_item(nav_css)

print("Saving . . .")

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
saveLocation = pathToLocation + title + '.epub'

# Saves Your EPUB File
epub.write_epub(saveLocation, book, {})

# Location File Got Saved
if pathToLocation == '':
 print("Saved at " + str(os.getcwd()) + ' as "' + title + '.epub"')
else :
 print("Saved at " + saveLocation)
