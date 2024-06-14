let currentNav = 'HID';
let IP = '';
let MODE = '';
let SSID = '';
let PASSW = '';
let AP = '';
let retryCount = 3;
let currentTemplate = '';

let currentIndex = 0;
let setupData = {"IP": '', "SSID": '', "PASSW": '', "MODE": "", "AP": ""};
let setupDataItems = {
    "IP": "10.0.0.15", 
    "SSID": "Atom Ducky", 
    "Password": '', 
    "Device Mode": 'NORMAL', 
    "Access Point Mode": 'TRUE'
};

let settingsDefaults = {
    "IP": IP, 
    "SSID": SSID, 
    "Password": PASSW, 
    "Device Mode": MODE, 
    "Access Point Mode": AP    
};

const setupKeys = Object.keys(setupData);
const setupItemKeys = Object.keys(setupDataItems);
const settingsDefaultsKeys = Object.keys(settingsDefaults);

async function readConfig() {
    try {
        const response = await fetch('/atoms/_config');
        const data = await response.text();
        const lines = data.split('\n');
        for (let line of lines) {
            const [key, value] = line.split('=');
            if (key === 'IP') {
                IP = value.trim();
            }
            if (key === 'SSID') {
                SSID = value.trim();
            }
            if (key === 'PASSW') {
                PASSW = value.trim();
            }
            if (key === 'AP') {
                AP = value.trim();
            }
            if (key === 'MODE') {
                MODE = value.trim();
            }
        }

        // Update settingsDefaults with the values from the config
        settingsDefaults = {
            "IP": IP, 
            "SSID": SSID, 
            "Password": PASSW, 
            "Device Mode": MODE, 
            "Access Point Mode": AP    
        };

        // Call createSettingsRows after readConfig has populated the config values
        createSettingsRows();

    } catch (error) {
        if (retryCount > 0) {
            console.log(`Retrying... Attempts left: ${retryCount - 1}`);
            retryCount = retryCount - 1;
            setTimeout(() => readConfig(), 1000);
        } else {
            console.error('Max retries reached. Giving up.');
        }
        retryCount = 3;
    }
}

function createSettingsRows() {
    const settingsContainer = document.getElementById('settings-container');
    const placeholderRow = settingsContainer.querySelector('.settings-card-row');

    settingsDefaultsKeys.forEach((key, index) => {
        const newRow = placeholderRow.cloneNode(true);
        newRow.style.display = 'flex';
        newRow.querySelector('.settings-card-item').innerText = key;
        const inputElement = newRow.querySelector('.settings-card-input');
        inputElement.placeholder = settingsDefaults[key];
        inputElement.id = `settings-card-input-${index}`;
        settingsContainer.appendChild(newRow);
    });
    console.log("Data", IP, SSID, PASSW, MODE, AP)
    placeholderRow.remove(); // Remove the initial placeholder row
}

function showPopInput(placeholder, callback) {
    const popInput = document.querySelector('.pop-input');
    const input = document.getElementById('popInput');
    const okButton = popInput.querySelector('.card-button');

    input.placeholder = placeholder;

    okButton.replaceWith(okButton.cloneNode(true));
    popInput.querySelector('.card-button').addEventListener('click', () => {
        callback(input.value);
        popInput.style.display = 'none';
    });

    popInput.style.display = 'flex';
}

function rubberMode() {
    if (MODE === '') {
        console.error('MODE not set!');
        return;
    }
    const mode = (MODE === 'NORMAL') ? 'RUBBER' : 'NORMAL';
    const configUpdates = {
        "MODE": mode,
    };

    fetch(`/edit_config`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(configUpdates)
    })
    .then(response => response.text())
    .then(data => {
        console.log(data);
        const rubberModeElements = document.getElementsByClassName('rubber-mode');
        if (rubberModeElements.length > 0){
            rubberModeElements[0].style.display = 'flex';
            document.getElementById("rubber-state").textContent = (mode === 'RUBBER') ? 'Rubber Mode Activated' : 'Rubber Mode Deactivated';
        }
         
    })
    .catch(error => console.error('Error:', error));
}

