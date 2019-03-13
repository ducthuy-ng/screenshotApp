from PIL import ImageGrab, ImageTk, Image
from Tkinter import *
from sets import Set
import ttk
import os
import re


# Define some constants
app_width = 300
app_height = 60

padding_size = 3

btn_width = 7

cropped_width = 400
cropped_height = 400

current_dir = os.path.dirname(__file__)
image_folder = 'mine'


class MyApp(object):
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.title("Screenshot App")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure('TLabel', font = ('Arial', 13))

        self._toolbarDisplay()

                 
    #----------------------------------------------------------------------
    def show(self):
        self.root.update()
        self.root.deiconify()

    #----------------------------------------------------------------------
    def returnToToolbar(self, event=None):
        self._indexMenu.destroy()
        self.show()
        

    #----------------------------------------------------------------------
    """
    A function for get all the image 
    """
    def getScreenAndIndexList(self):
        file_list = os.listdir(os.path.join(current_dir, image_folder))
        screenList = {}
        for file_name in file_list:
            if re.match('^\w+\.\w+\.png$', file_name):
                file_split = re.split('\.', file_name)
                if file_split[0] in screenList:
                    screenList[file_split[0]].append(file_split[1])
                else:
                    screenList[file_split[0]] = [file_split[1]]

        del file_list, file_name, file_split         
        return screenList
        


    #----------------------------------------------------------------------
    """
    A function for saving image with the screen and index as parameter
    """
    def saveImg(self, img, screenName, indexName):
        LOGFILE_NAME = screenName + '.' + indexName + '.png'    
        LOGFILE_PATH = os.path.join(current_dir, image_folder, LOGFILE_NAME)  # Get the file name

        img.save(LOGFILE_PATH)
        del LOGFILE_NAME, LOGFILE_PATH

        self.returnToToolbar()
        

    #----------------------------------------------------------------------
    def _scrBtn_pressed(self):
        self.root.wm_withdraw()

        img = ImageGrab.grab()

        self._indexMenuDisplay(img)    
        

    #----------------------------------------------------------------------
    def _toolbarDisplay(self):
        """
        Draw the toolbar, which contain the screenshot button, the Btn1, Btn2
        """
        
        self.mainFrame = ttk.Frame(self.root, height=app_height)
        self.mainFrame.pack(fill=BOTH, expand=1)

        # Draw take screenshot button
        self.scrBtn_img = PhotoImage(file=current_dir + "\picture\scrBtn.gif").subsample(6, 6)

        self.scrBtn = ttk.Button(self.mainFrame, width=btn_width, command=self._scrBtn_pressed)
        self.scrBtn.config(image=self.scrBtn_img, compound=CENTER)
        self.scrBtn.grid(column=0, padx=padding_size, pady=padding_size)


    #----------------------------------------------------------------------
    def _indexMenuDisplay(self, img):
        def changeIndexBox(event):
            if self._screenBox.get() not in self._screenList: self._indexBox.configure(value=[])
            else: self._indexBox.configure(value=self._screenList[self._screenBox.get()])
       
            
        self._indexMenu = Toplevel(self.root)
        
        # Cropped and grayscale the picture
        x_center = img.size[0] / 2
        y_center = img.size[1] / 2

        left = x_center - cropped_width / 2
        top = y_center - cropped_height / 2
        right = x_center + cropped_width / 2
        bottom = y_center + cropped_height / 2
        
        cropped = img.crop( ( left, top, right, bottom ) ).convert('LA')

        self._capturedImg = ImageTk.PhotoImage(cropped)


        # Labels
        ttk.Label(self._indexMenu, text="Screen:").grid(column=0, row=0, sticky='w', padx=5, pady=5)
        ttk.Label(self._indexMenu, text="Index:").grid(column=0, row=1, sticky='w', padx=5, pady=5)

        self._screenList = self.getScreenAndIndexList()
        

        
        # Screen and Index Combobox
        self._screenBox = ttk.Combobox(self._indexMenu, width=50)
        self._indexBox = ttk.Combobox(self._indexMenu, width=50)

        self._screenBox.grid(column=1, row=0, columnspan=2, padx=5, pady=5, sticky='w')
        self._indexBox.grid(column=1, row=1, columnspan=2, padx=5, pady=5, sticky='w')

        self._screenBox.configure(value=sorted(self._screenList.keys()))
        self._screenBox.bind("<<ComboboxSelected>>", changeIndexBox)

        # Draw Save and Cancel button
        self.saveBtn = ttk.Button(self._indexMenu, text='Save', command=lambda: self.saveImg(img, self._screenBox.get(), self._indexBox.get()))
        self.cancelBtn = ttk.Button(self._indexMenu, text='Cancel', command=self.returnToToolbar)

        self.saveBtn.grid(column=1, row=2, sticky='e')
        self.cancelBtn.grid(column=2, row=2)

        # Grayscaled captured background        
        ttk.Label(self._indexMenu, borderwidth=4, image=self._capturedImg, relief='groove').grid(row=3, columnspan=3, padx=5, pady=5)

       
        
def main():
    root = Tk()
    root.geometry(str(app_width) + "x" + str(app_height))
    
    app = MyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
