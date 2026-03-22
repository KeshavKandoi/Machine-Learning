from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

load_dotenv()


llm=HuggingFaceEndpoint(
     repo_id="Qwen/Qwen2.5-72B-Instruct", 
    task="text-generation"
)

model1=ChatHuggingFace(llm=llm)

model2 = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


prompt1=PromptTemplate(
  template='Generate short and simple notes from the following text\n{text}',
  input_variable=['text']
)

prompt2=PromptTemplate(
  template='Generate 5 short questions answer from the following text\n{text}',
  input_variable=['text']
)

prompt3=PromptTemplate(
  template='Merge the provided notes and quiz into a single document \n notes->{notes} and {quiz}',
  input_variables=['notes','quiz']
)


parser=StrOutputParser()

parallel_chain=RunnableParallel({
  'notes':prompt1|model1|parser,
  'quiz':prompt2|model2|parser
})


merge_chain=prompt3|model1|parser

chain=parallel_chain|merge_chain

text="""

Cricket is a bat-and-ball game that is played between two teams of eleven players on a field, at the centre of which is a 22-yard (20-metre; 66-foot) pitch with a wicket at each end, each comprising two bails (small sticks) balanced on three stumps. Two players from the batting team, the striker and nonstriker, stand in front of either wicket holding bats, while one player from the fielding team, the bowler, bowls the ball toward the striker's wicket from the opposite end of the pitch. The striker's goal is to hit the bowled ball with the bat and then switch places with the nonstriker, with the batting team scoring one run for each of these swaps. Runs are also scored when the ball reaches the boundary of the field or when the ball is bowled illegally.

The fielding team aims to prevent runs by dismissing batters (so they are "out"). Dismissal can occur in various ways, including being bowled (when the ball hits the striker's wicket and dislodges the bails), and by the fielding side either catching the ball after it is hit by the bat but before it hits the ground, or hitting a wicket with the ball before a batter can cross the crease line in front of the wicket. When ten batters have been dismissed, the innings (playing phase) ends and the teams swap roles. Forms of cricket range from traditional Test matches played over five days to the newer Twenty20 format (also known as T20), in which each team bats for a single innings of 20 overs (each "over" being a set of 6 fair opportunities for the batting team to score) and the game generally lasts three to four hours.

Traditionally, cricketers play in all-white kit, but in limited overs cricket, they wear club or team colours. In addition to the basic kit, some players wear protective gear to prevent injury caused by the ball, which is a hard, solid spheroid made of compressed leather with a slightly raised sewn seam enclosing a cork core layered with tightly wound string.

The earliest known definite reference to cricket is to it being played in South East England in the mid-16th century. It spread globally with the expansion of the British Empire, with the first international matches in the second half of the 19th century. The game's governing body is the International Cricket Council (ICC), which has over 100 members, twelve of which are full members who play Test matches. The game's rules, the Laws of Cricket, are maintained by Marylebone Cricket Club (MCC) in London. The sport is primarily played in India, Pakistan, Bangladesh, Sri Lanka, Afghanistan, Australia, New Zealand, England and Wales, South Africa and the West Indies.[2]

While cricket has traditionally been played largely by men, women's cricket has experienced significant growth in the 21st century.[3]

The most successful side playing international cricket is Australia, which has won eight One Day International trophies, including six World Cups, more than any other country, and has been the top-rated Test side more than any other country.[4][5]

"""

result=chain.invoke({'text':text})

print(result)

chain.get_graph().print_ascii()