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
const defaultLineHeight = {{ font.line_height }};
const defaultFontSize = parseInt(getComputedStyle(content).fontSize);
const defaultPaddingSize = parseInt(getComputedStyle(content).paddingLeft);;
const defaultScrollSpeed = {{ screen.scroll.speed }};

const _settings = {
    "lineHeight": defaultLineHeight,
    "fontSize": defaultFontSize,
    "paddingSize": defaultPaddingSize,
    "scrollSpeed": defaultScrollSpeed,
}

function saveSetting(setting, value) {
    _settings[setting] = value;
    console.log(`Saved setting ${setting} with value ${value}`);
    window.localStorage.setItem("nprompter:settings", JSON.stringify(_settings));
}

function getSetting(setting) {
    return _settings[setting];
}

const settings = JSON.parse(window.localStorage.getItem("nprompter:settings"));
if (settings) {
    console.log("Loaded settings from localStorage");
    Object.assign(_settings, settings);
} else {
    console.log("No settings found in localStorage");
}