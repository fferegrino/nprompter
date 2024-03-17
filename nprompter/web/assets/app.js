const content = document.getElementById('content')
const mirrorElements = Array.from(document.getElementsByClassName('mirror'))
const nprompterElements = document.querySelectorAll('.nprompter-element');
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
setMirrored(getSetting("mirrored"))


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
    nprompterElements.forEach(function(element) {
        element.style.lineHeight = lineHeight + "em"
    })
}

function increaseLineHeight() {
    const newLineHeight = getSetting("lineHeight") + lineHeightIncrement
    setLineHeight(newLineHeight)
    saveSetting("lineHeight", newLineHeight)
    return `Line height: ${newLineHeight.toFixed(2)}`
}

function setMirrored(mirror) {
    if (mirror) {
        mirrorElements.forEach(function(element) {
            element.classList.add('mirrored')
        })
    } else {
        mirrorElements.forEach(function(element) {
            element.classList.remove('mirrored')
        })
    }
    saveSetting("mirrored", mirror)
}

function mirrorScreen() {
    const mirrored = !getSetting("mirrored")
    setMirrored(mirrored)
    return `Screen mirrored: ${mirrored}`
}

function decreaseLineHeight() {
    const currentLineHeight = getSetting("lineHeight")
    const newLineHeight =  Math.max(minLineHeight, currentLineHeight - lineHeightIncrement);
    setLineHeight(newLineHeight)
    saveSetting("lineHeight", newLineHeight)
    return `Line height: ${newLineHeight.toFixed(2)}`
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

    81: [decreaseFontSize, "Decrease font size", 'Q'],
    87: [increaseFontSize, "Increase font size", 'W'],
    65: [decreasePadding, "Decrease padding", 'A'],
    83: [increasePadding, "Increase padding", 'S'],
    90: [decreaseLineHeight, "Decrease line height", 'Z'],
    88: [increaseLineHeight, "Increase line height", 'X'],

    32: [toggleScrolling, "Start scroll", 'Space'], // Space key
    37: [decreaseSpeed, "Decrease speed", '→'], // Right arrow
    39: [increaseSpeed, "Increase speed", '←'], // Left arrow
    70: [openFullscreen, "Fullscreen", 'F'], // F key
    72: [toggleModalWindow, "Help", 'H'], // H key
    73: [debugInfo, "Show debug info to the console", 'I'], // I key
    77: [mirrorScreen, "Mirror screen", 'M'], // M key
    49: [scrollToTop, "Scroll to top", '1'], // X key

    // Presenter mode controls
    27: [scrollUpManually, "Manual scroll up", "ESC"],
    66: [scrollDownManually, "Scroll down manually", 'B'],
    116: [toggleScrolling, "Toggle scrolling", 'F5'],
    34: [increaseSpeed, "Increase speed", 'PageDown'],
    33: [decreaseSpeed, "Decrease speed", 'PageUp'],
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