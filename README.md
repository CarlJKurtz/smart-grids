# SmartGrids

SmartGrids is a small application that allows you to easily configure and preview typography grids.
You can input parameters like the page size, margins, font size, and leading and SmartGrids will show you all the possible grid configurations.

Unlike the built-in grid creation tools in Adobe InDesign, SmartGrids will automatically align the grid to your body copy. The gridlines can be aligned with the cap-height, ascender, or x-height of the text. It also allows for a baseline shift so that the gridlines don't align with the baseline of the text but with the descenders.

![preview image](assets/readme_image-1.png)

Creating cap-height aligned grids in Adobe InDesign is not impossible, but involves a lot of trial and error and manual measuring. The applications allow you to skip the tedious guesswork and manual calculations. SmartGrids will show you all possible grid configurations and output all relevant values which you can then input into your layout software.

The grids follow the style proposed by Josef Müller-Brockamann in his influential 1981 book [Grid Systems in Graphic Design](https://books.google.de/books/about/Grid_Systems_in_Graphic_Design_a_Visual.html?id=YOgtwAEACAAJ&redir_esc=y). Typographic grids help you structure your layouts in a meaningful and clean way. When working on larger editorial projects they can speed up your workflow significantly.

Because of its type-first approach the application might enlarge the ```bottom margin``` to fit a whole number of lines into the text area. (After all we can't work with half a line of text, can we?) This means, that you have to use the ```corrected bottom margin``` suggested by the application in your layout software. This change will never be greater than the ```line height```.

## Installation
### MacOS:
**Just install it:**
The easiest way is to download the latest release, which will download a ```.dmg``` file which you install just like every other app on your machine.

**Download the source code:**
If you prefer the nerdy way, you can download the source code and run the ```main.py``` file with python.
This requires you to have python3 and the required packages installed. (See [Required packages](##Required-packages))

### Windows:
On Windows, you need to download the source code and run the ```main.py``` file via python. This requires the same packages to be installed. (See [Required packages](##Required-packages))

### Compile SmartGrids from source:
SmartGrids is compiled with the module _pyinstaller_. To compile it from source, install the required packages (see [Required packages](##Required-packages)) and pyinstaller with ```$ pip install pyinstaller```.
Then run ```build.py``` with python. An app-file will be created inside the new _dist_ folder.

## How to use SmartGrids
When setting up a grid with SmartGrids it is helpful to know your Page dimensions, including the preferred margins as well as the font of choice, its size, and its leading beforehand. It is suggested to create the document in InDesign and test out these values beforehand.
1. Input all values into SmartGrids and select the font.
2. Chose your vertical alignments. The vertical alignment specifies which part of the text the gridlines will align. When _Cap-Height_ is selected the guides will align with the Cap-Height of the font and so on.
3. Chose the lines between the cells. (The default is 1.)
4. In the Output panel under _Possible Divisions_, it will hopefully show you multiple numbers. These are all possible ways you can divide the text area vertically. (2 will give you 2 rows, 3 will 3, etc.) You can preview them by inputting them under Amount of Rows. If it says _None_, there is no possible way to divide the text area into even rows. But fear not! The most efficient way to find a possible configuration is to decrease the bottom margin or change the leading.
5. Preview the configuration by setting the desired amount of rows.
6. **Optional!** Configure and preview the columns. (The default _column gutter_ is equal to the _row gutter_)
7. Copy the values into InDesign. Set up the baseline grid under ```InDesign - Preferences - Grids``` (Don't forget the grid start.) and create guides under ```Layout - Create Guides``` in InDesign according to the output values. **Important:** SmartGrids will likely increase the bottom margin a bit to fit a whole number of lines so you must adjust your bottom margin in InDesign as well.

### What units should you use?
SmartGrids does not currently support automatic unit conversion as we know it from our Adobe programs. This means, that all values must be put in as point values. This includes the dimensions and margins of the page. Luckily for us, in Adobe InDesign ```1 pt. == 1 px.```. This means that when you're setting up a grid for a digital setting in Adobe InDesign you can use pixels and points interchangeably. When you're using inches or millimeters you will need to do some conversion.

## Required packages
All packages may be installed via ```pip3``` in the terminal.

````$ pip install package````

- [PIL](https://pypi.org/project/Pillow/)
- [FontTools](https://pypi.org/project/fonttools/)
- [PyQt5](https://pypi.org/project/PyQt5/)

### Support
SmartGrids is entirely free of charge for both commercial and private use! But code doesn't write itself — so please consider sharing this project with a fellow design aficionado, or even support the project by sponsoring it here on GitHub if you got some use out of it!

Thank you, and happy designing! 🥳

### Copyright
Copyright (c) 2023, Carl J. Kurtz. (See [LICENSE](LICENSE) for more information)