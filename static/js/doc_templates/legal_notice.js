// This file is dynamically loaded by doc_generator.js
// It defines a global function that builds the Legal Notice UI

function initializeTemplate() {
    const templateTitle = document.getElementById("template-title");
    const formContent = document.getElementById("form-content");
    const formFooter = document.getElementById("form-footer");
    const previewContent = document.getElementById("preview-content");

    // Set the title
    templateTitle.textContent = "Legal Notice Generator";

    // --- 1. Build the Form ---
    formContent.innerHTML = `
        <form id="legal-notice-form" class="form-grid">
            <div class="form-group">
                <label for="advocateName">Advocate's Name *</label>
                <input type="text" id="advocateName" name="advocateName" required>
            </div>
            <div class="form-group">
                <label for="clientName">Client's Name *</label>
                <input type="text" id="clientName" name="clientName" required>
            </div>
            <div class="form-group">
                <label for="opponentName">Opponent's Name *</label>
                <input type="text" id="opponentName" name="opponentName" required>
            </div>
            <div class="form-group">
                <label for="opponentAddress">Opponent's Address *</label>
                <textarea id="opponentAddress" name="opponentAddress" rows="3" required></textarea>
            </div>
            <div class="form-group full-span">
                <label for="noticeSubject">Subject of Notice *</label>
                <input type="text" id="noticeSubject" name="noticeSubject" required>
            </div>
            <div class="form-group full-span">
                <label for="noticeBody">Detailed Facts & Demands *</label>
                <textarea id="noticeBody" name="noticeBody" rows="8" placeholder="Enter the detailed facts, legal grounds, and demands..." required></textarea>
            </div>
            <div class="form-group">
                <label for="noticeDate">Date of Notice *</label>
                <input type="date" id="noticeDate" name="noticeDate" required>
            </div>
            <div class="form-group">
                <label for="compliancePeriod">Compliance Period (days)</label>
                <select id="compliancePeriod" name="compliancePeriod">
                    <option value="15">15 days</option>
                    <option value="30" selected>30 days</option>
                    <option value="60">60 days</option>
                </select>
            </div>
        </form>
        <p class="text-muted"><small>Your progress is saved in your browser automatically.</small></p>
    `;

    // --- 2. Build the Action Buttons ---
    formFooter.innerHTML = `
        <button id="download-pdf-btn" class="btn btn-primary">
            <i class="fas fa-download"></i> Download as PDF
        </button>
    `;

    // --- 3. Build the Preview ---
    previewContent.innerHTML = `
        <div id="preview-pane" class="doc-preview">
            <h4 class="preview-title">LEGAL NOTICE</h4>
            <hr>
            <p><strong>To:</strong></p>
            <p id="preview-opponentName">[Opponent's Name]</p>
            <p id="preview-opponentAddress" style="white-space: pre-wrap;">[Opponent's Address]</p>
            <br>
            <p><strong>Date:</strong> <span id="preview-noticeDate">[Date]</span></p>
            <br>
            <p><strong>Subject:</strong> <span id="preview-noticeSubject">[Subject of Notice]</span></p>
            <br>
            <p>Sir/Madam,</p>
            <p>Under the instructions of my client, <strong><span id="preview-clientName">[Client's Name]</span></strong>, I, <strong><span id="preview-advocateName">[Advocate's Name]</span></strong>, do hereby serve you with the following legal notice:</p>
            <div id="preview-noticeBody" style="white-space: pre-wrap; margin-top: 1rem; margin-bottom: 1rem;">
                [Detailed facts and demands will appear here...]
            </div>
            <p>You are hereby called upon to comply with the demands as stated above within a period of <strong><span id="preview-compliancePeriod">30</span> days</strong>, failing which my client shall be constrained to initiate appropriate legal proceedings against you.</p>
            <br>
            <p>Sincerely,</p>
            <p><strong><span id="preview-advocateName-2">[Advocate's Name]</span></strong></p>
        </div>
    `;

    // --- 4. Add Event Listeners ---
    const form = document.getElementById("legal-notice-form");
    const downloadBtn = document.getElementById("download-pdf-btn");

    const updatePreview = () => {
        // Get all form values
        const data = Object.fromEntries(new FormData(form).entries());

        // Update all preview fields
        document.getElementById('preview-opponentName').textContent = data.opponentName || "[Opponent's Name]";
        document.getElementById('preview-opponentAddress').textContent = data.opponentAddress || "[Opponent's Address]";
        document.getElementById('preview-noticeDate').textContent = data.noticeDate || "[Date]";
        document.getElementById('preview-noticeSubject').textContent = data.noticeSubject || "[Subject of Notice]";
        document.getElementById('preview-clientName').textContent = data.clientName || "[Client's Name]";
        document.getElementById('preview-advocateName').textContent = data.advocateName || "[Advocate's Name]";
        document.getElementById('preview-noticeBody').textContent = data.noticeBody || "[Detailed facts...]";
        document.getElementById('preview-compliancePeriod').textContent = data.compliancePeriod || "30";
        document.getElementById('preview-advocateName-2').textContent = data.advocateName || "[Advocate's Name]";

        // Save to localStorage
        localStorage.setItem('legalNoticeData', JSON.stringify(data));
    };

    const loadFromStorage = () => {
        const savedData = localStorage.getItem('legalNoticeData');
        if (savedData) {
            const data = JSON.parse(savedData);
            for (const key in data) {
                if (form.elements[key]) {
                    form.elements[key].value = data[key];
                }
            }
        }
        // Set default date if not present
        if (!form.elements['noticeDate'].value) {
            form.elements['noticeDate'].valueAsDate = new Date();
        }
        updatePreview();
    };

    const generatePDF = () => {
        // Check for jsPDF (loaded from base template)
        if (typeof window.jspdf === 'undefined') {
            alert('Error: PDF library not loaded.');
            return;
        }
        const { jsPDF } = window.jspdf;
        const pdf = new jsPDF();

        // Get the text from the preview pane, not the HTML
        const previewText = document.getElementById('preview-pane').innerText;

        // Add text to PDF
        pdf.setFont("times", "normal");
        pdf.setFontSize(12);

        // Split text into lines and add to PDF
        const lines = pdf.splitTextToSize(previewText, 180); // 180mm width
        pdf.text(lines, 15, 20); // 15mm left, 20mm top

        pdf.save('Legal-Notice.pdf');
    };

    // Attach listeners
    form.addEventListener('input', updatePreview);
    downloadBtn.addEventListener('click', generatePDF);

    // Initial load
    loadFromStorage();
}
