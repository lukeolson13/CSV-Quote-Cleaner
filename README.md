This script will take a CSV file format which contains both within string commas and quotes (ie 'Get me milk, eggs, and Pabst' & 'He yelled "potato!"') as well as formatting commas and quotes (ie '"first item","second item","third item"') and formats the string commas and quotes in such a way that you will not have additional rows and columns upon opening this in Excel, Pandas, etc.

For example:
- Raw CSV Input:
```python
"this is a test","she said "hey" to me","i was like "no way, jose!!@@","","""
"check one two"
"the "real" slim shady","his name is "shady, slim" I think"
"one more for S&G:","let's up
the 
level a bit
eh?"
```
- Input in Excel:
<p align="center">
<img src="/images/before.png" width="70%">
</p>

- Output:
```python
"this is a test","she said ""hey"" to me","i was like ""no way, jose!!@@"","""","""""
"check one two"
"the ""real"" slim shady","his name is ""shady, slim"" I think"
"one more for S&G:","let's up
the 
level a bit
eh?"
```

- Output in Excel:
<p align="center">
<img src="/images/after.png" width="70%">
</p>

Requirements:
1. All cells are quoted to begin with