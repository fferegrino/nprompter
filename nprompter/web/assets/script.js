let scrollTimer = 0;
let isScrolling = false;
let scrollSpeed = 10;

const content = document.getElementById('content')
const elem = document.documentElement;

document.addEventListener('keydown', logKey);

function logKey(e) {
    const keyCode = e.keyCode;
    console.log(keyCode)
    if (handleKeyCode(keyCode)) {
        e.preventDefault();
    }
}

/* View in fullscreen */
function openFullscreen() {
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.webkitRequestFullscreen) {
        /* Safari */
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) {
        /* IE11 */
        elem.msRequestFullscreen();
    }
}

const controls = {
    27: [function() {
        window.scrollTo(0, 0)
    }, "Scroll to top", 'esc'],
    32: [toggleScrolling, "Start scroll", 'space'],
    70: [openFullscreen, "Fullscreen", 'f'],
    77: [function() {
        content.classList.toggle('mirrored');
    }, "Mirror screen", 'm']
}

function handleKeyCode(keyCode) {
    let handled = true;
    if (keyCode in controls) {
        const [action, docs, key] = controls[keyCode]
        action()
    } else {
        handled = false;
        console.log("Not handled " + keyCode)
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


const commands = [];

for (var [keyCode, [fn, docs, key]] of Object.entries(controls)) {
    commands.push(`<kbd>${key}</kbd>: ${docs}`)
}
const help = document.getElementById('help')
help.innerHTML = commands.join(' ')