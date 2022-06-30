const content = document.getElementById('content')
const body = document.getElementsByTagName("body")[0]
const elem = document.documentElement;
const manualScrollAmount = 10;
const fontSizeIncrease = 2;
const paddingSizeIncrease = 10;
const maxScrollSpeed = 200;
const scrollSpeedIncrease = 3;
const maxPadding = 250;
const maxFontSize = 200;
let fontSize = parseInt(getComputedStyle(content).fontSize);
let paddingSize = parseInt(getComputedStyle(content).paddingLeft);
let scrollTimer = 0;
let isScrolling = false;
let scrollSpeed = 10;


document.addEventListener('keydown', logKey);

function logKey(e) {
    const keyCode = e.keyCode;
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
    37: [function() {
        scrollSpeed = Math.min(maxScrollSpeed, scrollSpeed + scrollSpeedIncrease)
    }, "Decrease speed", '→'],
    39: [function() {
        scrollSpeed = Math.max(0, scrollSpeed - scrollSpeedIncrease)
    }, "Increase speed", '←'],
    80: [function() {
        paddingSize = Math.min(maxPadding, paddingSize + paddingSizeIncrease);
        content.style.paddingLeft = paddingSize + "px"
        content.style.paddingRight = paddingSize + "px"
    }, "Increase padding", 'P'],
    79: [function() {
        paddingSize = Math.max(0, paddingSize - paddingSizeIncrease);
        content.style.paddingLeft = paddingSize + "px"
        content.style.paddingRight = paddingSize + "px"
    }, "Decrease padding", 'O'],
    85: [function() {
        fontSize = Math.min(maxFontSize, fontSize + fontSizeIncrease);
        content.style.fontSize = fontSize + "px"
    }, "Increase font size", 'U'],
    68: [function() {
        fontSize = Math.max(0, fontSize - fontSizeIncrease);
        content.style.fontSize = fontSize + "px"
    }, "Decrease font size", 'D'],
    32: [toggleScrolling, "Start scroll", 'space'],
    70: [openFullscreen, "Fullscreen", 'f'],
    77: [function() {
        body.classList.toggle('mirrored');
    }, "Mirror screen", 'm']
}

function handleKeyCode(keyCode) {
    let handled = true;
    if (keyCode in controls) {
        const [action, docs, key] = controls[keyCode]
        action()
        console.log(docs)
    } else {
        handled = false;
        console.log("Not handled " + keyCode)
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
    commands.push(`<span class="command"></span><kbd>${key}</kbd>: ${docs}</span>`)
}
const help = document.getElementById('help')
help.innerHTML = commands.join(' ')