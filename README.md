# Intro

i write some market automation helper scripts in different types

the first tool that i have developed is seo-checker that checks 
- meta links
- alt images
- keywords
- etc etc
to gather best seo techniques of top sites 
then we can use them in our website

based on demand we develop different tools for lightweghit business and ideas

# how to use?

## install requirements
> pip install -r requirements

## using the script
> python main.py --help # to see the help


## how to use seo checker?

> python main.py --seo-check --kw-path ./kw.txt

what should exists in kw.txt
```
MY KEYWORDS THAT I WANNA CHECK
```

then you can check google-image results and first rank sites keywords and links
these results will be in two files:
- in-site => the meta-links and alts and h1s and etc etc in 'in-site.txt'
- google-image.txt => the top navbar on google images part that helps you search related info 

