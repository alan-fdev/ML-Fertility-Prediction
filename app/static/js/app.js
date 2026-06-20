// Form submission handler
document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Validate form
    if (!this.checkValidity()) {
        e.stopPropagation();
        this.classList.add('was-validated');
        return;
    }

    // Hide previous result
    document.getElementById('resultSection').classList.remove('show');
    document.getElementById('alertMessage').classList.remove('show');

    // Show spinner
    document.getElementById('spinnerContainer').classList.add('show');
    document.getElementById('predictBtn').disabled = true;

    // Collect form data
    const formData = {
        Female_Age: document.getElementById('Female_Age').value,
        Male_Age: document.getElementById('Male_Age').value,
        BMI: document.getElementById('BMI').value,
        Menstrual_Regularity: document.getElementById('Menstrual_Regularity').value,
        PCOS: document.getElementById('PCOS').value,
        Stress_Level: document.getElementById('Stress_Level').value,
        Smoking: document.getElementById('Smoking').value,
        Alcohol_Intake: document.getElementById('Alcohol_Intake').value,
        Sperm_Count_Million_per_ml: document.getElementById('Sperm_Count_Million_per_ml').value,
        'Motility_%': document.getElementById('Motility_%').value,
        Trying_Duration_Months: document.getElementById('Trying_Duration_Months').value,
        Treatment_Type: document.getElementById('Treatment_Type').value
    };

    try {
        // Send prediction request
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        // Hide spinner
        document.getElementById('spinnerContainer').classList.remove('show');
        document.getElementById('predictBtn').disabled = false;

        if (result.success) {
            // Display result
            const resultIcon = document.getElementById('resultIcon');
            const resultTitle = document.getElementById('resultTitle');
            const resultDescription = document.getElementById('resultDescription');
            const probabilityValue = document.getElementById('probabilityValue');
            const probabilityBarFill = document.getElementById('probabilityBarFill');
            const confidenceBadge = document.getElementById('confidenceBadge');

            resultIcon.className = `result-icon ${result.prediction_color}`;
            resultIcon.innerHTML = result.prediction_icon;
            
            resultTitle.textContent = result.prediction_label;
            resultDescription.textContent = `Tingkat Keyakinan: ${result.confidence}`;
            
            probabilityValue.textContent = result.probability + '%';
            probabilityBarFill.style.width = result.probability + '%';
            
            confidenceBadge.textContent = result.confidence;

            // Show result section
            document.getElementById('resultSection').classList.add('show');

            // Scroll to result
            setTimeout(() => {
                document.getElementById('resultSection').scrollIntoView({ behavior: 'smooth' });
            }, 300);
        } else {
            // Show error
            showAlert(result.error, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('spinnerContainer').classList.remove('show');
        document.getElementById('predictBtn').disabled = false;
        showAlert('Terjadi kesalahan saat memproses prediksi. Silakan coba lagi.', 'error');
    }
});

// Reset button handler
document.getElementById('resetBtn').addEventListener('click', function() {
    document.getElementById('predictionForm').classList.remove('was-validated');
    document.getElementById('resultSection').classList.remove('show');
    document.getElementById('alertMessage').classList.remove('show');
});

// Show alert function
function showAlert(message, type) {
    const alertElement = document.getElementById('alertMessage');
    alertElement.textContent = message;
    alertElement.className = `alert-message ${type} show`;
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        alertElement.classList.remove('show');
    }, 5000);
}

// Form validation for numeric inputs
document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('invalid', function(e) {
        if (this.validity.rangeUnderflow) {
            this.setCustomValidity(`Nilai minimum adalah ${this.min}`);
        } else if (this.validity.rangeOverflow) {
            this.setCustomValidity(`Nilai maksimum adalah ${this.max}`);
        } else if (this.validity.stepMismatch) {
            this.setCustomValidity('Format nilai tidak valid');
        } else {
            this.setCustomValidity('');
        }
    });
});
