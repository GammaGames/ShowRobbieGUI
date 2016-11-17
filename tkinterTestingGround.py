import Tkinter

# open a SPIDER image and convert to byte format    
im = Image.open("img/placeholder_image.gif")

root = Tkinter.Tk()  # A root window for displaying objects

# Convert the Image object into a TkPhoto object
tkimage = ImageTk.PhotoImage(im)

Tkinter.Label(root, image=tkimage, text="Update User", compound=Tkinter.CENTER).pack() # Put it in the display window

root.mainloop() # Start the GUI