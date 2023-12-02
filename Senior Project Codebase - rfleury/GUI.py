#Ryan Fleury
#Lawrence Tech University
#Senior Project Summer 2022
#Emotion Predictive Text Editor
#"I have neither given nor received unauthorized aid in completing this 
# work, nor have I presented someone else's work as my own."

from tkinter import *
from tkinter.tix import *
from tkinter import filedialog
#import text2emotion as te
#import nltk
from textblob import TextBlob
from APIRequests import GenFile
import docx
#import threading
from emotion import buildKernal
from consts import FEATURE_NUMBER
from consts import init
import consts

#possile filetypes that can be opened with the program
filetypes = (
        ('text files', '*.txt'),
        ('Word Document', '*.docx'),
)
#print(type(filetypes))

def open_txt(): #function to open a text file or word file
  
    File = filedialog.askopenfilename(initialdir = "D:\vsCode\Code", title = "Open Files", filetypes = filetypes ) 
    
    try: #opening a text file
        textFile = open(File, 'r')
        data = textFile.read()
        my_text.insert(END, data)
        textFile.close()
    except: #opening a word file
        textFile = docx.Document(File)
        data = textFile.paragraphs
        for para in data:
            my_text.insert(END, para.text + "\n")


def save_txt(): #function to save progress to a file
    textFile = filedialog.asksaveasfilename(initialdir = "D:\vsCode\Code", title = "Open Text File", filetypes = filetypes )
    textFile = open(textFile, 'w')
    textFile.write(my_text.get(1.0, END))
    textFile.close()


