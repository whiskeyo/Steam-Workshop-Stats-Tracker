# Steam Workshop Stats Tracker

## App description

Simple webscraper written in Python using `BeautifulSoup` and `requests` modules. It fetches data from given *url* every 60 seconds and looks for a table with the number
of unique visitors (new, logged in Steam users visit *url*), current subscribers and
current favorites. Then it prints data in a form presented below:

```
-------------------------------------Last data fetch--------
Jumps Training Statistics            06/04/2021 09:35:13
------------------------------------------------------------
Unique Visitors      1434295              (+0)
Current Subscribers  2019607              (+1)
Current Favorites    18337                (+0)
------------------------------------------------------------
Gains since starting scraping ( 05/04/2021 18:42:07 )
New visitors:     194
New subscribers:  367
New favorites:    5
---------- GRAPH OF LAST 60 MINUTES OF ACTIVITY ------------










                       v
                       v                    v
     v  v          v   s                    s
    vs  sv         v   s     vv  v   v    v s  v v
    ss sssss      ss v s  s sss  s   ss   s ss s s    s  v s
------------------------------------------------------------
oldest                                                newest
event                                                  event
```

First section shows current values with changes from last fetch. Second section shows cumulative values since the process got started. Last section is a timeline: `s` stands for new subscriber, `v` for new visitor and `f` for new favorite. Every column (one `-` on the line) shows changes from one data fetch. 

## TODO (order does not imply importance)

1. Improve outputting data to file
2. Support drawing plots with various options (e.g. comparing days)
3. Add possibility of tracking any Steam Workshop item
4. Add command line arguments support or menu with possibility of setting things up 
