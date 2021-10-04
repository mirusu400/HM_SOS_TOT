# Story of seasons: Trio of Towns Fan Translation
Harvest Moon - Story of Seasons Trio Of Towns Korean Translate Git

# For anyone who wanted to make fan translation...
I know, there are very seldom people willing to do this gigantic job.

But I just write this documentaion who loved this game very much.

## 1. Make font
You should modify `romfs/Font/mainfont.bffnt` and `romfs/Font/subfont.bffnt`.

Trio of Towns use `bffnt` font, which usually use 3DS games and WiiU Games.

You can extract / build bffnt files using [3dsTool](https://github.com/ObsidianX/3dstools)

On a `/font` directory, I make a example manifest file and sheet PSD (photoshop) files for korean glyphs. You can modify and make your own font.


## 2. Edit texts
Story of Seasons use custom archiving structure, you should unpack yourself.

### 2-1. Unpack xbb file
On a `romfs/Msg.xbb`, `romfs/DataText.xbb`, there are almost whole texts datas.

But you should unpack, using `Kerameru` which bundled in [Kuriimu](https://github.com/IcySon55/Kuriimu) 

You can extract each xbb and get lots of raw datas, I'll call us `PAPA` files. (Because it has `PAPA` flag at the head of file.)

### 2-2. Convert PAPA file as JSON file
Using `extract.py`, you can convert PAPA as JSON file. Just drag and drop original file/folder and automatically convert as JSON file.

Modify extracted texts, but *YOU SHOULD NOT EDIT ascii ENCODED TEXTS.* if you modify these, games cannot recognize original texts. You only edit *UTF-16* sections.

After modify, use `import.py` and you get `*.out` file. Using `Kerameru` to replace original file, and build or use layeredfs to apply to game.

# Warning
`extract.py` cannot extract whole PAPA files, it can only extract text datas (from Msg.xbb)