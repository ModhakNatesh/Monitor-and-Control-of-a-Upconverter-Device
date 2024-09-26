document.addEventListener('DOMContentLoaded', () => {
    const dateTimeElement = document.getElementById('dateTime');
    const updateDateTime = () => {
        const now = new Date();
        now.setHours(now.getHours() - 5);
        now.setMinutes(now.getMinutes() - 30);
        dateTimeElement.textContent = now.toLocaleString();
    };
    setInterval(updateDateTime, 1000);
    updateDateTime();
});
