export function setHeading(heading) {
    const h1 = document.querySelector('.heading');

    if (h1) {
        h1.innerHTML = heading;
    }
}
