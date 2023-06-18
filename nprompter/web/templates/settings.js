const content = document.getElementById('content')
const mirrorElements = Array.from(document.getElementsByClassName('mirror'))
const modal = document.getElementById('modal')
const elem = document.documentElement;
const snackbar = document.getElementById("snackbar");
const manualScrollAmount = 40;
const fontSizeIncrease = {{ font.size_increment }};
const paddingSizeIncrease = {{ screen.padding.increment }};
const maxScrollSpeed = {{ screen.scroll.max_speed }};
const scrollSpeedIncrease = {{ screen.scroll.speed_increment }};
const maxPadding = {{ screen.padding.max_value }};
const maxFontSize = {{ font.max_size }};
const minLineHeight = 0.1;
const lineHeightIncrement = {{ font.line_height_increment }};
const snackbarTimeout = 500;
let lineHeight = {{ font.line_height }};
let fontSize = parseInt(getComputedStyle(content).fontSize);
let paddingSize = parseInt(getComputedStyle(content).paddingLeft);
let scrollTimer = 0;
let snackbarTimer = -1;
let isScrolling = false;
let scrollSpeed = {{ screen.scroll.speed }};


