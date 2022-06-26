let scrollTimer = 0;
let isScrolling = false;
let scrollSpeed = 10;


document.addEventListener('keydown', logKey);

function logKey(e) {
    const keyCode = e.keyCode;
    console.log(keyCode)
    if (handleKeyCode(keyCode)) {
        e.preventDefault();
    }
}

function handleKeyCode(keyCode) {
    let handled = true;

    switch (keyCode) {
        case 27: // Escape
            window.scrollTo(0, 0);
            break;
        case 32: // Space
            toggleScrolling();
            break;
        default:
            handled = false;
            break;
    }

    if (handled) {
        // updateDebug();
    }
    return handled;

}

function pageScroll() {
    window.scrollBy(0, 1); // horizontal and vertical scroll increments
    scrollTimer = setTimeout(pageScroll, scrollSpeed);
    console.log('scroll')
}


function toggleScrolling() {
    if (isScrolling === false) {
        pageScroll()
        isScrolling = true;
    } else {
        clearTimeout(scrollTimer);
        isScrolling = false;
    }
}
