document.addEventListener('DOMContentLoaded', function() {
    // Toggle collapse for inline rows
    document.querySelectorAll('.inline-related h3').forEach(header => {
        header.addEventListener('click', function() {
            const row = this.parentElement;
            const content = row.querySelector('.form-row');
            if (content.style.display === 'none') {
                content.style.display = 'block';
                this.style.background = '#e7e7e7';
            } else {
                content.style.display = 'none';
                this.style.background = '#f0f0f0';
            }
        });
    });

    // Initialize collapse state
    document.querySelectorAll('.inline-related .form-row').forEach(row => {
        row.style.display = 'none';
    });

    // Auto-focus first input in new inline form
    document.querySelectorAll('.inline-related.dynamic').forEach(form => {
        const firstInput = form.querySelector('input, select');
        if (firstInput) {
            firstInput.focus();
        }
    });
});