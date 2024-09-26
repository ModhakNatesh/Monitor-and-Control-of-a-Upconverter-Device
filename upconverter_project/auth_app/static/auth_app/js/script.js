document.addEventListener('DOMContentLoaded', () => {
    const dateTimeElement = document.getElementById('dateTime');
    const updateDateTime = () => {
        const now = new Date();
        dateTimeElement.textContent = now.toLocaleString();
    };
    setInterval(updateDateTime, 1000);
    updateDateTime();
});

