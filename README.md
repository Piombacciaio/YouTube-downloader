# YouTube-downloader

simple script to download youtube videos

After something like 11 months I fixed the script.
There is also a GUI verion now.

## Requirements

- pytube
- moviepy
- pysimplegui

to make sure you are able to use pytube open pytube/ciper.py and find function_patterns.
Update it to the following:

```py
  r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
  r'\([a-z]\s*=\s*([a-zA-Z0-9$]{2,3})(\[\d+\])?\([a-z]\)'
```

then go to line 288 and change it to:
  `nfunc=re.escape(function_match.group(1))),`
  
 Remember that this script is for educational purposes only. The creator will not be responsible for any illegal use.
