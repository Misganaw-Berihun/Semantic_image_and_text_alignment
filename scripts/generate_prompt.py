from openai import OpenAI
client = OpenAI(
  api_key="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"
)

system_prompt = """
        Assume you are an expert prompt engineer. I will give you a 
        description of an image and you will write me a prompt based 
        on the following format: 
            
            Format : 'subject + style + details + format of output'.
        
        You will add this details by yourself. This is an example prompt 
            Example: 'Draw a ginger-and-white striped cat looking excited 
                      as it chases a mouse around a kitchen, in the style 
                      of an impressionist painter, with light streaming 
                      through the windows and prominent use of blue and yellow.
                      The output of the image has an aspect ratio of 1 : 1 and 
                      the image is used for social media post.'
        This is the kind of image I want you to generate.
"""

response = client.chat.completions.create(
  model="gpt-3.5-turbo-0125",
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "A suspenseful animation of a LEGO CITY set, with buildings, vehicles, and mini-figures coming to life in a dynamic, 3D environment. The animation is designed to captivate the viewer's attention and set the stage for the upcoming challenge."}
  ]
)
print(response.choices[0].message.content)