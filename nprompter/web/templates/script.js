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


function toggleModalWindow () {
    modal.classList.toggle("open")
}

const controls = {
    27: [function() {
        window.scrollTo(0, 0)
    }, "Scroll to top", 'escape'],
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
    }, "Increase padding", 'p'],
    79: [function() {
        paddingSize = Math.max(0, paddingSize - paddingSizeIncrease);
        content.style.paddingLeft = paddingSize + "px"
        content.style.paddingRight = paddingSize + "px"
    }, "Decrease padding", 'o'],
    85: [function() {
        fontSize = Math.min(maxFontSize, fontSize + fontSizeIncrease);
        content.style.fontSize = fontSize + "px"
    }, "Increase font size", 'u'],
    68: [function() {
        fontSize = Math.max(0, fontSize - fontSizeIncrease);
        content.style.fontSize = fontSize + "px"
    }, "Decrease font size", 'D'],
    32: [toggleScrolling, "Start scroll", 'space'],
    70: [openFullscreen, "Fullscreen", 'f'],
    72: [toggleModalWindow, "Help", 'h'],
    77: [function() {
        mirrorElements.forEach(function (element){
            element.classList.toggle('mirrored')
        })
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
    commands.push(`<li class="command"><kbd>${key}</kbd>: ${docs}</li>`)
}
const help = document.getElementById('help')
help.innerHTML = commands.join(' ')

