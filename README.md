EPAM Python Training 2021.09 Final Task - Python RSS-reader


RSS-reader is a pure Python command-line utility on python 3.9 version. 
It receives RSS URL and prints results in human-readable format.
An example of format of the news console output:

```shell
$ python rss_reader.py https://www.onliner.by/feed

################################### https://www.onliner.by/feed ####################################

        Feed: Onliner. 

     Topic 1|  Подбежал, сделал замах, отбежал. В Гомеле подрались таксист и пешеход-«боксер»
        Date| Sat, 30 Oct 2021 18:14:44 +0300
        Link| https://auto.onliner.by/2021/10/30/v-gomele-podralis-taksist-i-peshexod-bokser
 Description: Не смогли мирно разойтись по своим сторонам водитель такси и… нет, не пассажир, а пешеход. Конфликт двух мужчин произошел в четверг, 28 октября. Видео рукопашного боя появилось в группе «ЧП. Гомель». И вам стоит посмотреть этот ролик. Читать далее…
       Links:
             1 https://content.onliner.by/news/thumbnail/6982f44cd2b92a3184e95121ae0371d3.jpeg
             2 https://vk.com/gomelchp?w=wall-131126363_267004
```

Utility provides the following interface:
```shell
usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [--to-html] [--to-pdf] [source]

Pure Python command-line RSS reader

positional arguments:
  source         Input RSS URL. Must starts with http[s]://

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
  --date DATE    Retrieves news for the date, format: 'YYYYMMDD'
  --to-html      Save result in HTML file
  --to-pdf       Save result in PDF file

```

The utility with the --json argument prints news to standard output in the following format:
```shell
$ python rss_reader.py https://www.onliner.by/feed --json --limit 1
{
    "https://www.onliner.by/feed": {
        "source_news": [
            {
                "title": " Подбежал, сделал замах, отбежал. В Гомеле подрались таксист и пешеход-«боксер»",
                "pubdate": "Sat, 30 Oct 2021 18:14:44 +0300",
                "description": "Не смогли мирно разойтись по своим сторонам водитель такси и… нет, не пассажир, а пешеход. Конфликт двух мужчин произошел в четверг, 28 октября. Видео рукопашного боя появилось в группе «ЧП. Гомель». И вам стоит посмотреть этот ролик. Читать далее…",
                "links": [
                    "https://auto.onliner.by/2021/10/30/v-gomele-podralis-taksist-i-peshexod-bokser",
                    "https://content.onliner.by/news/thumbnail/6982f44cd2b92a3184e95121ae0371d3.jpeg",
                    "https://vk.com/gomelchp?w=wall-131126363_267004"
                ]
            }
        ],
        "source_info": "Onliner. "
    }
}
```

With the --to-pdf and --to-html arguments, the results are saved in the news.pdf and news.html files, respectively



Installing:
1. clone current repository.
2. from directory with setup.py file star commant:
   ```shell
   pip  install .
   ```
   or from any directory:
   ```shell
   pip install [path/to/cloned/deirectory]
   ```

Run utility:
```shell
python rss_reader.py
```

or

run from any directory:
```shell
rss_reader
```
