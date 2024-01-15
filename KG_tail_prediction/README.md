This folder is used for tail entity inference in the product reasoning module. 
- In the 'data' folder
  - The "E&R" folder contains entity and relationship files, the "Entity_linking" folder contains entity linking files
  - The "relations_for_different_category" folder contains category files for different products
  - The "triples" folder contains knowledge triple files used for training
- Under the "model" directory, the trained inference model is stored. In this case, it is the TuckER model
- The "Tail_prediction" file performs inference on the products for each dialogue and stores the results in a file.
