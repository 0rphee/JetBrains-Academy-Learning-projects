import requests
import argparse
from sys import exit
from bs4 import BeautifulSoup


# Returns the arguments
def process_args():
    parser = argparse.ArgumentParser()
    args = ["orig_lang", "target_lang", "word"]
    for arg in args:
        parser.add_argument(arg)
    return parser.parse_args()


def write_file(text: str, word: str):
    with open(f"{word}.txt", "a") as file:
        file.write(f"{text}\n")


def return_lang_or_exit(language):  # If an invalid language is entered, the program stops
    if language in Languages.lang_list:
        return [language]
    else:
        print(f"Sorry, the program doesn't support {language}")
        exit()


class Languages:
    lang_list = ["arabic", "german", "english", "spanish", "french", "hebrew", "japanese",
                 "dutch", "polish", "portuguese", "romanian", "russian", "turkish"]

    def __init__(self):  # todo fix type differences
        args = process_args()
        self.orig_lang: str = return_lang_or_exit(args.orig_lang)[0]  # ej. "spanish" (lowercase)
        # ej. "english", IMPORTANT "all" (lowercase) // assigns the target lang or all the langs except the origin
        if args.target_lang != "all":
            self.targ_lang = return_lang_or_exit(args.target_lang)
        else:
            self.targ_lang = Languages.lang_list[:]
            self.targ_lang.remove(self.orig_lang)
        self.word_to_trans: str = args.word  # ej. "hola"

    def give_url(self) -> list:
        if type(self.targ_lang) is str:
            return [
                f"https://context.reverso.net/translation/{self.orig_lang.lower()}-{self.targ_lang.lower()}/{self.word_to_trans}"]
        else:
            return [f"https://context.reverso.net/translation/{self.orig_lang.lower()}-{target}/{self.word_to_trans}"
                    for target in self.targ_lang]


def main():
    # Prints the lists of both the translations and the examples
    def print_lists(li: list, translation_example: str, targ_lang: str, mult_langs: bool, word: str):
        example_title_ln = f"{targ_lang.capitalize()} {translation_example}:"
        print(example_title_ln)
        example_title_ln = example_title_ln if translation_example == "Translations" else "\n" + example_title_ln
        write_file(example_title_ln, word)
        if translation_example == "Translations":
            for i in li:
                print(i)
                write_file(i, word)
                if mult_langs:
                    break
            print()
        else:
            for orig, trans in zip(li[::2], li[1::2]):
                line = f"{orig}\n{trans}\n"  # Formatted line for printing and writing
                print(line)
                write_file(line, word)
                if mult_langs:
                    break

    def search_trans(url: list, targ_langs: list, word: str):
        mult_langs = True if len(targ_langs) > 1 else False
        for i, targ_lang in zip(url, targ_langs):
            r = requests.get(i, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 404:
                print(f"Sorry, unable to find {word}")
                exit()
            elif r.status_code != 200:
                print("Something wrong with your internet connection")
                exit()
            else:
                # TRANSLATIONS BEGIN
                soup = BeautifulSoup(r.content, "html.parser")
                # translated words are added to their list
                trans_tags = soup.find("div", id="translations-content")
                trans_list = [child.text.strip() for child in trans_tags.children if len(child.text.strip()) > 1]

                # example translations are added to their list
                example_tags = soup.find_all("div", {"class": "example"})
                examples_list = [subtag.text.strip() for tag in example_tags for subtag in
                                 tag.find_all("div", {"class": "ltr"})
                                 if len(subtag.text.strip()) > 1]  # strip and len()

                # FINAL PRINTING
                print_lists(trans_list, "Translations", targ_lang, mult_langs, word)
                print_lists(examples_list, "Examples", targ_lang, mult_langs, word)

    # PROPER FUNCTION EXECUTION BEGINS
    # Word and language settings
    languages = Languages()
    with open(f"{languages.word_to_trans}.txt", "w") as file:
        pass
    search_trans(languages.give_url(), languages.targ_lang, languages.word_to_trans)


if __name__ == "__main__":
    main()