function newTemplate() {
    showPopInput('Enter template name', (inputValue) => {
        console.log(`New template name: ${inputValue}`);
        fetch(`/ret_templates?action=write&name=${inputValue}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain'
            },
            body: ''
        })
    });
}

function toggleMenu() {
    var menu = document.getElementById("dropdownMenu");
    menu.classList.toggle("show");
}

function setNav(nav) {
    currentNav = nav;
    updateCardContent();
}

function softReboot() {
    fetch(`/restart`)
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
}

function saveSettings() {
    setupKeys.forEach((key, index) => {
        const inputElement = document.getElementById(`settings-card-input-${index}`);
        const value = inputElement.value.trim();
        if (value !== '' || key === 'PASSW') {
            setupData[key] = value;
        }
    });

    const filteredSetupData = Object.fromEntries(
        Object.entries(setupData).filter(([key, value]) => value.trim() !== '' || key === 'PASSW')
    );

    fetch('/edit_config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(filteredSetupData)
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text) });
        }
        return response.text();
    })
    .then(data => {
        console.log('Success:', data);
        alert("Setup saved successfully. Restarting device...");
        softReboot();
    })
    .catch((error) => {
        console.error('Error:', error);
        alert(`Couldn't save the config due to ${error.message}`)
    });
}

function nextItem() {
    const inputElement = document.getElementById('setup-card-input');
    const key = setupKeys[currentIndex];
    const value = inputElement.value;

    if (value.trim() !== '') {
        setupData[key] = value;
    }

    currentIndex++;

    if (currentIndex < setupKeys.length) {
        const setupItemKey = setupItemKeys[currentIndex];
        const setupItemValue = setupDataItems[setupItemKey];
        document.getElementById('setup-card-item').innerText = setupItemKey;
        inputElement.value = '';
        inputElement.placeholder = setupItemValue;
    } else {
        document.getElementById('setup-card-item').innerText = 'Save the setup and restart the device?';
        inputElement.style.display = 'none';
        document.getElementById('next-button').style.display = 'none';
        document.getElementById('save-button').style.display = 'flex';
    }
}

function saveSetup() {
    const filteredSetupData = Object.fromEntries(
        Object.entries(setupData).filter(([key, value]) => value.trim() !== '' || key === 'PASSW')
    );

    fetch('/edit_config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(filteredSetupData)
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text) });
        }
        return response.text();
    })
    .then(data => {
        console.log('Success:', data);
        alert("Setup saved successfully. Restarting device...");
        softReboot();
    })
    .catch((error) => {
        console.error('Error:', error);
        alert(`Couldn't save the config due to ${error.message}`)
    });
}


function showSection(sectionId) {
    const sections = document.querySelectorAll('.body-section');
    sections.forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById(sectionId).style.display = 'flex';
}

function updateCardContent() {
    document.getElementById('hidContent').classList.remove('card-content-show');

    document.querySelectorAll('.menu-card-nav div').forEach(el => {
        el.classList.remove('currently-selected');
    });

    if (currentNav === 'HID') {
        document.getElementById('hidContent').classList.add('card-content-show');
        document.querySelector('.nav1').classList.add('currently-selected');
    }
}

function hideSinglePayload() {
    document.querySelectorAll('.card-content-menu').forEach(el => {
        el.style.display = 'flex';
    });
    document.querySelectorAll('.single-payload').forEach(el => {
        el.style.display = 'none';
    });  
}

function showEditPayload() {
    document.querySelectorAll('.card-content-menu').forEach(el => {
        el.style.display = 'none';
    });
    document.querySelectorAll('.edit-payload').forEach(el => {
        el.style.display = 'flex';
    });
    readPayload();
}

function injectPayload() {
    fetch(`/inject`)
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
}

