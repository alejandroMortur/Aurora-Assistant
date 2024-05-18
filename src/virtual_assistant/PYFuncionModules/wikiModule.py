import wikipedia

def wiki_search(input, language, Nsentences):
    """
    Function to search for a summary on Wikipedia.

    Parameters:
    - input (str): The search query.
    - language (str): The language code for the Wikipedia language edition (e.g., 'en' for English, 'es' for Spanish).
    - Nsentences (int): The number of sentences to include in the summary.

    Returns:
    - wiki (str): The summary text retrieved from Wikipedia.
    """
    
    # Set the language for the Wikipedia search
    wikipedia.set_lang(language)

    # Get the summary from Wikipedia
    wiki = wikipedia.summary(input, Nsentences)

    # Print the input query and the summary
    print(input + ": " + wiki)

    return wiki
