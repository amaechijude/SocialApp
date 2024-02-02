from pathlib import Path

def rename_text(file_name, s_word, new_word):
    try:
        #file name
        file = Path(file_name)
        #Convert both the old and new words into lists
        word_list = s_word.split(",")
        new_word_list = new_word.split(",")
        #Loop through the list and replace them
        for i in range(len(word_list)):
            data = file.read_text()
            data = data.replace(word_list[i], new_word_list[i])
            #Save the new text
            file.write_text(data)
        return f"{s_word} is succesfully renamed to {new_word}"
    except FileNotFoundError:
        return "file name error"


x = input("Enter file name: ")
y = input("Enter words to be renamed seperated by ',': ")
z = input("Enter new words for the above accordignly: ")

output = rename_text(x,y,z)
print(output)