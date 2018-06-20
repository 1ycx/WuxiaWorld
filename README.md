<img src="https://img.shields.io/badge/Version-3.0-brightgreen.svg" ></img>
# About: 
<h4>Python Script To Copy WW Chapters Into EPUB File.</h4>

Copies The Novel Chapters Along With Novel Details And Sometimes 'Not' The Cover Image (IDK Why ? Maybe Because Of BeautifulSoup4 Internal Problem).

Just Enter The Novel URL And You're Good To Go!

<h4>I'll Try To Add Any Necessary Updates.</h4>


<h4> Initial Author :  <a href="https://forum.wuxiaworld.com/profile/Aundinn">Aundinn</a> </h4>

<br/>

## Task(s) :
- [x] Get List Of Chapters From Novel Website And Use Links From The List Rather Than Progress Sequentially Because Of The Arising Problem Of Some Pages Not Having Sequential Names.


## Problem(s) :

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
* If Specific No. Of Chapters Are To Be Downloaded, Then Enter 2 And Provide The `start` And `end` Chapters.
* All Chapters Of Corresponding Novel Will Be Downloaded And Saved At `novel-name_start-chapter_end-chapter.epub`

### Parsing :
`html5lib` Is Used Because Although Being Tiny Winy Bit Slow, It Generates Valid HTML. You May Compare Others Here, [**BeautifulSoup - Different Parsers**](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser)


## License

Copyright &copy; 2018 [Kogam22](https://github.com/Kogam22). Released under the terms of the [MIT license](LICENSE.md).
