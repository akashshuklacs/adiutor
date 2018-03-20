from firebase import firebase
import os
import requests
import json
import tkinter as tk
import random
import webbrowser
from PIL import Image, ImageTk
from tkinter import filedialog, Label
from subprocess import call

root = tk.Tk()

# Get Live Location
def get_location():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    lon, lat = str(lon), str(lat)

    format_lon = ""
    for i in range(len(lon)):
        if lon[i] == ".":
            format_lon += "_"
        else:
            format_lon+=lon[i]

    entry_longitude = format_lon
    
    format_lat = ""
    for i in range(len(lat)):
        if lat[i] == ".":
            format_lat += "_"
        else:
            format_lat += lat[i]
    entry_latitude = format_lat
    entry_latitude_longitude = entry_latitude + "_" + entry_longitude

    return [format_lat, format_lon, entry_latitude_longitude, entry_latitude, entry_longitude]

def database_processing(database_name, issue, entry_latitude_longitude):
    fire = firebase.FirebaseApplication('https://rajasthanhackathon-bd003.firebaseio.com/', None)
    result = fire.get("/"+ database_name + "/" + issue, entry_latitude_longitude)
    if result != None:
        complain = fire.get("/"+ database_name + "/" + issue + "/" + entry_latitude_longitude, "complains")
        updated_complain = int(complain) + 1
        result = fire.put("/"+ database_name + "/" + issue + "/" + entry_latitude_longitude, "complains", updated_complain)
        print(result)
    else:
        result = fire.put("/"+ database_name + "/" + issue + "/" + entry_latitude_longitude, "complains", "1")
        print(result)
        result = fire.put("/"+ database_name + "/" + issue + "/" + entry_latitude_longitude, "severity_index", "10")
        print(result)
        
#Browsing Images from the Gallery
def browse():
    path=tk.filedialog.askopenfilename(filetypes=[("Image File",'.jpg')])
    im = Image.open(path)
    tkimage = ImageTk.PhotoImage(im)
    myvar=tk.Label(root,image = tkimage)
    myvar.image = tkimage
    myvar.pack()
    #call("bash ./test.sh", shell="True")
    os.system("python ./tf_files/label_image.py --graph=tf_files/retrained_graph.pb --labels=tf_files/retrained_labels.txt --image="+path)
	

    # getting user's input latitude and longitude
    entry_latitude = entry_1.get()
    entry_longitude = entry_2.get()
    if entry_latitude == "" or entry_longitude == "":
        location_details = get_location()
        format_latitude, format_longitude, entry_latitude_longitude, entry_latitude, entry_longitude = location_details[0], location_details[1], location_details[2], location_details[3], location_details[4]
        database_processing("feedback", "potholes", entry_latitude_longitude)
    else:
        database_processing("feedback", "potholes")

def qwerty():
    call("./enhance.sh", shell="True")
    webbrowser.open("https://srivastavvaibhav.carto.com/builder/797a88ac-6ffa-42a0-8fa5-f3e0a94e3a0a")

frame = tk.Frame(root)

# width x height + x_offset + y_offset:
root.geometry('{}x{}'.format(400, 400))

# User Interface
services = ['Feedback','Service Enhancement']
for i in range(2):
    ct = [random.randrange(256) for x in range(3)]
    #brightness = int(round(0.299*ct[0] + 0.587*ct[1] + 0.114*ct[2]))
    #ct_hex = "%02x%02x%02x" % tuple(ct)
    bg_colour ="#4286f4"
    if i == 0:
        l = tk.Button(root, 
                text=services[i], 
                #fg='White' if brightness < 120 else 'Black', 
                bg=bg_colour,
                command=browse)
        
    else:
        l = tk.Button(root, 
                text=services[i], 
                #fg='White' if brightness < 120 else 'Black',
                bg=bg_colour,
                command=qwerty)
        
    l.place(x = 20, y = 30 + i*30, width=180, height=25)

entry_1 = tk.Entry(root)
entry_2 = tk.Entry(root)

root.mainloop()
