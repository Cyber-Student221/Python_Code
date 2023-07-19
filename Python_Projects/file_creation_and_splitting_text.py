# Author: Yasmeen Ghanim
# Last Modified: 04/04/2023
"""Description:
This code is a Python script that takes user input for a novel and creates multiple text files, 
one for each chapter, prologue, epilogue, and any side stories. The input is processed and split into paragraphs of a specified chunk size (number of words per paragraph). 
The text files are saved in a directory named after the novel's title."""

import os

def process_input_and_split_into_chunks(chunk_size):
    input_str = ""
    while True:
        line = input("Enter a line (or 'q' to quit): ").strip()
        if line == 'q':
            break
        input_str += line + ' '

    # Split the input string into a list of individual words
    word_list = input_str.split()

    # Create empty lists for paragraphs and the current paragraph being constructed
    paragraphs = []
    paragraph = []

    # Initialize the index of the current word being processed
    word_index = 0

    # Loop through each word in the list
    while word_index < len(word_list):
        # Get the current word
        word = word_list[word_index]

        # If the paragraph is empty, add the word to it
        if not paragraph:
            paragraph.append(word)

        # If the word ends with a question mark and is the last word in the chunk, start a new paragraph with the word
        elif (word.endswith("？") or word.endswith("?")) and len(paragraph) == chunk_size - 1:
            paragraphs.append(" ".join(paragraph))
            paragraph = [word]

        # If the word does not end with a question mark, add it to the paragraph if there is space or start a new paragraph
        else:
            if len(paragraph) < chunk_size:
                paragraph.append(word)
            else:
                paragraphs.append(" ".join(paragraph))
                paragraph = [word]

        word_index += 1

        # If the current paragraph is full, add it to the list of paragraphs and start a new paragraph
        if len(paragraph) == chunk_size:
            paragraphs.append(" ".join(paragraph))
            paragraph = []

    # If there are any remaining words in the final paragraph, add it to the list of paragraphs
    if paragraph:
        paragraphs.append(" ".join(paragraph))

    # Print the number of chunks/paragraphs
    print(f"The input has been split into {len(paragraphs)} paragraphs.")
    # Return the list of paragraphs
    return paragraphs


def create_novel_chapters(chunk_size):
    while True:
        try:
            title_untouched = input("Enter the title of the novel: ")
            title = title_untouched.replace('"', '')
            # Remove unwanted characters from the title
            for c in ['*', '.', '"', '/', '\\', '[', ']', ':', ';', '|', ',','?','@','!','#']:
                title = title.replace(c, '')
                
            directory = title
            # Create the directory if it doesn't exist
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Changing the current directory to the newly created one
            os.chdir(directory)
            break
        except FileNotFoundError:
            print("Invalid Input - Too Many Characters")

    starting_chapter = 1
    for filename in sorted(os.listdir()):
        if filename.startswith("Chapter"):
            starting_chapter += 1

    while True:
        try:
            chapter_number = int(input(f"Enter the total number of chapters (starting from {starting_chapter}): "))
            # Create a text file for each chapter in the specified directory
            for i in range(starting_chapter, chapter_number+1):
                paragraphs = process_input_and_split_into_chunks(chunk_size)
                filename = f"Chapter {i}.txt"
                with open(filename, "a", encoding='utf-8') as file:
                    file.write(f"{title_untouched} - Chapter {i} \n")
                    for paragraph in paragraphs:
                        file.write("Translate the following into english:\n" + paragraph + '\n\n')
            break
        except ValueError:
            print("Invalid input! Please enter a valid integer for number of chapters.")       
    while True:
        try:
            # Ask if there is an epilogue
            epilogue = input("Does the novel have an epilogue? (y/n): ")
            if epilogue.lower() not in ['y','n']:
                raise Exception
            if epilogue.lower() == 'y':
                with open("Epilogue.txt", "a", encoding='utf-8') as file:
                    file.write(f"{title_untouched} - Epilogue \n")
                    paragraphs = process_input_and_split_into_chunks(chunk_size)
                    for paragraph in paragraphs:
                        file.write("Translate the following into english:\n" + paragraph + '\n\n')
            break
        except:
            print("Invalid Input - Please enter y or n")

    while True:
        try:
            # Ask if there is a prologue
            prologue = input("Does the novel have a prologue? (y/n): ")
            if prologue.lower() not in ['y','n']:
                raise Exception
            if prologue.lower() == 'y':
                with open("Prologue.txt", "a", encoding='utf-8') as file:
                    file.write(f"{title_untouched} - Prologue \n")
                    paragraphs = process_input_and_split_into_chunks(chunk_size)
                    for paragraph in paragraphs:
                        file.write("Translate the following into english:\n" + paragraph + '\n\n')
            break
        except:
            print("Invalid Input - Please enter y or n")
            
    while True:
        try:
            side_stories = input("Does the novel have side stories? (y/n): ")
            if side_stories.lower() not in ['y','n']:
                raise Exception
            break
        except:
            print("Invalid Input - Please enter y or n")

    while True:
        try:
            if side_stories.lower() == 'y':
                # Ask for the number of side stories
                num_side_stories = int(input("Enter the number of side stories: "))
                for i in range(1, num_side_stories+1):
                    with open(f"Side Story {i}.txt", "a", encoding='utf-8') as file:
                        file.write(f"{title_untouched} - Side Story {i}\n")
                        paragraphs = process_input_and_split_into_chunks(chunk_size)
                        for paragraph in paragraphs:
                            file.write("Translate the following into english:\n" + paragraph + '\n\n')
            break
        except:
            print("Invalid Input - Please enter a valid integer for number of side stories.")

def main():
    chunk_size = 20
    create_novel_chapters(chunk_size)
if __name__ == '__main__':
    main()