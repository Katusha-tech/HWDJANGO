let seconds = 7;
const countdown = document.getElementById('countdown');

if (countdown) {
    const timer = setInterval(() => {
        seconds--;
        countdown.textContent = seconds;
        if (seconds <= 0) {
            clearInterval(timer);
            window.location.href = "{% url 'landing' %}";
        }
    }, 1000);
}