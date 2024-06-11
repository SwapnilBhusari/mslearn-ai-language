from dotenv import load_dotenv
import os

# Import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Create client using endpoint and keypython text-analysis.pypython text-analysis.py
        credential = AzureKeyCredential(ai_key)
        ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

        # Analyze each text file in the reviews folder
        reviews_folder = 'reviews'
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print('\n' + text)

            # Get language
            detectedLanguages = ai_client.detect_language(documents=[text])
            #print(type(detectedLanguages))
            #print(detectedLanguages)
            detectedLanguage = detectedLanguages[0]
            print('\nLanguage:{}'.format(detectedLanguage.primary_language.name))

            # Get sentiment
            sentimentAnalysisList = ai_client.analyze_sentiment(documents=[text])
            #print(sentimentAnalysisList)
            sentimentAnalysis = sentimentAnalysisList[0]
            print("\nSentiment:{}".format(sentimentAnalysis.sentiment))


            # Get key phrases
            phrasesList = ai_client.extract_key_phrases(documents=[text])
            #print(phrasesList)
            phrases = phrasesList[0].key_phrases 
            if len(phrases) > 0:
                print("\n Key Phrases:")
                for phrase in phrases:
                    print("\t{}".format(phrase))

            # Get entities
            entitiesList = ai_client.recognize_entities(documents=[text])
            #print(entitiesList)
            entities = entitiesList[0].entities
            if len(entities) > 0:
                print("\nEntities:")
                for entity in entities:
                    print('\t{} ({})'.format(entity.text, entity.category))

            # Get linked entities
            entitiesList = ai_client.recognize_linked_entities(documents=[text])
            #print(entitiesList)
            entities = entitiesList[0].entities
            if len(entities) > 0:
                print("\n Links:")
                for linked_entity in entities:
                    print('\t{} ({})'.format(linked_entity.name, linked_entity.url))

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()