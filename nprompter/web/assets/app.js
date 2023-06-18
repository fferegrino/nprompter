const content = document.getElementById('content')
const mirrorElements = Array.from(document.getElementsByClassName('mirror'))
const modal = document.getElementById('modal')
const elem = document.documentElement;
const snackbar = document.getElementById("snackbar");
let isScrolling = false
let scrollTimer = 0;
let snackbarTimer = -1;

document.addEventListener('keydown', logKey);
setFontSize(getSetting("fontSize"))
setPadding(getSetting("paddingSize"))
setLineHeight(getSetting("lineHeight"))



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
    return "Scrolled to top"
}

function decreaseSpeed() {
    const scrollSpeed = Math.min(maxScrollSpeed, getSetting("scrollSpeed") + scrollSpeedIncrease);
    saveSetting("scrollSpeed", scrollSpeed)
    return `Scroll speed: ${scrollSpeed}`
}

function increaseSpeed() {
    const scrollSpeed = Math.max(0, getSetting("scrollSpeed") - scrollSpeedIncrease)
    saveSetting("scrollSpeed", scrollSpeed)
    return `Scroll speed: ${scrollSpeed}`
}

function setLineHeight(lineHeight) {
    content.style.lineHeight = lineHeight + "em"
}

function increaseLineHeight() {
    const newLineHeight = getSetting("lineHeight") + lineHeightIncrement
    setLineHeight(newLineHeight)
    saveSetting("lineHeight", newLineHeight)
    return `Line height: ${newLineHeight}`
}

function decreaseLineHeight() {
    const currentLineHeight = getSetting("lineHeight")
    const newLineHeight =  Math.max(minLineHeight, currentLineHeight - lineHeightIncrement);
    setLineHeight(newLineHeight)
    saveSetting("lineHeight", newLineHeight)
    return `Line height: ${newLineHeight}`
}

function mirrorScreen() {
    mirrorElements.forEach(function(element) {
        element.classList.toggle('mirrored')
    })
}

function setPadding(paddingSize) {
    content.style.paddingLeft = paddingSize + "px"
    content.style.paddingRight = paddingSize + "px"
}

function decreasePadding() {
    const currentPadding = getSetting("paddingSize")
    const newPaddingSize = Math.max(0, currentPadding - paddingSizeIncrease);
    setPadding(newPaddingSize)
    saveSetting("paddingSize", newPaddingSize)
    return `Padding size: ${newPaddingSize}`
}

function increasePadding() {
    const currentPadding = getSetting("paddingSize")
    const newPadding = Math.min(maxPadding, currentPadding + paddingSizeIncrease);
    setPadding(newPadding)
    saveSetting("paddingSize", newPadding)
    return `Padding size: ${newPadding}`
}

function setFontSize(fontSize) {
    content.style.fontSize = fontSize + "px"
}

function increaseFontSize() {
    const currentFontSize = getSetting("fontSize")
    const newFontSize = Math.min(maxFontSize, currentFontSize + fontSizeIncrease);
    setFontSize(newFontSize)
    saveSetting("fontSize", newFontSize)
    return `Font size: ${newFontSize}`
}

function decreaseFontSize() {
    const currentFontSize = getSetting("fontSize")
    const newFontSize = Math.max(0, currentFontSize - fontSizeIncrease);
    setFontSize(newFontSize)
    saveSetting("fontSize", newFontSize)
    return `Font size: ${newFontSize}`
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
    // Normal controls
    27: [scrollUpManually, "Manual scroll up", "ESC"], // Esc key
    32: [toggleScrolling, "Start scroll", 'space'], // Space key
    37: [decreaseSpeed, "Decrease speed", '→'], // Right arrow
    39: [increaseSpeed, "Increase speed", '←'], // Left arrow
    68: [decreaseFontSize, "Decrease font size", 'D'], // D key
    70: [openFullscreen, "Fullscreen", 'f'], // F key
    72: [toggleModalWindow, "Help", 'h'], // H key
    73: [debugInfo, "Show debug info to the console", 'i'], // I key
    77: [mirrorScreen, "Mirror screen", 'm'], // M key
    79: [decreasePadding, "Decrease padding", 'o'], // O key
    80: [increasePadding, "Increase padding", 'p'], // P key
    81: [decreaseLineHeight, "Decrease padding", 'q'], // Q key
    87: [increaseLineHeight, "Increase padding", 'w'], // W key
    88: [scrollToTop, "Scroll to top", 'x'], // X key
    85: [increaseFontSize, "Increase font size", 'u'], // U key
    // Presenter mode controls
    116: [toggleScrolling, "Toggle scrolling", 'F5'], // F5 key
    34: [increaseSpeed, "Increase speed", 'PageDown'], // PageDown key
    33: [decreaseSpeed, "Decrease speed", 'PageUp'], // PageUp key
    66: [scrollDownManually, "Scroll down manually", 'B'] // B key
}

function handleKeyCode(keyCode) {
    let handled = true;
    if (keyCode in controls) {
        const [action, docs, key] = controls[keyCode]
        const result = action()
        if(result) {
            showInfo(result)
        }
    } else {
        handled = false;
    }
    return handled;
}

function scrollUpManually() {
    window.scrollBy(0, -1 * manualScrollAmount);
}

function scrollDownManually() {
    window.scrollBy(0, manualScrollAmount);
}

function pageScroll() {
    window.scrollBy(0, 1); // horizontal and vertical scroll increments
    scrollTimer = setTimeout(pageScroll, getSetting("scrollSpeed"));
}

function toggleScrolling() {
    if (isScrolling === false) {
        pageScroll()
        isScrolling = true;
        return "Scrolling started"
    } else {
        clearTimeout(scrollTimer);
        isScrolling = false;
        return "Scrolling stopped"
    }
}


const commands = [];

for (const [keyCode, [fn, docs, key]] of Object.entries(controls)) {
    commands.push(`<li class="command"><kbd>${key}</kbd>: ${docs}</li>`)
}
const help = document.getElementById('help')
help.innerHTML = commands.join(' ')

function showInfo(message) {
    snackbar.innerHTML = message;
   if (snackbar.className !== "show") {
       snackbar.className = "show";
       // After 3 seconds, remove the show class from DIV
       snackbarTimer = setTimeout(function () {
           snackbar.className = snackbar.className.replace("show", "");
       }, snackbarTimeout);
   }
   else {
         clearTimeout(snackbarTimer);
         snackbarTimer = setTimeout(function () {
              snackbar.className = snackbar.className.replace("show", "");
         }, snackbarTimeout);
   }
}