document.getElementById('searchForm').onsubmit = () => {
    document.getElementById('content').style.opacity = 0.3;
    document.getElementById('spinnerContainer').style.display = "block";
    let timer = setInterval(() => {
        let time = document.getElementById('time');
        let currentTime = time.textContent;
        time.textContent = parseInt(currentTime) + 1;
    }, 1000);
};