def analize_text(): #create analize_text() function
    try:
        #--------------------sediment gathering and processing--------------------
        #=========================================================================================================================================================
        #get text from tkinter class
        roughSediment = my_text.get("1.0", END)
        #print(roughSediment)

        #-----break responce characters into list of words
        wordSediment = convert(roughSediment)
        #print("printing word level")
        #print(wordSediment)

        #consts.redditBool = True
        #remove first instance on reddit pull
        if (consts.redditBool == True):
            wordSediment.pop(0)#delete "body," text that every redit pull has for 1st word
        
        #-----breaks responce into sentence level
        sentSediment = sentenceStruct(wordSediment)
        #print("print sentence sediment")
        #print(sentSediment)
            
        if (consts.redditBool == True):
            #remove all entries that were less than two characters in length
            sentSediment = [x for x in sentSediment if len(x) >= 2]
            #removes numbers from reddit pull
            sentSediment = list(map(lambda x: x.replace("0,",'').replace("1,",'').replace("2,",'').replace("3,",'').replace("4,",'').replace("5,",'').replace("6,",'').replace("7,",'').replace("8,",'').replace("9,",'').replace("10,",''),sentSediment))

        #-----breaks responce into paragraph
        fullSediment = fullStructure(sentSediment)
        #print("aftwe full structure")
        #print(fullSediment)

        #-----cleans the gathered sedinent
        # finalSediment = listClense(sentSediment)
        # print("after list clense")
        # print(finalSediment)
        #=========================================================================================================================================================



        # #--------------------Texb Blob documnet scoring--------------------
        # #=========================================================================================================================================================
        blob_text = TextBlob(fullSediment)
        #tags = blob_text.tags
        #print("Textblob tags")
        #print(tags)

        #polarity of the sediment (1 for negative 1 for positive)
        #sentiment = blob_text.sentiment 
        #print(sentiment)

        polarity = blob_text.polarity
        #print("Documnet polarity")
        #print(polarity)

        subjectivity = blob_text.subjectivity
        #print("Documnet subjectivity")
        #print(subjectivity)

        #semtence level postitive and negative feedback https://hackernoon.com/how-to-perform-emotion-detection-in-text-via-python-lk383tsu
        positive_feedbacks = []
        negative_feedbacks = []
        for feedback in sentSediment:
            feedback_polarity = TextBlob(feedback).sentiment.polarity
            if feedback_polarity>0:
                positive_feedbacks.append(feedback)
                continue
            negative_feedbacks.append(feedback)
    
        # print('Positive_feebacks Count : {}'.format(len(positive_feedbacks)))
        # #print(positive_feedbacks)
        # print('Negative_feedback Count : {}'.format(len(negative_feedbacks)))
        # # print(negative_feedbacks)

        polarity  = round(polarity, 5)
        subjectivity  = round(subjectivity, 5)
        stringNegative = 'Negative Feedbacks: ' + str(len(negative_feedbacks))
        stringPositive = 'Positive Feedbacks: ' + str(len(positive_feedbacks))
        stringPolarity = 'Polarity: ' + str(polarity)
        stringSubjectivity = 'Subjectivity: ' + str(subjectivity)

        #overwrite the labels for some document grading
        negativeLabel = Label(
        text=stringPositive,
        bg='#f0f0f0',
        font=(30)
        )
        negativeLabel.place(x = 1600, y =(52 + 260))

        positiveLabel = Label(
        text=stringNegative,
        bg='#f0f0f0',
        font=(30)
        )
        positiveLabel.place(x = 1600, y = (52 + 290))

        polarityLabel = Label(
        text=stringPolarity,
        bg='#f0f0f0',
        font=(30)
        )
        polarityLabel.place(x = 1600, y = (52 + 320))

        subjectivityLabel = Label(
        text=stringSubjectivity,
        bg='#f0f0f0',
        font=(30)
        )
        subjectivityLabel.place(x = 1600, y = (52 + 350))
        # #=========================================================================================================================================================



        # #--------------------text to emotion library-------------------- 
        # #=========================================================================================================================================================
        # textToEmotionVar = te.get_emotion(fullSediment)
        # print(textToEmotionVar)
            #NOT USED CURRENTLY BECAUSE OF COMPUTATION ISSUES
        # #=========================================================================================================================================================

    

        # #--------------------SVM cutom emotion grading-------------------- 
        # #=========================================================================================================================================================
        #Generate the SVM kernal
        clf = buildKernal()
        testVect = transformData(sentSediment)   
        prediction = clf.predict(testVect)

        #prediction = clf.predict(testVect)
        #print(prediction)
        # #=========================================================================================================================================================
        


        # #--------------------clears the text box to place in text with highlights and preprocessing-------------------- 
        # #=========================================================================================================================================================
        def clear_frame():
            my_text.delete('1.0', END)

        clear_frame()
        # #=========================================================================================================================================================



        # #--------------------rewrite the text to the screen with highlights-------------------- 
        # #=========================================================================================================================================================
        def write_frame():
            #create text tags based on emotion
            my_text.tag_config("neutral", background= "white", foreground= "black")
            my_text.tag_config("non-neutral", background= "gray", foreground= "black")
            my_text.tag_config("fear", background= "pale violet red", foreground= "black")
            my_text.tag_config("disgust", background= "green yellow", foreground= "black")
            my_text.tag_config("surprise", background= "gold", foreground= "black")
            my_text.tag_config("joy", background= "spring green", foreground= "black")
            my_text.tag_config("anger", background= "maroon", foreground= "black")

            #sentSediment[ins] + "\n" to break higlights apart with a endline
            ins = 0
            for entry in prediction:
                if(entry == "neutral"):
                    my_text.insert(INSERT, sentSediment[ins] ,("neutral"),)
                elif(entry == "non-neutral"):
                    my_text.insert(INSERT, sentSediment[ins] ,("non-neutral"),)
                elif(entry == "fear"):
                    my_text.insert(INSERT, sentSediment[ins] ,("fear"),)
                elif(entry == "disgust"):
                    my_text.insert(INSERT, sentSediment[ins] ,("disgust"),)
                elif(entry == "surprise"):
                    my_text.insert(INSERT, sentSediment[ins] ,("surprise"),)
                elif(entry == "joy"):
                    my_text.insert(INSERT, sentSediment[ins] ,("joy"),)
                elif(entry == "anger"):
                    my_text.insert(INSERT, sentSediment[ins] ,("anger"),)
                else:
                    my_text.insert(INSERT, sentSediment[ins] )
                    
                ins = ins +1

        write_frame()#function call to write to the frame with text tags

        #label to show text has been analized
        exceptionNotThrown = Label(root,
        text="Text has been analized, see legend to detremine prediction.", bg='#f0f0f0',
        font=(30))
        exceptionNotThrown.place(x = 1010, y = 23)
        # #=========================================================================================================================================================
    except:
        #exception will be thrown if there is not enough input text present for the program
        exceptionThrown = Label(root,
        text="ERROR: More input text is needed to analize for emotion!  ", bg='#f0f0f0',
        font=(30))
        exceptionThrown.place(x = 1010, y = 23)
        


