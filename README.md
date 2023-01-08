![app icon](assets/smart_grids-icon.png)

# SmartGrids

SmartGrids is a small, free application that allows you to easily configure and preview typography grids.
You can input parameters like the page size, margins, font size, and leading, SmartGrids will then show you possible grid configurations.

Unlike the built-in grid creation tools in Adobe InDesign, the grids will automatically be aligned to your body copy. The gridlines can be aligned with the Cap-Height, Ascender, or x-Height of the text. It also allows for a baseline shift so that the gridlines don't align with the baseline of the text but with the descenders.

![preview image](assets/readme_image-1.png)

Creating Cap-Height aligned grids in Adobe Indesign is not impossible, but involves a lot of trial and error and manual measuring. The applications allow you to skip the tedious guesswork and manual calculations. SmartGrids will show you all possible grid configurations and output all relevant values which you can then input into your layout software.

The grids follow the style proposed by Josef Müller-Brockamann in his influential 1981 book [Grid Systems in Graphic Design](https://books.google.de/books/about/Grid_Systems_in_Graphic_Design_a_Visual.html?id=YOgtwAEACAAJ&redir_esc=y). Typographic grids help you structure your layouts in a meaningful and clean way. When working on larger editorial projects they can speed up your workflow significantly.

Because of its type-first approach the application might enlarge the ```bottom margin``` to fit a whole number of lines into the text area. (After all we can't work with half a line of text, can we?) This means, that you have to use the new ```bottom margin``` suggested by the application in your layout software. This change will never be greater than the ```line height```.

## What units should I use?
SmartGrids does not currently support automatic unit conversion as we know it from our Adobe programs. This means, that all values must be put in as point values. This includes the dimensions and margins of the page. Luckily for us, in Adobe InDesign ```1 pt. == 1 px.```. This means that when you're setting up a grid for a digital setting in Adobe InDesign you can use pixels and points interchangeably. When you're using inches or millimeters you will need to do some conversion.

## Required packages
All packages may be installed via ```pip``` in the terminal.

- [PIL](https://pypi.org/project/Pillow/)
- [FontTools](https://pypi.org/project/fonttools/)
- [PyQt5](https://pypi.org/project/PyQt5/)

### Copyright
Copyright (c) 2023, Carl J. Kurtz. (See [LICENSE](LICENSE) for more information)