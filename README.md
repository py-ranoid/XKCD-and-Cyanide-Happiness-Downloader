# XKCD-and-Cyanide-Happiness-Downloader
##Python script to download XKCD and Cyanide &amp; Happiness comics.

###Requirements
* Python 2.7
* bs4 ((Beautiful Soup library)[https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup])

Options | Help
--------|-----------
-c | **Webcomic** to download : XKCD(xkcd) or Cyanide and Happiness(CnH)
-b | Comic number to **begin** with
-e | Comic number to **end** at
-p | **Path** to store comics in

###Example 
To download all xkcd comics till date
> python -c xkcd

To download all Cyanide and Happiness comics between 1000 and 2000
> python -c CnH -b 1000 -e 2000

To download all Cyanide and Happiness comics from 3000 till date and store in /home/MyComputer/WebComics.
> python -c CnH -b 3000 -p /home/MyComputer/WebComics
  