function readPayload() {
    fetch(`/modify_payload?action=read`)
        .then(response => response.text())
        .then(data => {
            console.log(data);
            document.getElementById('payloadTextarea').value = data;
        })
        .catch(error => { 
            console.log(error)
            if (retryCount > 0) {
            console.log(`Retrying... Attempts left: ${retryCount - 1}`);
            retryCount = retryCount - 1;
            setTimeout(() => readPayload(retryCount - 1), 1000);
            } else {
            console.error('Max retries reached. Giving up.');
            }
            retryCount = 3

        });
}

function savePayload() {
    const data = document.getElementById('payloadTextarea').value;
    console.log(data)
    console.log(data.length)
    fetch(`/modify_payload?action=write`, {
        method: 'POST',
        headers: {
            'Content-Type': 'text/plain',
            'Content-Length': data.length
        },
        body: data
        })
        .then(response => {
            if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
            }
            return response.text();
        })
        .then(data => console.log(data))
        .catch(error => {
            console.error('Error:', error);

            if (retryCount > 0) {
            console.log(`Retrying... Attempts left: ${retryCount - 1}`);
            retryCount = retryCount - 1;
            setTimeout(() => savePayload(retryCount - 1), 1000);
            } else {
            console.error('Max retries reached. Giving up.');
            }
            retryCount = 3

        });

    document.querySelectorAll('.card-content-menu').forEach(el => {
        el.style.display = 'flex';
    });
    document.querySelectorAll('.edit-payload').forEach(el => {
        el.style.display = 'none';
    });
    }

function displayKeyboard() {
    document.querySelectorAll('.card-content-menu').forEach(el => {
        el.style.display = 'none';
    });
    document.querySelectorAll('.keyLayout').forEach(el => {
        el.style.display = 'flex';
    });
}

function hideKeyboard() {
    document.querySelectorAll('.card-content-menu').forEach(el => {
        el.style.display = 'flex';
    });
    document.querySelectorAll('.keyLayout').forEach(el => {
        el.style.display = 'none';
    });
}

// Initial state
updateCardContent();
const keyMapping = {
    "LSHIFT": "<LSHT>",
    "RSHIFT": "<RSHT>",
    "BACKSPACE": "<BSC>",
    "ENTER": "<RET>",
    "TAB": "<TAB>",
    "CAPS LOCK": "<CAPS>",
    "CTRL": "<CTRL>",
    "CMD": "<CMD>",
    "ALT": "<ALT>",
    "SPACE": "<SPACE>",
    "UP": "<ARU>",
    "PRINT SCREEN": "<SCR>",
    "DOWN": "<ARD>",
    "LEFT": "<ARL>",
    "RIGHT": "<ARR>"
};

function singlePayload() {
    document.querySelectorAll('.card-content-menu').forEach(el => {
        el.style.display = 'none';
    });
    document.querySelectorAll('.single-payload').forEach(el => {
        el.style.display = 'flex';
    });
}

function sendSinglePayload() {
    const data = document.getElementById('singlePayloadTextarea').value;
    fetch('/single_payload', {
        method: 'POST',
        headers: {
            'Content-Type': 'text/plain',
            'Content-Length': data.length
        },
        body: data
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }
        return response.text();
    })
    .then(data => {
        console.log(data);
        hideSinglePayload();
    })
    .catch(error => {
        if (retryCount > 0) {
                console.log(`Retrying... Attempts left: ${retryCount - 1}`);
                retryCount = retryCount - 1;
                setTimeout(() => sendSinglePayload(retryCount - 1), 1000);
                } else {
                console.error('Max retries reached. Giving up.');
            }
        retryCount = 3
        
    });
}

function showTemplates() {
    document.querySelectorAll('.card-content-menu').forEach(el => {
        el.style.display = 'none';
    });
    document.querySelectorAll('.templates').forEach(el => {
        el.style.display = 'flex';
    });

    fetchTemplates();
}

