const content = document.getElementById('content')
const mirrorElements = Array.from(document.getElementsByClassName('mirror'))
const modal = document.getElementById('modal')
const elem = document.documentElement;
const manualScrollAmount = 10;
const fontSizeIncrease = {{ font.size_increment }};
const paddingSizeIncrease = {{ screen.padding.increment }};
const maxScrollSpeed = {{ screen.scroll.max_speed }};
const scrollSpeedIncrease = {{ screen.scroll.speed_increment }};
const maxPadding = {{ screen.padding.max_value }};
const maxFontSize = {{ font.max_size }};
let fontSize = parseInt(getComputedStyle(content).fontSize);
let paddingSize = parseInt(getComputedStyle(content).paddingLeft);
let scrollTimer = 0;
let isScrolling = false;
let scrollSpeed = {{ screen.scroll.speed }};


document.addEventListener('keydown', logKey);

function logKey(e) {
    const keyCode = e.keyCode;
    if (handleKeyCode(keyCode)) {
        e.preventDefault();
    }
}

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

function toggleModalWindow() {
    modal.classList.toggle("open")
}

function scrollToTop() {
    window.scrollTo(0, 0)
}

function decreaseSpeed() {
    scrollSpeed = Math.min(maxScrollSpeed, scrollSpeed + scrollSpeedIncrease)
}

function increaseSpeed() {
    scrollSpeed = Math.max(0, scrollSpeed - scrollSpeedIncrease)
}

function decreaseFontSize() {
    fontSize = Math.max(0, fontSize - fontSizeIncrease);
    content.style.fontSize = fontSize + "px"
}

function mirrorScreen() {
    mirrorElements.forEach(function(element) {
        element.classList.toggle('mirrored')
    })
}

function decreasePadding() {
    paddingSize = Math.max(0, paddingSize - paddingSizeIncrease);
    content.style.paddingLeft = paddingSize + "px"
    content.style.paddingRight = paddingSize + "px"
}

function increasePadding() {
    paddingSize = Math.min(maxPadding, paddingSize + paddingSizeIncrease);
    content.style.paddingLeft = paddingSize + "px"
    content.style.paddingRight = paddingSize + "px"
}

function increaseFontSize() {
    fontSize = Math.min(maxFontSize, fontSize + fontSizeIncrease);
    content.style.fontSize = fontSize + "px"
}

function debugInfo() {
    const properties = new Map([
        ["Font size", fontSize],
        ["Padding size", paddingSize],
        ["Scroll speed", scrollSpeed]
    ]);

    const black = 'color:black; font-size:25px; font-weight: bold; -webkit-text-stroke: 1px white;'
    const red = 'color:red; font-size:25px; font-weight: bold; -webkit-text-stroke: 1px black;'

    const propertyList = new Array()
    const colors = new Array()
    properties.forEach((value, key, map) => {
        propertyList.push(`%c${key}: %c${value}`);
        colors.push(red)
        colors.push(black)
    })
    console.log(propertyList.join(' '), ...colors)
}

const controls = {
    27: [scrollToTop, "Scroll to top", 'escape'],
    32: [toggleScrolling, "Start scroll", 'space'],
    37: [decreaseSpeed, "Decrease speed", '→'],
    39: [increaseSpeed, "Increase speed", '←'],
    68: [decreaseFontSize, "Decrease font size", 'D'],
    70: [openFullscreen, "Fullscreen", 'f'],
    72: [toggleModalWindow, "Help", 'h'],
    73: [debugInfo, "Show debug info to the console", 'i'],
    77: [mirrorScreen, "Mirror screen", 'm'],
    79: [decreasePadding, "Decrease padding", 'o'],
    80: [increasePadding, "Increase padding", 'p'],
    85: [increaseFontSize, "Increase font size", 'u']
}

function handleKeyCode(keyCode) {
    let handled = true;
    if (keyCode in controls) {
        const [action, docs, key] = controls[keyCode]
        action()
    } else {
        handled = false;
    }
    return handled;
}

function pageScroll() {
    window.scrollBy(0, 1); // horizontal and vertical scroll increments
    scrollTimer = setTimeout(pageScroll, scrollSpeed);
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
    commands.push(`<li class="command"><kbd>${key}</kbd>: ${docs}</li>`)
}
const help = document.getElementById('help')
help.innerHTML = commands.join(' ')
