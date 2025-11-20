document.addEventListener("DOMContentLoaded", () => {
    // --- Config for all our forms ---
    const formsConfig = {
        'report-form': {
            apiEndpoint: '/submit/api/report/',
            successMessage: 'Your report has been submitted anonymously. Your reference ID is: ',
        },
        'contact-form': {
            apiEndpoint: '/submit/api/contact/',
            successMessage: 'Your message has been sent successfully. We will get back to you soon.',
        }
    };

    // Find all forms on the page that match our config
    for (const formId in formsConfig) {
        const form = document.getElementById(formId);
        if (form) {
            setupFormListener(form, formsConfig[formId]);
        }
    }

    function setupFormListener(form, config) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const formStatus = form.querySelector('#form-status');
            const submitBtn = form.querySelector('#submit-btn');

            // Disable button and show loading
            if (submitBtn) submitBtn.disabled = true;
            if (formStatus) {
                formStatus.className = 'alert alert-info';
                formStatus.textContent = 'Submitting...';
            }

            // 1. Get Form Data
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            // We don't need to send the csrf token in the JSON body
            delete data.csrfmiddlewaretoken;

            try {
                // 2. Send to API
                const response = await fetch(config.apiEndpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken // This comes from auth.js
                    },
                    body: JSON.stringify(data)
                });

                if (!response.ok) {
                    // Get error details from server if possible
                    const errData = await response.json();
                    const errorMessages = Object.values(errData).join(', ');
                    throw new Error(errorMessages || `Server responded with status ${response.status}`);
                }

                const result = await response.json();

                // 3. Show Success
                if (formStatus) {
                    formStatus.className = 'alert alert-success';
                    let successText = config.successMessage;
                    if (result.id) {
                         successText += result.id;
                    }
                    formStatus.textContent = successText;
                }
                form.reset();

            } catch (error) {
                // 4. Show Error
                console.error('Submission Error:', error);
                if (formStatus) {
                    formStatus.className = 'alert alert-danger';
                    formStatus.textContent = `An error occurred: ${error.message}. Please check your inputs and try again.`;
                }
            } finally {
                // Re-enable button
                if (submitBtn) submitBtn.disabled = false;
            }
        });
    }
});
