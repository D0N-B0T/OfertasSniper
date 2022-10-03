
if "__name__" == "__main__":
    print('This is a library, not a script.')
else:
    def textItem_cleaner(text):
        text = text.replace('<div class="price flex-grow"><a href="/products/', '')
        text = text.replace('+', '')
        text = text.split('"')
        text = text[0]
        return(text)

    def textPrice_clean(text):
        text = text.split('"')
        text = text[4]
        text = text.replace('>$ ', '')
        text = text.replace('</a></div>', '')
        text = text.replace('+', '')
        text = text.replace('.', '')
        return(text)