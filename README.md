# Learning-English-advance-web-Software
A website that teaching English Vocabulary in smart ways,



## used Tools and techniques :
- Django framework.
- Sqlite database.
- HTML.
- JS.
- CSS.
- ChartJS.
- bootstrap.
- jquery.
- beautifulsoup4.
- googletrans.
- gTTS.
- requests.

## Development period: +4 months.

## The main pages and their functions:

### Add words page "/****"
The page responsible for adding words can be accessed by admin only

![التقاط الويب_29-4-2023_145158_127 0 0 1](https://user-images.githubusercontent.com/90055804/235303410-1cb6d45e-a451-4aa8-84ad-19c418950d34.jpeg)

#### How it works :
  - First: The admin enters the word in English.
  - Second: The word is translated into Arabic via the googletrans library.
  - Third: An audio pronunciation of the word is created and stored in an mp3 file using the gTTS library.
  - Fourth: Several sentences including the English word are fetched from websites that provide this service using web scraping technology (the program is for personal use only) through the requests library and the beautifulsoup4 library.
  - Fifth: Those sentences are translated into Arabic via the googletrans library and converted into an audio file using the gTTS library.
  - Sixth: The administrator determines the groups of words in which the word will be present, such as the group of words of countries or animals ..., the group of all and the group of the first letter of the word are automatically determined.
  - Finally: all that information and data get stored in the database, the process takes between 4-10s.

### Login "/login"
Login page

### learning "/learning"
The page where all groups of words are displayed to the user, contains features such as saving the groups that have been entered and defining custom groups that can only be accessed with a subscription paid by means of a gift card code
![التقاط الويب_29-4-2023_152934_127 0 0 1](https://user-images.githubusercontent.com/90055804/235305520-aa6e06cf-112f-4380-bdf9-f7feb9ed9cdb.jpeg)

### Word groub "/learning/<word_groub_name>"
The page that displays the words of one group, including the words that have been trespassed and can be marked as not traversed, and the words that are not trespassed and can be marked as trespassed, and detailed statistics on user performance.

![التقاط الويب_29-4-2023_153723_127 0 0 1](https://user-images.githubusercontent.com/90055804/235305911-9f61a402-fd85-4e44-8ae4-a1eee01a06c0.jpeg)

### Word "/learning/<word_groub_name>/<word>"
The page where the single word is displayed with options represented by random Arabic words, one of which represents the translation of the correct word. The sentences are located with their translation below and the ability to hear the word.

![التقاط الويب_29-4-2023_154447_127 0 0 1](https://user-images.githubusercontent.com/90055804/235306115-85f751d4-4088-44dd-b035-2ef8ff41a31b.jpeg)
