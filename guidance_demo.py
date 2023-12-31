import guidance

# set the default language model used to execute guidance programs
guidance.llm = guidance.llms.OpenAI("text-davinci-003")

# define the few shot examples
examples = [
    {'input': 'I wrote about shakespeare',
     'entities': [{'entity': 'I', 'time': 'present'}, {'entity': 'Shakespeare', 'time': '16th century'}],
     'reasoning': 'I can write about Shakespeare because he lived in the past with respect to me.',
     'answer': 'No'},
    {'input': 'Shakespeare wrote about me',
     'entities': [{'entity': 'Shakespeare', 'time': '16th century'}, {'entity': 'I', 'time': 'present'}],
     'reasoning': 'Shakespeare cannot have written about me, because he died before I was born',
     'answer': 'Yes'}
]

# define the guidance program
structure_program = guidance(
    '''Given a sentence tell me whether it contains an anachronism (i.e. whether it could have happened or not based on the time periods associated with the entities).
    ----
    
    {{~! display the few-shot examples ~}}
    {{~#each examples}}
    Sentence: {{this.input}}
    Entities and dates:{{#each this.entities}}
    {{this.entity}}: {{this.time}}{{/each}}
    Reasoning: {{this.reasoning}}
    Anachronism: {{this.answer}}
    ---
    {{~/each}}
    
    {{~! place the real question at the end }}
    Sentence: {{input}}
    Entities and dates:
    {{gen "entities"}}
    Reasoning:{{gen "reasoning"}}
    Anachronism:{{#select "answer"}} Yes{{or}} No{{/select}}''')

# execute the program
out = structure_program(
    examples=examples,
    # input='The T-rex bit my dog'
    input=''
)
print(out)
