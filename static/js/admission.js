// Phone number validation for maximum 10 digits
function validateField(fieldName) {
    const fieldInput = document.getElementById(fieldName);
    const errorElement = document.getElementById(`${fieldName}Error`);
    
    // Clear previous error message
    errorElement.textContent = "";

    // Phone number validation for maximum 10 digits
    if (fieldName === 'phone') {
        const phoneValue = fieldInput.value.replace(/\D/g, ''); // Remove non-digit characters
        if (phoneValue.length > 10) {
            errorElement.textContent = "Phone number cannot exceed 10 digits.";
            return;
        }
    }

// Send AJAX request for other validation (like email or phone duplication)
    fetch(`/validate-field/?field_name=${fieldName}&field_value=${fieldInput.value}`)
        .then(response => response.json())
        .then(data => {
            if (!data.is_valid) {
                errorElement.textContent = data.error; // Display error message
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// DOB
document.getElementById('dob').addEventListener('input', function() {
    let dob = this.value;
    let errorMessage = document.getElementById('dobError');
    if (dob) {
        let dobDate = new Date(dob);
        let today = new Date();
        let age = today.getFullYear() - dobDate.getFullYear();
        let monthDifference = today.getMonth() - dobDate.getMonth();

        // Adjust age calculation if the birthdate hasn't occurred yet this year
        if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < dobDate.getDate())) {
            age--;
        }

        // Check if the user is under 18 years old
        if (age < 18) {
            errorMessage.textContent = "You must be at least 18 years old to apply.";
        } else {
            errorMessage.textContent = "";
        }
    }
});

// Address
document.getElementById('address').addEventListener('input', function() {
    let address = this.value;
    let errorMessage = document.getElementById('addressError');
    
    // Split the address into words and check if there are at least 2 words
    let words = address.trim().split(/\s+/);
    
    if (words.length < 2) {
        errorMessage.textContent = "Address must contain at least 2 words.";
    } else {
        errorMessage.textContent = "";
    }
});

// CHATBOT
// Function to open the chat popup
function openChat() {
    const chatPopup = document.getElementById('chatPopup');
    chatPopup.classList.add('show'); // Show the chat popup by adding the 'show' class
}

// Function to close the chat popup
function closeChat() {
    const chatPopup = document.getElementById('chatPopup');
    chatPopup.classList.remove('show'); // Hide the chat popup by removing the 'show' class
}

// Function to send a message from the user
function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    if (userInput.trim() === '') return; // Don't send empty messages

    // Display the user's message in the chat
    const chatBody = document.getElementById('chatBody');
    const userMessage = document.createElement('div');
    userMessage.classList.add('chat-message', 'user-message');
    userMessage.textContent = userInput;
    chatBody.appendChild(userMessage);

    // Scroll to the bottom of the chat
    chatBody.scrollTop = chatBody.scrollHeight;

    // Clear the input field
    document.getElementById('userInput').value = '';

    // Respond with a bot message (this is just an example, you can modify it)
    setTimeout(function() {
        const botResponse = getBotResponse(userInput); // Get bot's response based on user input

        // Display the bot's message
        const botMessage = document.createElement('div');
        botMessage.classList.add('chat-message', 'bot-message');
        botMessage.textContent = botResponse;
        chatBody.appendChild(botMessage);

        // Scroll to the bottom of the chat
        chatBody.scrollTop = chatBody.scrollHeight;
    }, 1000); // Simulate a slight delay for the bot response
}

// Function to get the bot's response based on user input
function getBotResponse(userMessage) {
    userMessage = userMessage.toLowerCase();

    // Predefined responses
    if (userMessage.includes('hi') || userMessage.includes('hello')) {
        return 'Hi there! How can I help you today?';
    }
    if (userMessage.includes('hey')) {
        return 'Hey! Need help with anything related to admissions or courses?';
    }
    if (userMessage.includes('admission')) {
        return 'Admissions are open! Please fill out the form on this page to apply.';
    }
    if (userMessage.includes('application')) {
        return 'You can apply online through our Admissions Portal. Let me know if you need guidance.';
    }
    if (userMessage.includes('status')) {
        return 'You can check your application status in the "Application Status" section.';
    }
    if (userMessage.includes('courses')) {
        return 'We offer a wide range of programs, including Computer Science, Electronics, Mechanical, and Civil.';
    }
    if (userMessage.includes('fees')) {
        return 'Our fee structure varies by program. Check the Admissions page for details.';
    }
    if (userMessage.includes('scholarships')) {
        return 'We offer scholarships for meritorious and financially challenged students.';
    }
    if (userMessage.includes('help')) {
        return 'Sure! How can I assist you further?';
    }
    if (userMessage.includes('placement')) {
        return 'Our placement cell ensures that students are industry-ready with training and internship opportunities.';
    }
    if (userMessage.includes('hostel')) {
        return 'Hostel accommodations are available for boys and girls with comfortable living spaces and security.';
    }
    if (userMessage.includes('campus')) {
        return 'Our campus includes modern labs, libraries, sports facilities, and vibrant student activities.';
    }
    if (userMessage.includes('contact')) {
        return 'Reach us at info@royalcollege.edu or call us at +1 234 567 890.';
    }
    if (userMessage.includes('library')) {
        return 'Our library houses thousands of books, journals, and digital resources to support your learning.';
    }
    if (userMessage.includes('events')) {
        return 'We host frequent cultural and academic events to enrich your college experience.';
    }
    if (userMessage.includes('documents')) {
        return 'You\'ll need academic certificates, ID proof, and a passport-sized photo for admission.';
    }

    return "I'm sorry, I didn't understand that. Please try asking differently.";
}

// Listen for the send button click event
document.getElementById('sendButton').addEventListener('click', function () {
    sendMessage(); // Trigger sending message
});

// Listen for the Enter key press to send the message
document.getElementById('userInput').addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        sendMessage(); // Trigger sending message
    }
});

function openChat() {
    document.getElementById('chatPopup').style.display = 'block';
}

function closeChat() {
    document.getElementById('chatPopup').style.display = 'none';
}

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

