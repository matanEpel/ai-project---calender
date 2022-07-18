from classify_assigments import NN

learning_model = NN()
if not learning_model.has_model():
    learning_model.train_and_evaluate()
while True:
    inp = input("Assignment:\n")
    if inp == 'quit':
        break
    classification = learning_model.classify(inp)
    if classification == 0:
        print("TASK")
    if classification == 1:
        print("MEETING")
    if classification == 2:
        print("MUST_BE_IN")
    print()