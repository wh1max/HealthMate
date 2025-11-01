
document.addEventListener('DOMContentLoaded', () => {
    const symptomInput = document.getElementById('symptom-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const summaryBtn = document.getElementById('summary-btn');
    const emailInput = document.getElementById('email-input');

    const symptomSection = document.getElementById('symptom-section');
    const questionsSection = document.getElementById('questions-section');
    const summarySection = document.getElementById('summary-section');
    const loadingSpinner = document.getElementById('loading-spinner');

    const questionsList = document.getElementById('questions-list');
    const summaryOutput = document.getElementById('summary-output');

    let questionsData = [];

    analyzeBtn.addEventListener('click', async () => {
        const symptoms = symptomInput.value.trim();
        if (!symptoms) {
            alert('Please describe your symptoms.');
            return;
        }

        // Show spinner and hide other sections
        symptomSection.classList.add('hidden');
        loadingSpinner.classList.remove('hidden');

        try {
            const response = await fetch('http://localhost:5000/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ symptoms }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            questionsData = data.questions;
            displayQuestions(data.questions);

            // Hide spinner and show questions
            loadingSpinner.classList.add('hidden');
            questionsSection.classList.remove('hidden');

        } catch (error) {
            console.error('Error during analysis:', error);
            alert('Failed to analyze symptoms. Please try again.');
            // Restore initial view
            loadingSpinner.classList.add('hidden');
            symptomSection.classList.remove('hidden');
        }
    });

    summaryBtn.addEventListener('click', async () => {
        const email = emailInput.value.trim();
        if (!email || !validateEmail(email)) {
            alert('Please enter a valid email address.');
            return;
        }

        const answers = getAnswers();
        if (answers.length !== questionsData.length) {
            alert('Please answer all questions.');
            return;
        }

        // Show spinner
        questionsSection.classList.add('hidden');
        loadingSpinner.classList.remove('hidden');

        try {
            const response = await fetch('http://localhost:5000/summary', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    symptoms: symptomInput.value.trim(),
                    questions: questionsData,
                    answers: answers,
                    email: email,
                }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            summaryOutput.textContent = data.summary;

            // Hide spinner and show summary
            loadingSpinner.classList.add('hidden');
            summarySection.classList.remove('hidden');

        } catch (error) {
            console.error('Error getting summary:', error);
            alert('Failed to get summary. Please try again.');
            // Restore questions view
            loadingSpinner.classList.add('hidden');
            questionsSection.classList.remove('hidden');
        }
    });

    function displayQuestions(questions) {
        questionsList.innerHTML = '';
        questions.forEach((q, index) => {
            const questionEl = document.createElement('div');
            questionEl.className = 'question';
            questionEl.innerHTML = `
                <p>${q}</p>
                <div class="answers" data-question-index="${index}">
                    <button data-answer="yes">Yes</button>
                    <button data-answer="no">No</button>
                </div>
            `;
            questionsList.appendChild(questionEl);
        });

        // Add event listeners for the new answer buttons
        questionsList.querySelectorAll('.answers button').forEach(button => {
            button.addEventListener('click', (e) => {
                const parent = e.target.parentElement;
                // Remove 'selected' from sibling buttons
                parent.querySelectorAll('button').forEach(btn => btn.classList.remove('selected'));
                // Add 'selected' to the clicked button
                e.target.classList.add('selected');
            });
        });
    }

    function getAnswers() {
        const answers = [];
        questionsList.querySelectorAll('.answers').forEach(answerDiv => {
            const selectedButton = answerDiv.querySelector('button.selected');
            if (selectedButton) {
                answers.push(selectedButton.dataset.answer);
            }
        });
        return answers;
    }

    function validateEmail(email) {
        const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }
});
