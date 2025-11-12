document.addEventListener("DOMContentLoaded", () => {
    const chatWindow = document.getElementById("chat-window");
    const chatInput = document.getElementById("chat-input");
    const submitBtn = document.getElementById("chat-submit-btn");

    // 'csrftoken' is loaded from auth.js, which is included in the HTML
    if (typeof csrftoken === 'undefined') {
        console.error("CSRF token not found. Did you forget to include auth.js?");
    }

    const addMessage = (message, sender) => {
        const messageDiv = document.createElement("div");
        messageDiv.className = `chat-message ${sender}`;
        messageDiv.innerHTML = `<div class="chat-bubble">${message}</div>`;
        chatWindow.appendChild(messageDiv);
        // Auto-scroll to bottom
        chatWindow.scrollTop = chatWindow.scrollHeight;
    };

    const handleSendQuery = async () => {
        const query = chatInput.value.trim();
        if (query === "") return;

        // 1. Add user's message
        addMessage(query, "user");
        chatInput.value = "";
        submitBtn.disabled = true;

        // 2. Add a typing indicator
        addMessage("...", "bot");
        const typingIndicator = chatWindow.lastChild;

        try {
            // 3. Send query to the new backend API
            const response = await fetch("/tools/api/bot-query/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify({ query: query }),
            });

            if (!response.ok) {
                throw new Error("Network response was not ok.");
            }

            const data = await response.json();

            // 4. Replace "..." with the real answer
            typingIndicator.querySelector('.chat-bubble').innerHTML = data.answer;

        } catch (error) {
            console.error("Error:", error);
            typingIndicator.querySelector('.chat-bubble').innerHTML = "Sorry, I had trouble connecting. Please try again.";
        } finally {
            submitBtn.disabled = false;
            chatInput.focus();
        }
    };

    submitBtn.addEventListener("click", handleSendQuery);
    chatInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            handleSendQuery();
        }
    });
});