#Extract the TfidfVectorizer features from the text that is in the text box
def transformData(sentenceData):
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorBoi = TfidfVectorizer(max_features=FEATURE_NUMBER, stop_words= "english")
        trainVext = vectorBoi.fit_transform(sentenceData) #transforming of training sentences
        return trainVext



#convert from list of string characters to list of words
def convert(s):
    # initialization of string to ""
    new = ""
    myList = []
    # traverse in the string 
    var = 0
    for x in s:
        if(s[var] == " " or s[var] == "\n"):
            myList.append(new)
            #print(new)
            new = ""
        new = new + x 
        var = var + 1; 
    # return string 
    return myList


#convert from list of words to list of sentences
def sentenceStruct(list):
    new = ""
    list2 = []
    for word in list:
        #print(word)
        if "." in word or "!" in word or "?" in word:
             new = new + word
             list2.append(new)
             new = "" 
        elif "\n" in word:
             list2.append(new)
             new = "" 
             word = word.replace("\n", "")
             new = new + word
        else:
            new = new + word

    list2.append(new)
    return list2


#convert from list of sentences to a paragraph form. aka one big string.
def fullStructure(list): 
    # initialize an empty string
    str1 = " " 
    # return string
    return (str1.join(list))
        

#cleans a list of all \n characters    (CURRENTLY NOT USED)    
def listClense(list): 
    for x in list:
        if '\n' in x:
            x.replace("\n", "")


#change color of a button on hover: https://www.geeksforgeeks.org/tkinter-button-that-changes-its-properties-on-hover/
def changeOnHover(button, colorOnHover, colorOnLeave):
    #background on hover
    button.bind("<Enter>", func=lambda e: button.config(
        background=colorOnHover))
  
    # background color on leving widget
    button.bind("<Leave>", func=lambda e: button.config(
        background=colorOnLeave))


