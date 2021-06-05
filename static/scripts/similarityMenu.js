let similarity = document.getElementById('similarity').children;
let leftButton = document.getElementById('leftButton');
let rightButton = document.getElementById('rightButton');
if (similarity[0] !== undefined) {
    similarity[0].style.display = "";
}
let index = 0;
let len = parseInt(document.getElementById('len').textContent);
if (len <= 1) {
    rightButton.disabled = true;
}

leftButton.onclick = () => {
    if (index - 1 >= 0) {
        similarity[index].style.display = "none";
        index--;
        similarity[index].style.display = "";
        rightButton.disabled = false;
        if (index === 0) {
            leftButton.disabled = true;
        } else {
            leftButton.disabled = false;
        }
    }
}

rightButton.onclick = () => {
    if (index + 1 < len) {
        similarity[index].style.display = "none";
        index++;
        similarity[index].style.display = "";
        leftButton.disabled = false;
        if (index === len - 1) {
            rightButton.disabled = true;
        } else {
            rightButton.disabled = false;
        }
    }
}
