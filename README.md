<img src="https://img.shields.io/badge/Version-3.0-brightgreen.svg" ></img>
# About: 
<h4>Python Script To Copy WW Chapters Into EPUB File. I'll Try To Add Any Necessary Updates.</h4>


<h4> Initial Author :  <a href="https://forum.wuxiaworld.com/profile/Aundinn">Aundinn</a> </h4>

<br/>

## Task(s) :
- [x] Make The Code Get List Of Chapters And Use Links From The List Rather Than Progress Sequentially Because Of The Arising Problem <s>( Update Coming Soon )</s>


## Problem(s) :
<s>1. If Some Chapter Does Not Have A Sequential Number, Then It Won't Be Added. You'll Get To Know Which, Inside The Terminal.</s>
   <s>* Example : AWE Chapters 472,473,474 Have Different URLs Which Aren't Sequential Like The Rest From 1-630.</s>
### None Yet
   
<br/>

## Documentation :
1. For Beginners, After Setting Up A Working Python 3 Environment, You Need To Install Some Packages. To Install, Run These Commands In Your CMD/Terminal :
   * `pip3 install bs4`
   * `pip3 install ebooklib`
   * `pip3 install cfscrape`
   * `pip3 install html5lib=="0.9999999"` 

2. Download The Python Script And Unzip It.

3. Open The Script With A Text Editor And Read The Details Inside.

4. In Case The Script Was Not Updated According To The Changes In Website, You Might Refer The [**BeautifulSoup Docs**](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) To Make Changes Accordingly.

4. To Run, Open CMD/Terminal, Navigate To The Unzip Location And Type :
  `python3 code.py`

5. EPUB File Will Be Saved At The Location Of Script.

### Working :
* Set Novel Link in `novelURL`
* If Specific Chapters Are To Be Downloaded Then, Select 2 And Enter The `start` And `end` Chapters.

### Parsing :
`html5lib` Is Used Because Although Being Tiny Winy Bit Slow, It Generates Valid HTML. You May Compare Others Here, [**BeautifulSoup - Different Parsers**](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser)

