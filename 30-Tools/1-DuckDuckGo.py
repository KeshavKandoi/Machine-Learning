# from langchain_community.tools import DuckDuckGoSearchRun

# search = DuckDuckGoSearchRun()

# kk=search.invoke("compliance automation")
# print(kk)



from langchain_community.tools import DuckDuckGoSearchResults

search = DuckDuckGoSearchResults(output_format="list")

kk=search.invoke("Obama")
print(kk)