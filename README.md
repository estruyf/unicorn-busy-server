# Simple server for Raspberry Pi with Pimoroni Unicorn hat

* [Introduction](#Introduction)
* [Installation](#Installation)
* [Usage](#Usage)
    * [Set the display to On](#on)
    * [Set the display to Off](#off)
    * [Get the server Status](#status)
    * [Get a list of supported Icons](#icons)
    * [Set Display to a colour using HSV](#hsv)
    * [Set Display to show a Rainbow](#rainbow)
    * [Set Display to a colour using RGB](#rgb)
    * [Set Display to show Icon](#icon)
    * S[et the Display to show JSON output](#json)
    * [Shutdown the Server](#shutdown)
* [Todo](#Todo)
* [License](#License)

# Introduction

OK this is my branch of the unicorn-busy-server.  I've made some updates to support both the [Unicorn Phat](https://shop.pimoroni.com/products/unicorn-phat) and [Unicorn Mini](https://shop.pimoroni.com/products/unicorn-hat-mini) from [Pimoroni](https://shop.pimoroni.com/).  I have also add the following features:

* Updated install script to make installation simple and repeatable
* HSV support for homebridge RGB lighting support
* Icon and JSON support
* Rainbow effect
* Startup and Shutdown actions to tell you what your Pi status light is doing

# Installation

OK this bit is hopefully the easy bit.  You can just copy and paste the following in to a terminal and it will install all the required files, enable and start the service.  If you are running Raspbian or Ubuntu The short version is:

```bash
curl -LSs https://raw.githubusercontent.com/j-maynard/unicorn-busy-server/master/install.sh | sudo bash -
```

If you have trust issue like many do you'll probably want to do the following:

```bash
cd /tmp
curl -LSs https://raw.githubusercontent.com/j-maynard/unicorn-busy-server/master/install.sh
cat install |more # So you can see the contents of the script a page at time
sudo bash ./install.sh -V -i /home/pi/unicorn-busy-server
```

Currently the script only runs on Raspbian/Ubuntu I am accepting pull requests to extend the PR to support other distributions.  I plan to add support for Debian shortly.

If you want to clone/fork this repo and carry on development on a more sensible machine you can install the required files without needing to install the service by doing the following:

```bash
curl -LSs https://raw.githubusercontent.com/j-maynard/unicorn-busy-server/master/install.sh
bash ./install.sh -d
```

The scripts usage output is as follows:

```
Unicorn Busy Server installation script 0.5
(c) Jamie Maynard 2020

Usage:
  -i  --install-dir        Specify where you want to install to
                           Default is: /home/pi/Development/unicorn-busy-server
  -d  --development        Install for development only (no service installation)
  -V  --verbose            Shows command output for debugging
  -v  --version            Shows version details
  -h  --help               Shows this usage message
```

# Usage

If you've run the install script (without the -d option) check the Unicorn hat attache to your Pi.  If all has gone according to plan the unicorn hat will be changing colours.  Once its going through all 360 Hues within the HSV spectrum it'll go blank.  As soon as the Uniron hat lights up the `Busylight Server` is ready to start recieving commands.

The API is fairly simple though has been extend quite a bit from its oriignal implementation.  The Busy server has the following API endpoing:

| Method                                                  | Endpoint                           | Description                                                          |
|:-------------------------------------------------------:|------------------------------------|----------------------------------------------------------------------|
| [<span style="color: blue">**GET**</span>](#on)         | [`/api/on`](#on)                   | Turn the Unicorn Hat on to a random colour                           |
| [<span style="color: blue">**GET**</span>](#off)        | [`/api/off`](#off)                 | Turn the Unicorn Hat off                                             |
| [<span style="color: blue">**GET**</span>](#status)     | [`/api/status`](#status)           | Get the status of the Unicorn Hat/Pi                                 |
| [<span style="color: blue">**GET**</span>](#icons)      | [`/api/icons`](#icons)             | Get a list of support icons for your Unicorn hat                     |
| [<span style="color: green">**POST**</span>](#hsv)      | [`/api/display/hsv`](#hsv)         | Set the display to a specific colour using HSV Integer values        |
| [<span style="color: green">**POST**</span>](#rainbow)  | [`/api/display/rainbow`](#rainbow) | Set the display to cycle through all 360 hues in the HSV spectrum    |
| [<span style="color: green">**POST**</span>](#rgb)      | [`/api/display/rgb`](#rgb)         | Set the display to a specific colour using RGB Integer values        |
| [<span style="color: green">**POST**</span>](#icon)     | [`/api/display/icon`](#icon)       | Set the display to show a specific icon in your choice of RGB colour |
| [<span style="color: green">**POST**</span>](#json)     | [`/api/display/json`](#json)       | Set the display to what you want using the support JSON format       |
| [<span style="color: red">**DELETE**</span>](#shutdown) | [`/api/shutdown`](#shutdown)       | Shutdowns down the Pi after 2 minutes **(Can't be cancelled)**       |

## <a id="on"></a> Set the display to On

| Method                                      | Endpoint  |
|:-------------------------------------------:|-----------|
| <span style="color: blue">**GET**</span>    | `/api/on` |

### Description
The simpelest method there is.  It turns the Unicorn Hat on to a random colour.

### Result

Returns `200 OK` and an Empty JSON Object `{}`

## <a id="off"></a> Set the display to Off

| Method                                      | Endpoint   |
|:-------------------------------------------:|------------|
| <span style="color: blue">**GET**</span>    | `/api/off` |

### Description
Another really simple method.  This Turns the Unicorn Hat off.

### Result
Returns `200 OK` and an Empty JSON Object `{}`

## <a id="status"></a> Get the server Status

| Method                                      | Endpoint      |
|:-------------------------------------------:|---------------|
| <span style="color: blue">**GET**</span>    | `/api/status` |

### Description

Get the status of the pi

### Result

Returns `200 OK` and the following JSON Object:

```json
{
  "blue": 110,
  "brightness": 0.5,
  "cpuTemp": 39.546,
  "green": 60,
  "height": 8,
  "icon": "none",
  "lastCalled": "Sun, 17 May 2020 18:00:33 GMT",
  "lastCalledApi": "/api/on",
  "red": 247,
  "unicorn": "phat",
  "width": 4
}
```

## <a id="icons"></a> Get a list of supported Icons

| Method                                      | Endpoint      |
|:-------------------------------------------:|---------------|
| <span style="color: blue">**GET**</span>    | `/api/icons`  |

### Description

Gets a list of supported Icons for the Hat currently attached to the Pi

### Result

Returns `200 OK` and the following JSON Object:

```json
{
  "height": 8,
  "icons": [
    "pencil",
    "exclaim",
    "phone",
    "dnd",
    "arrow-down",
    "numbers/0",
    "numbers/4",
    "numbers/5",
    "numbers/1",
    "numbers/8",
    "numbers/7",
    "numbers/6",
    "numbers/2",
    "numbers/9",
    "numbers/3"
  ],
  "unicorn": "phat",
  "width": 4
}
```

## <a id="hsv"></a> Set Display to a colour using HSV

| Method                                       | Endpoint            |
|:--------------------------------------------:|---------------------|
| <span style="color: green">**POST**</span>   | `/api/display/hsv`  |

### Description

Set the display to any colour defined in HSV Integer Values.  See an HSV Colour picker such as (Such as this one from AlloyUI)[https://alloyui.com/examples/color-picker/hsv.html]

This method was added to allow the Unicorn PHAT/Mini to be used in conjuntion with the Homekit/Homebridge RGB Light profile and possibly Razer Synapse.  (Currently investigating integrations)

### Request

Hue, Saturation, Value are all json numbers (preferably integers) and all are required to set the colour of the Unicorn.

Optionally you can specify the brightness of the Unicorn.  This is a float value between 0 and 1.  The default is set to 0.5.

Optionally you can also specify the blink speed.  This specifies the speed in seconds which the Unicorn turns on and off.

Example Request JSON:

```jsonc
{
    "hue":0,
    "saturation":100,
    "value":100,
    "brightness": 0.5,      // Optional
    "speed": 1              // Optional
}
```

### Result
Returns `200 OK` and an Empty JSON Object `{}`

## <a id="rainbow"></a> Set Display to show a Rainbow

| Method                                       | Endpoint                |
|:--------------------------------------------:|-------------------------|
| <span style="color: green">**POST**</span>   | `/api/display/rainbow`  |

### Description

This method was build off the back of the HSV method above.  You can step horizontally across the HSV spectrum from 0 to 360 this allows you to cycle through all colours of a spectrum.  It is similar to Razer Synpases "Spectrum" effect.  It makes a nice display when you're not doing anything and can be helpful for making sure your Unicorn Phat/Mini is setup correctly.

### Request

All values are optional in this request so its possible to send a request like the one below and still have the rainbow effect activate.

```json
{}
```

However you can customise your rainbow first by specifying the starting `hue`.  This is an integer between `0` and `360`.  The default is `0` which is Red.

You can specify your `step` through the hue range.  This again can be any number between `1` and `90`  The bigger the number the greater the change between between transitioning colours.  Smaller numbers result in a much smooter transition.  The default is `1`.

You can specify the transition `speed`, that is the speed at which the colours change.  This is any number in seconds the smaller the number the quicker the change the quicker you cycle through the hue spectrum.  The default is `0.2`

Finally you can specify the `brightness` this is any floating point number between `0` and `1`.  The default is `0.5`.

Example request JSON:


```jsonc
{
    "hue": 0,               // Optional
    "step": 1,              // Optional
    "brightness": 0.5,      // Optional
    "speed": 1              // Optional
}
```

### Result

Returns `200 OK` and an Empty JSON Object `{}`

## <a id="rgb"></a> Set Display to a colour using RGB

| Method                                       | Endpoint            |
|:--------------------------------------------:|---------------------|
| <span style="color: green">**POST**</span>   | `/api/display/rgb`  |

### Description

This is the original RGB method for setting the display to a single colour.

### Request

You have to specify the vaules for `red`, `green` and `blue`.  These are integers between `0` and `255`.

Optionally you can specify the brightness of the Unicorn.  This is a float value between 0 and 1.  The default is set to 0.5.

Optionally you can also specify the blink speed.  This specifies the speed in seconds which the Unicorn turns on and off.

```jsonc
{
    "red":0,
    "green":255,
    "blue":0,
    "brightness": 0.5,      // Optional
    "speed": 1              // Optional
}
```

### Result

Returns `200 OK` and an Empty JSON Object `{}`

## <a id="icon"></a> Set Display to show Icon

| Method                                       | Endpoint             |
|:--------------------------------------------:|----------------------|
| <span style="color: green">**POST**</span>   | `/api/display/icon`  |

### Description

It possible to set the display to display some pixel art (icon) rather than just a single solid colour.  The icon files can be found in `icons/phat` and `icons/mini` and will be displayed according to which Unicorn hat you are using.  You can get a current list of available icons by making a <span style="color: blue">**GET**</span> request to the [Icons endpoint at `/api/icons`](#icons).

### Request

As with the RGB request you have to specify the vaules for `red`, `green` and `blue`.  These are integers between `0` and `255`.  In addition you also have to specify the `icon` you want to display.  If you make a request for an icon which doesn't exist you'll get a 500 repose.

Optionally you can specify the `brightness` of the Unicorn.  This is a float value between 0 and 1.  The default is set to 0.5.

Optionally you can also specify the blink `speed`.  This specifies the speed in seconds which the Unicorn turns on and off.

```jsonc
{
    "red": 255,
    "green": 0,
    "blue": 0,
    "icon": "dnd",
    "brightness": 0.5,      // Optional
    "speed": 1              // Optional
}
```

### Result

Returns `200 OK` and an Empty JSON Object `{}`

If a request is made for a non-existant icon file it returns `500 INTERNAL SERVER ERROR` and the following JSON object:

```json
{
  "error": "Invalid Icon name",
  "message": "No icon file matches ./icons/phat/numbers/01.json... Maybe think about creating it?"
}
```

## <a id="json"></a> Set the Display to show JSON output

| Method                                       | Endpoint             |
|:--------------------------------------------:|----------------------|
| <span style="color: green">**POST**</span>   | `/api/display/json`  |

### Description

This version of the busylight-server has support for processing a json object to set the display.  It allows you to address all the pixels on your unicorn hat.  This allows you to test your own icons before you save them and give you some certainty they will work.  You can specify RGB colours for each pixel.

Each file is made up of the following elements:

* Header
* 3D Array of Pixels
* Indvidual Pixels

Basic example JSON:

```json
{
    "name": "string",
    "size": {
        "height": 1,
        "width": 1
    },
    "pixels": [
        [
            { "red": -1, "green": -1, "blue": -1 }
        ],
    ]
}
```

This is a unicorn with a height of 1 and width of 1.

#### Header

The header contains some basic information such as the `name` and the specified `size` of the 3D array specifing the `height` and `width`.  The size information is really important as this is used to validate the file's contents and make sure it matches the size of the Unicorn being used.

#### 3D Array of Pixels

A 3D array is an array of arrays.  Its a simple concept... the first array represents the height (or the number of rows) of the Unicorn.  Each inner array represents the width (or the columns) of the Unicorn.  In the inner array there should a number pixel objects.   There should be as many rows and columns as specified in the height and width values of the size object in the header and again this should in turn match the reported height and width of your Unicorn.

#### Pixels

At the heart of your 3D array you should specify the correct number of pixel object.  The values for `red`, `green` and `blue` the same as you do for the [RGB display endpoint](#rgb).  There is a slight difference in that you can also speicfy a value of `-1` for each colour channel.  This sets it to the base value for the colour channel specified in the request.  Below are some example pixel objects:

| Pixel JSON Object                           | Description
|---------------------------------------------|-----------------------------------|
| `{ "red": 0, "green": 0, "blue": 0 }`       | An **off** pixel.                 |
| `{ "red": 255, "green": 255, "blue": 255 }` | An **on** white pixel             |
| `{ "red": 255, "green": 0, "blue": 0 }`     | An **on** red pixel               |
| `{ "red": 0, "green": 255, "blue": 0 }`     | An **on** green pixel             |
| `{ "red": 0, "green": 0, "blue": 255 }`     | An **on** blue pixel              |
| `{ "red": -1, "green": -1, "blue": -1 }`    | A pixel set to the default colour |

### Request

A full example of the json request can be found in the examples folder.

`json` must be a valid json object.  This will also be validated using the built in validator to make sure the right number of pixels and rows has been specified.

You also have to specify the vaules for `red`, `green` and `blue`.  These are integers between `0` and `255`.  These are used as the base colour for any pixel where the colour channel has been set to -1.

Optionally you can specify the `brightness` of the Unicorn.  This is a float value between 0 and 1.  The default is set to 0.5.

Optionally you can also specify the blink `speed`.  This specifies the speed in seconds which the Unicorn turns on and off.


```jsonc
{   
    "json": {},             //Abriviated Object
    "red": 255,
    "green": 0,
    "blue": 0,
    "brightness": 0.5,      // Optional
    "speed": 1              // Optional
}
```

### Result

Returns `200 OK` and an Empty JSON Object `{}`

If you submit an invalid JSON object you'll get a `500 INTERNAL SERVER ERROR` with the following JSON.  This information should be helpful in debugging any issues you may encounter.

```json
{
  "error": "Invalid Json",
  "message": "An error occured, Missing JSON Key: 'size'"
}
```

## <a id="shutdown"></a> Shutdown the Pi

| Method                                       | Endpoint         |
|:--------------------------------------------:|------------------|
| <span style="color: red">**DELETE**</span>   | `/api/shutdown`  |

### Description

The most useful addition for a headless device.  The busylight-server ultimately runs on a small linux computer and they do prefer to be shutdown properly.  This method is all about doing that safely.  Simply send a delete request to `/api/shutdown` and it will kick off a 2 minute count down to shutdown.  The Unicorn will start to display a flashing yellow arror or shevrons to indicate its shutting down.  At 10 seconds from shutdown it will start to count down from `9 -> 0` before the Unicorn then turns `red` and a few seconds later the Unicorn will go blank.  It should be safe to unplug the Pi now.

### Result

Returns `200 OK` and an Empty JSON Object `{}`

# Todo

- [ ] Add a frontend (currently in progress)
- [ ] Finish implementing support for HTML colours
- [ ] Add a dummy unicornhat/unicornhat-mini to the wrapper which displays the output to console or a TK Window
- [ ] Add support for Debian
- [ ] Add support for Arch
- [ ] Add support for DietPi
- [ ] Add support for development on Mac OS X and Windows
- [ ] Add for a "Wave" display
- [ ] Add support for Razer Synapse

# License

**MIT License**

Copyright (c) 2020 [*Jamie Maynard*](https://github.com/j-maynard)<br>
Parts Copyright (c) 2020 [*Elio Struyf*]()

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