if __name__ == "__main__":  #main function

    init()#initilization function
    root = Tk() #tkinter object 
    root.title("Senior Project - Text Editor") #title of the window
    root.geometry("1920x1080")#size of window        
    tip = Balloon(root)

    #top button 1
    openTextButton = Button(root, text = "Open Text File", command = open_txt, background = "lightgray")
    openTextButton.place(x=0, y=0)
    #tip.bind_widget(openTextButton,balloonmsg="Open a text(.txt) or word(.docx) file.")
    changeOnHover(openTextButton, "lightblue", "lightgray")
    # openTextButton.grid(row=1,column=0)

    #top button 2
    openSaveButton = Button(root, text = "Save File", command = save_txt, background = "lightgray")
    openSaveButton.place(x=86, y=0)
    #tip.bind_widget(openSaveButton,balloonmsg="Save content to a text file.")
    changeOnHover(openSaveButton, "lightblue", "lightgray")
    # openSaveButton.grid(row=1,column=2)

    #top button 3
    RedditPullButton = Button(root, text = "Pull Reddit File", command = GenFile, background = "lightgray")
    RedditPullButton.place(x=142, y=0)
    #tip.bind_widget(RedditPullButton,balloonmsg="Pull data from Reddit. Will be stored in a text file in the local directory.")
    changeOnHover(RedditPullButton, "lightblue", "lightgray")
    # RedditPullButton.grid(row=1,column=4)

    #top button 4
    analyzeButton = Button(root, text = "Analyze", command = analize_text, background = "lightgray")
    analyzeButton.place(x=231, y=0)
    #tip.bind_widget(analyzeButton,balloonmsg="Analize text for emotion if there is enough input text present.")
    changeOnHover(analyzeButton, "lightblue", "lightgray")
    # analyzeButton.grid(row=1,column=3)

    #label for the text editor box
    frame = Label(
        text='Text Editor - Write Text or Open file for tone/emotion analysis',
        bg='#f0f0f0',
        font=(30)
    )
    frame.place(x = 70, y = 26)#place text box frame

    
    #create text editing box
    my_text = Text(root, width = 112, height= 35, font = ("Helventica", 18))
    my_text.place(x=70, y=52) #pady == vert didtance between elements
    #print(type(my_text))
    

    #add a scrollbar to text editing box
    scrollbar = Scrollbar(root)
    scrollbar.pack( side = RIGHT, fill = Y )
    scrollbar.config( command = my_text.yview )


    #A table that contains the emotion color grading legend
    #==================================================================================================================
    fontSize =  30
    legend = Label(root,
    text="         Legend         ",
     fg= "black",font=(fontSize))
    legend.place(x = 1600, y = 52)
   
    fearLabel = Label(root,
    text="  Fear is Pink   ",
    bg= "pale violet red", fg= "black",font=(fontSize))
    fearLabel.place(x = 1600, y = (52 + 30))
    
    surpriseLabel = Label(root,
    text="  Suprise is gold  ",
    bg= "gold", fg= "black",font=(fontSize))
    surpriseLabel.place(x = 1600, y = (52 + 60))

    neutraLabel = Label(root,
    text="  Neutral is White  ",
    bg= "white", fg= "black",font=(fontSize))
    neutraLabel.place(x = 1600, y = (52 + 90))

    angerLabel = Label(root,
    text= "  Anger is maroon  ",
    bg= "maroon", fg= "white",font=(30))
    angerLabel.place(x = 1600, y =(52 + 120))

    joyLabel = Label(root,
    text="  Joy is spring green  ",
    bg= "spring green", fg= "black",font=(fontSize))
    joyLabel.place(x = 1600, y = (52 + 150))

    nonNeutralLabel = Label(root,
    text="  Non-Neutral is Gray  ",
    bg= "gray", fg= "black",font=(fontSize))
    nonNeutralLabel.place(x = 1600, y = (52 + 180))

    disgustllLabel = Label(root,
    text="  Disgust is green yellow  ",
    bg= "green yellow", fg= "black",font=(fontSize))
    disgustllLabel.place(x = 1600, y = (52 + 210))
    #==================================================================================================================


    #placeholder labels string
    stringNegative = 'Negative Feedbacks: 0' 
    stringPositive = 'Positive Feedbacks: 0' 
    stringPolarity = 'Polarity: 0' 
    stringSubjectivity = 'Subjectivity: 0'

    #placeholder labels apended to GUI
    negativeLabel = Label(
    text=stringPositive,
    bg='#f0f0f0',
    font=(30)
    )
    negativeLabel.place(x = 1600, y =(52 + 260))

    positiveLabel = Label(
    text=stringNegative,
    bg='#f0f0f0',
    font=(30)
    )
    positiveLabel.place(x = 1600, y = (52 + 290))

    polarityLabel = Label(
    text=stringPolarity,
    bg='#f0f0f0',
    font=(30)
    )
    polarityLabel.place(x = 1600, y = (52 + 320))

    subjectivityLabel = Label(
    text=stringSubjectivity,
    bg='#f0f0f0',
    font=(30)
    )
    subjectivityLabel.place(x = 1600, y = (52 + 350))

    root.mainloop() #call mainloop function to generate the tkinter GUI