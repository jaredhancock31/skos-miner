import logging
import rdflib
import skos

filename = "pp_project_manuterms.rdf"
infile = open(filename)

# xml_data = infile.read()
# g = rdflib.Graph()
# result = g.parse(data=xml_data, format="application/rdf+xml")


g = rdflib.Graph()
result = g.parse(location=filename, format="application/rdf+xml")

loader = skos.RDFLoader(g)
print loader.keys()
