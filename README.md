# ColonyCounter

## Deprecated! 
## New version can be found [here](https://github.com/ColonyCounter/CascadeImgScript)

*samplefilecreator* is used to create the *bg.txt* and *info.data* files used by *opencv_createsamples*.

Also contains the data folder that can be copied into the build dir of the [ColonyCounter](https://github.com/ColonyCounter/ColonyCounter-GUI) to enable the cascade classifier.

## Usage

```python
# Run with:
python simplefilecreator -g jpg -p /home/me/Pictures/ -f + -w 25 -h 25

# Usage:
# -g: jpg or png
# -p: path to dir
# -f: + for positive images or - for bg
# -w: width that images should be resized to
# -h: height that images should be resized to
# -m: resize to mean size value of images
```




#### It assumes the following dir structure
Images just need **.jpg**, **.jpeg** or **.png** at the end, names do not matter
```
path-to-dir/
        pos/
            img1.jpg
            img2.jpg
            ...
        pos_resized/
            ...
        neg/
            img1.jpg
            img2.jpg
            ...
        bg.txt
        info.data
```

#### bg.txt then contains:

```
neg/img1.pg
neg/img2.jpg
```
#### info.data then contains:

```
pos/img1.jpg 1 0 0 25 25
pos/img2.jpg 1 0 0 25 25
```
