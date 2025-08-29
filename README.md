This repository contains the official implementation of the paper:
To Know What User Concerns: Conceptual Knowledge Reasoning for User Satisfaction Estimation in E-Commerce Dialogue Systems

Our work proposes a novel Conceptual Knowledge Reasoning framework for User Satisfaction Estimation (USE) in E-Commerce dialogues. The model mimics human-like decision-making by first selecting crucial conceptual knowledge from a dialogue context and then performing deep reasoning over it to make an accurate satisfaction prediction.

🧠 Model Architecture Overview
The core of our model is a two-stage reasoning framework:

Knowledge Selection: Identifies and extracts the most relevant knowledge triplets from a Knowledge Graph (KG) that are pertinent to the user's core concerns in the dialogue.

Knowledge Reasoning (Tail Prediction): Reasons over the selected knowledge, predicting the implied conclusions or states (the missing tail entities), which reveal the underlying reasons for user satisfaction/dissatisfaction.

The final prediction is made by integrating the original dialogue context, the selected knowledge, and the reasoned new knowledge.
