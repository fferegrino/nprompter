
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
    return "Scrolled to top"
}

function decreaseSpeed() {
    scrollSpeed = Math.min(maxScrollSpeed, scrollSpeed + scrollSpeedIncrease)
    return `Scroll speed: ${scrollSpeed}`
}

function increaseSpeed() {
    scrollSpeed = Math.max(0, scrollSpeed - scrollSpeedIncrease)
    return `Scroll speed: ${scrollSpeed}`
}

function decreaseFontSize() {
    fontSize = Math.max(0, fontSize - fontSizeIncrease);
    content.style.fontSize = fontSize + "px"
    return `Font size: ${fontSize}`
}

function increaseLineHeight() {
    lineHeight = lineHeight + lineHeightIncrement;
    content.style.lineHeight = lineHeight + "em"
    return `Line height: ${lineHeight}`
}

function decreaseLineHeight() {
    lineHeight =  Math.max(minLineHeight, lineHeight - lineHeightIncrement);
    content.style.lineHeight = lineHeight + "em"
    return `Line height: ${lineHeight}`
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
    return `Padding size: ${paddingSize}`
}

function increasePadding() {
    paddingSize = Math.min(maxPadding, paddingSize + paddingSizeIncrease);
    content.style.paddingLeft = paddingSize + "px"
    content.style.paddingRight = paddingSize + "px"
    return `Padding size: ${paddingSize}`
}

function increaseFontSize() {
    fontSize = Math.min(maxFontSize, fontSize + fontSizeIncrease);
    content.style.fontSize = fontSize + "px"
    return `Font size: ${fontSize}`
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
    scrollTimer = setTimeout(pageScroll, scrollSpeed);
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