document.addEventListener('DOMContentLoaded', function() {
    const modeSelect = document.querySelector('select[name="mode"]');
    if (modeSelect) {
        modeSelect.addEventListener('change', function() {
            this.form.submit();
        });
    }
});