import wikipedia

def search_wikipedia_summary(query, language,queue,num_sentences,):
    """
    Function to search for a summary on Wikipedia.

    Parameters:
    - query (str): The search query.
    - language (str): The language code for the Wikipedia language edition (e.g., 'en' for English, 'es' for Spanish). Default is English.
    - num_sentences (int): The number of sentences to include in the summary. Default is 2.

    Returns:
    - summary (str): The summary text retrieved from Wikipedia.
    """

    try:
        # Set the language for the Wikipedia search
        wikipedia.set_lang(language)

        # Get the summary from Wikipedia
        summary = wikipedia.summary(query, num_sentences)

        # Print the input query and the summary
        print(query + ": " + summary)

        return summary
    
    except wikipedia.exceptions.DisambiguationError as e:
        print("DisambiguationError: There are multiple possible pages. Please be more specific in your query.")
        queue.put("DisambiguationError: There are multiple possible pages. Please be more specific in your query.")
        
    except wikipedia.exceptions.PageError as e:
        print("PageError: The page does not exist. Please check your query.")
        queue.put("PageError: The page does not exist. Please check your query.")
        
    except wikipedia.exceptions.WikipediaException as e:
        print("WikipediaException: An unknown Wikipedia exception occurred.")
        queue.put("WikipediaException: An unknown Wikipedia exception occurred.")
    
    return None