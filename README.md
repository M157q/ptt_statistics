# ptt_statistics  
  
Get the statistics of a board on PTT by crawling <https://www.ptt.cc/bbs/>.  
Not a telnet crawler.  
  
---  
  
## Installation  
  
`$ pip3 install git+https://github.com/M157q/ptt-crawler`  
`$ pip3 install git+https://github.com/M157q/ptt_statistics`  
  
---  
  
## Usage  
  
```  
usage: ptt-statistics [-h] {crawl,get_article,show} ...  
  
optional arguments:  
  -h, --help            show this help message and exit  
  
subcommands:  
  {crawl,get_article,show}  
                        use ${sub-command} -h for further usage  
    crawl               Crawl the specific board  
    get_article         Get specific article info with path  
    show                Show info of the board via data in db  
```  
  
---  
  
## Current Limitation  
  
### 出現在作者發文內容的推文會被算進去  
  
發生在下列幾種情況：  
  
1. 作者把推文貼上到文章中  
    + ex: <https://www.ptt.cc/bbs/sex/M.1437667210.A.324.html>  
2. 作者使用推文當作簽名檔  
  
目前考慮解決方式：  
  
由於網頁版的  
```  
※ 發信站: 批踢踢實業坊(ptt.cc), 來自: xxx.xxx.xxx.xxx  
```  
會使用 `<span class="f2">` tag 包起來，  
所以考慮每篇文章先找此類 tag 中內容為  
```  
※ 發信站: 批踢踢實業坊(ptt.cc)  
```  
開頭且必須為最後一個，找到後再從這 tag 之後開始計算推文  
  
此解法必須修改 <https://github.com/M157q/ptt-crawler> 才行。  
  
  
### 從別版轉錄過來的文章，先前在別版的推文會被計算  
  
解決方法同上，但問題在於有些轉錄者為了美觀，會把此 tag 刪除，這樣就無解。  
  
### 使用者編輯文章的時候修改到推文日期時間  
  
此狀況無解，只會紀錄該推文的使用者及內容，日期及時間無法準確紀錄。  
  
### 推文的年份計算  
  
由於批踢踢並無提供推文的年份，所以目前是用文章的年份推算，  
問題在於跨年的推文、沈寂多年後突然很多人回去朝聖的文這種  
尤其後者很難得知推文的時間，  
所以目前的作法是：  
  
+ 只儲存文章的月份為 12 月且推文的月份是 1 月的推文，並將符合此條件的推文的年份視為文章的年份加一  
    + 這種推文非常容易發生在新舊年份交替之際。  
+ 其餘月份小於文章月份且不符合上述條件的推文則暫不儲存，等到之後有辦法處理的時候再說。  
  
當然以上只針對有提供推文月份的版，  
沒有提供的話則推文年份全部視為和發文年份相同。  
  
---  
  
## Reference  
  
+ <https://www.ptt.cc/bbs/sex/M.1447949531.A.610.html>  
  
---  
  
## LICENSE  
  
GPLv3  
