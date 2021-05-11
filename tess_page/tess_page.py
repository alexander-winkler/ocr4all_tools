#!/usr/bin/env python
# coding: utf-8

# In[84]:


from lxml import etree
try:
    from PIL import Image,ImageDraw
except ImportError:
    import Image
import pytesseract
from glob import glob
import re
from pathlib import Path


# In[85]:


NSMAP = {'page': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15'}


# In[86]:


## Code snippet adapted from
#https://stackoverflow.com/questions/22588074/polygon-crop-clip-using-python-pil


def mask(coords, img=img):
    xy = [tuple(map(int, tuples.split(','))) for tuples in coords.split(" ")]
    x_coordinates = [c[0] for c in xy]
    y_coordinates = [c[1] for c in xy]
    a,b,c,d = [min(x_coordinates), min(y_coordinates), max(x_coordinates), max(y_coordinates)]
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.polygon(xy, fill=255, outline=None)
    black =  Image.new("L", img.size, 255)
    result = Image.composite(img, black, mask)
    result = result.crop((a,b,c,d))
    return result


# In[89]:


def tess_pagexml(project_dir):
    xml_files = (Path(project_dir) / "processing").glob("*.xml")
    for XML in xml_files:
        print(f"Start working on {str(XML)} now.")

        tree = etree.parse(str(XML))
        img_info = tree.find('page:Page', NSMAP).attrib
        img = Image.open(project_dir+"/processing/"+img_info['imageFilename'].replace('.png','.bin.png'))

        # Make copy of pagexml in subdir 'old_processing'
        legacy_dir = Path(XML).parents[1].joinpath('old_processing')
        legacy_dir.mkdir(exist_ok=True)
        # Write legacy pagexml
        with open(legacy_dir / img_info['imageFilename'].replace('.png','.xml'), 'w') as OUT:
            output_string = etree.tostring(tree, encoding='unicode', method='xml')
            OUT.write(output_string)

        # Find lines and OCR with Tesseract
        print("Starting OCR on page with tesseract ...")
        for line in tree.findall('.//page:TextLine', NSMAP):
            coords = line.find('page:Coords', NSMAP).attrib['points']
            m = mask(coords)
            output = plt.imshow(m)
            ocr = pytesseract.image_to_string(m, lang='rus')
            ocr_text = line.find('page:TextEquiv[@index="1"]', NSMAP)
            if ocr_text is not None:
                ocr_text.text = ocr
            else:
                ocr_text = etree.SubElement(line,'page:TextEquiv[@index="1"]', NSMAP)
                ocr_text.text = ocr
        print("Done.")

        # Write new pagexml with Tesseract OCR
        with open(XML, 'w') as OUT:
            OUT.write(etree.tostring(tree, encoding='unicode', method='xml'))
            print(f"New {XML.name} written.")


# In[ ]:




