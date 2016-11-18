export function setHeading(heading) {
    const h1 = document.querySelector('.heading');

    if (h1) {
        console.log('Updating heading', heading)
        h1.innerHTML = heading;
    }
}
