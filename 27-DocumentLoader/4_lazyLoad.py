# Lazy Loading
# Lazy loading means loading data only when it's actually needed, instead of loading everything upfront.
# Normal Loading vs Lazy Loading
# Normal (Eager) Loading:
# Load all 100 PDFs → store in memory → then use them

# Everything loaded immediately
# Uses lots of memory upfront

# Lazy Loading:
# Just note that 100 PDFs exist → load each one only when accessed

# Nothing loaded until you actually need it
# Saves memory





from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader

loader=DirectoryLoader(
  path='books',
  glob='*.pdf',
  loader_cls=PyPDFLoader

)

docs=loader.lazy_load()

for document in docs:
  print(document.metadata)