function hideTemplates(value='flex') {
    document.querySelectorAll('.card-content-menu').forEach(el => {
        el.style.display = `${value}`;
    });
    document.querySelectorAll('.templates').forEach(el => {
        el.style.display = 'none';
    });
}

function editTemplateVisibility(mod) {
    document.querySelectorAll('.edit-template').forEach(el => {
        el.style.display = `${mod}`;
    });
}

function fetchTemplates() {
    fetch('/ret_templates?action=read_list')
        .then(response => response.text())
        .then(data => {
            const templatesList = document.getElementById('templatesList');
            templatesList.innerHTML = '';

            const templates = JSON.parse(data); // Assuming the server returns a JSON list
            templates.forEach(template => {
                const button = document.createElement('button');
                button.addEventListener('click', () => {
                    fetch(`/ret_templates?action=read&name=${template.replace(".txt", "")}`) // Pass the template name to the server
                    .then(response => response.text())
                    .then(data => {
                        console.log(`Data from ${template}: ${data}`);
                        hideTemplates(value="none");
                        editTemplateVisibility("flex");
                        currentTemplate = template;
                        document.getElementById('editPayloadTextarea').value = data;

                    })
                });
                button.classList.add('templates-button');
                button.textContent = template;
                templatesList.appendChild(button);
            });
        })
        .catch(error => {
            console.error('Error fetching templates:', error);
            if (retryCount > 0) {
                console.log(`Retrying... Attempts left: ${retryCount - 1}`);
                retryCount = retryCount - 1;
                setTimeout(() => fetchTemplates(retryCount - 1), 1000);
                } else {
                console.error('Max retries reached. Giving up.');
            }
            retryCount = 3
        });
}

function saveTemplateVisibility() {
    editTemplateVisibility("none");
    hideTemplates();
}

function saveTemplate() {
    if (currentTemplate !== '') {
        const data = document.getElementById('editPayloadTextarea').value;
        fetch(`/ret_templates?action=write&name=${currentTemplate.replace('.txt', '')}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain',
                'Content-Length': data.length
            },
            body: data
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Request failed with status ${response.status}`);
            }
            return response.text();
        })
        .then(data => {
            console.log(data);
            saveTemplateVisibility();
        })
        .catch(error => {
            console.error('Error:', error);
            if (retryCount > 0) {
                console.log(`Retrying... Attempts left: ${retryCount - 1}`);
                retryCount = retryCount - 1;
                setTimeout(() => saveTemplate(retryCount - 1), 1000);
                } else {
                console.error('Max retries reached. Giving up.');
            }
            retryCount = 3
        });
    }
    else {
        console.log('Error saving template, currentTemplate variable is empty!')
    }
}

function runTemplate() {
    if (currentTemplate !== '') { 
        const data = document.getElementById('editPayloadTextarea').value;
        fetch('/single_payload', {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain',
                'Content-Length': data.length
            },
            body: data
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Request failed with status ${response.status}`);
            }
            return response.text();
        })
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.log(error)
            if (retryCount > 0) {
                    console.log(`Retrying... Attempts left: ${retryCount - 1}`);
                    retryCount = retryCount - 1;
                    setTimeout(() => runTemplate(retryCount - 1), 1000);
                    } else {
                    console.error('Max retries reached. Giving up.');
                }
            retryCount = 3
            
        });

    }
}

function bindButtons() {
    const buttons = document.querySelectorAll('.keyLayout button');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            let keyName = button.textContent.trim();
            if (keyName === 'Leave') {
                return;
            }
            if (keyMapping[keyName]) {
                keyName = keyMapping[keyName];
            }
            fetch('/single_payload', {
                method: 'POST',
                headers: {
                    'Content-Type': 'text/plain'
                },
                body: keyName
            })
            .then(response => response.text())
            .then(data => {
                console.log('Key sent:', data);
            })
            .catch(error => {
                console.error('Error sending key:', error);
            });
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    readConfig();
    bindButtons();
});