document.addEventListener('DOMContentLoaded', () => {
    const today = new Date().toISOString().split('T')[0];
    document.querySelectorAll('input[type="date"]').forEach((input) => {
        if (!input.value) {
            input.value = today;
        }
        input.min = today;
    });
});
