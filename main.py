import win32con
import win32gui
import requests
import textwrap
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from configparser import ConfigParser 


# Specify the file path
path = u'C:\\Stuff\\Projects\\Video\\Wallpaper\\Quotes\\Background.jpg'
save_path = 'C:\\Stuff\\Projects\\Video\\Wallpaper\\Quotes\\toSet.jpg'

#City
cityToSearch = "London"

# extract key from the 
# configuration file 
config_file = "config.ini"
config = ConfigParser() 
config.read(config_file) 
api_key = config['chris']['api'] 
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

#Quotes API
quotes_url = "https://waifu.it/api/v4/quote"
quotes_api = config['chris']['quotes_api'] 
  
  
# explicit function to get 
# weather details 
def getweather():
    try:
        result = requests.get(url.format(cityToSearch, api_key)) 
        
        if result: 
            json = result.json() 
            city = json['name'] 
            country = json['sys'] 
            temp_kelvin = json['main']['temp'] 
            temp_celsius = temp_kelvin-273.15
            weather1 = json['weather'][0]['main'] 
            final = f"{int(temp_celsius)}°C, {weather1}" 
            return final 
        else: 
            return "Error"
    except Exception:
        return None
  
  
# explicit function to 
# search city 
def search(): 
    weather = getweather()
    if weather: 
        return weather
    else: 
        return None
    
def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

def set_text(file, txt, location=(10,10), font_size=18):
    # Open an Image
    img = Image.open(file)

    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img)

    # Custom font style and font size
    myFont = ImageFont.truetype(r"C:\\windows\\Fonts\\Arial.ttf", font_size)

    # Add Text to an image
    I1.text(location, txt, font=myFont, fill=(255, 255, 255))

    # Save the edited image
    img.save(save_path)

def set_quote_center(file, lines, author=None, font_size=38):
    img = Image.open(file)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(r"C:\\windows\\Fonts\\Arial.ttf", font_size)

    max_width = 0
    total_height = 0
    for line in lines:
        width, height = textsize(line, font=font)
        max_width = max(max_width, width)
        total_height += height

    x = (img.width - max_width) // 2
    y = (img.height - total_height) // 2

    line_heights = []
    for line in lines:
        width, height = textsize(line, font=font)
        line_heights.append(height)

    line_y = y
    for i in range(len(lines)):
        line_x = x + (max_width - textsize(lines[i], font=font)[0]) // 2
        draw.text((line_x, line_y), lines[i], fill=(255,255,255), font=font)
        line_y += line_heights[i]

    # Add the author name
    if author:
        author_x = x + (max_width - textsize(author, font=font)[0])
        author_y = line_y
        draw.text((author_x, author_y), f"- {author}", fill=(255,255,255), font=font)
    
    img.save(save_path)

def get_quote():
    try:
        response = requests.get(quotes_url, headers={
            "Authorization": quotes_api,
        })
        if response:
            return response.json()
        else:
            return "Error"
    except Exception:
        return "Error"

def set_wallpaper():
    # Check for network
    weather = search()
    i = 0
    while weather == None:
        set_quote_center(path, textwrap.wrap(f"Disconnected, retrying in {i} seconds...", width=80))
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, save_path, 3)
        time.sleep(i)
        i += 30
        weather = search()
        
    
    quote_data = get_quote()
    text = ""

    #Set Weather
    set_text(path, f"{weather}", location=(1750,950), font_size = 28)

    if (quote_data != "Error"):
        #Set Quote
        set_quote_center(save_path, textwrap.wrap(quote_data.get("quote"), width=80), quote_data.get("author"))

    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, save_path, 3)

if __name__ == "__main__":
    while (True):
        set_wallpaper()
        time.sleep(60*60)
