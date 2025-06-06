let seconds = 7;
const countdown = document.getElementById('countdown');

if (countdown) {
    const landingUrl = countdown.getAttribute('data-landing-url');
    const timer = setInterval(() => {
        seconds--;
        countdown.textContent = seconds;
        if (seconds <= 0) {
            clearInterval(timer);
            window.location.href = landingUrl;
        }
    }, 1000);
}
