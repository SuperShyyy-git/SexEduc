from quizzes.models import Question, Answer

def create_answers():
    questions = Question.objects.all()
    print(f"Found {questions.count()} questions to populate.")
    
    # Generic but relevant answers
    answers_pool = [
        # Set 1
        [("Physical and emotional changes", True), ("Nothing happens", False), ("Everyone stays exactly the same", False), ("It only happens to adults", False)],
        # Set 2
        [("Mutual respect and communication", True), ("Keeping secrets", False), ("Controlling behavior", False), ("Ignoring boundaries", False)],
        # Set 3
        [("Enthusiastic, clear, and reversible", True), ("Implied by silence", False), ("Given under pressure", False), ("Once given, it cannot be taken back", False)]
    ]
    
    for i, q in enumerate(questions):
        # Use answers from pool if available, otherwise use a default set
        answers_data = answers_pool[i % len(answers_pool)]
        
        for text, is_correct in answers_data:
            Answer.objects.get_or_create(question=q, text=text, is_correct=is_correct)
        
        print(f"Populated Q{q.id}: {q.text[:30]}... with {q.answers.count()} answers.")

if __name__ == "__main__":
    create_answers()
