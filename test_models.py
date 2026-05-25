import google.generativeai as genai

genai.configure(api_key="AIzaSyCsjuK6sY2GA8njZC1g18QJxgWEaTeJo6I")

models = genai.list_models()

for m in models:
    print(m.name)