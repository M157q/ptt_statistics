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
usage: ptt-statistics [-h] {board,path} ...  
  
optional arguments:  
  -h, --help    show this help message and exit  
  
subcommands:  
  {board,path}  use ${sub-command} -h for further usage  
    board       Craw the specific board  
    path        Get specific article info with path  
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
開頭且為必須要後一個，找到後再從這 tag 之後開始計算推文  
  
此解法必須修改 <https://github.com/M157q/ptt-crawler> 才行。  
  
  
### 從別版轉錄過來的文章中，別版的推文會被計算  
  
解決方法同上，但問題在於有些轉錄者為了美觀，會把此 tag 刪除，這樣就無解。  
  
  
### 使用者編輯文章的時候修改到推文日期時間  
  
此狀況無解，只會紀錄該推文的使用者及內容，日期及時間無法準確紀錄。  
  
---  
  
## Reference  
  
+ <https://www.ptt.cc/bbs/sex/M.1447949531.A.610.html>  
  
---  
  
## LICENSE  
  
GPLv3  
