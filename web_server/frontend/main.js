url = 'http://192.168.1.2:17171/'

const login_container = document.getElementById('login_container');
const menu_container = document.getElementById('menu_container');
const change_pw_container = document.getElementById('change_pw_container')
const control_container = document.getElementById('control_container');

const username = document.getElementById('username');
const password = document.getElementById('password');
const ch_password = document.getElementById('ch_password');
const new_password = document.getElementById('new_password');
const start_time = document.getElementById('start_time');
const end_time = document.getElementById('end_time');

const login_btn = document.getElementById('login_btn');
const change_pw_btn = document.getElementById('change_pw_btn');
const control_btn = document.getElementById('control_btn');
const new_password_btn = document.getElementById('new_password_btn');
const submit_btn = document.getElementById('submit_btn');
const log_out_btn = document.getElementById('log_out_btn');

const pw_to_menu_btn = document.getElementById('pw_to_menu_btn');
const time_to_menu_btn = document.getElementById('time_to_menu_btn');

function QueryLogin(username, password) {
    const header = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            api_name: 'login',
            username: `${username}`,
            password: `${password}`
        })
    }

    return header
}

function UpdatePassword(username, password, new_password) {
    const header = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            api_name: 'update_password',
            username: `${username}`,
            password: `${password}`,
            new_password: `${new_password}`
        })
    }

    return header
}

function UpdateInterval(start_time, end_time) {
    const header = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            api_name: 'upd_time_interval',
            time_interval: `${start_time}-${end_time}`
        })
    }

    return header
}

login_btn.addEventListener('click', async () => {
    if (username.value.length === 0 || password.value.length === 0) {
        alert('Invalid input');
    } else {
        await fetch(url, QueryLogin(username.value, password.value))
            .then(res => {
                if (!res.ok) {
                    alert('Username or password error');
                } else {
                    login_username = username.value;
                    menu_container.style.visibility = 'visible';
                    username.value = '';
                    password.value = '';
                    login_container.style.visibility = 'hidden';
                    res.json().then(obj => {
                        group = obj.group;
                        console.log(group)
                        if (group === 'students') {
                            control_btn.style.visibility = 'hidden';
                        } else {
			    control_btn.style.visibility = 'inherit';
			}
                    })
                }
            })
            .catch(error => alert(error));
    }
})

change_pw_btn.addEventListener('click', () => {
    menu_container.style.visibility = 'hidden';
    change_pw_container.style.visibility = 'visible';
})

new_password_btn.addEventListener('click', async () => {
    if (ch_password.value.length === 0 || new_password.value.length === 0) {
        alert('Invalid input');
    } else {
        await fetch(url, UpdatePassword(login_username, ch_password.value, new_password.value))
            .then(res => {
                if (!res.ok) {
                    alert('Update password error');
                } else {
                    alert('Update password success');
                    ch_password.value = '';
                    new_password.value = '';
                    change_pw_container.style.visibility = 'hidden';
                    menu_container.style.visibility = 'visible';
                }
            })
            .catch(error => alert(error))
    }
})

control_btn.addEventListener('click', () => {
    menu_container.style.visibility = 'hidden';
    control_container.style.visibility = 'visible';
})

submit_btn.addEventListener('click', async () => {
    if (start_time.value.length != 4 || end_time.value.length != 4 || isNaN(start_time.value) || isNaN(end_time.value)) {
        alert('Invalid time format');
    } else if (Number(start_time.value) < 0 || Number(start_time.value) >= 2400 || Number(end_time.value) < 0 || Number(end_time.value) >= 2400) {
        alert('Invalid time value');
    } else if (Number(start_time.value) % 100 >= 60 || Number(end_time.value) % 100 >= 60) {
        alert('Invalid time value');
    } else if (Number(start_time.value) > Number(end_time.value)) {
        alert('Invalid time range');
    } else {
        await fetch(url, UpdateInterval(start_time.value, end_time.value))
            .then(res => {
                console.log(res)
                if (!res.ok) {
                    alert('Update time interval error');
                } else{
                    alert(`Update success: ${start_time.value}-${end_time.value}`);
                    start_time.value = '';
                    end_time.value = '';
                    control_container.style.visibility = 'hidden';
                    menu_container.style.visibility = 'visible';
                }
            })
            .catch(error => alert(error));
    }
})

log_out_btn.addEventListener('click', () => {
    menu_container.style.visibility = 'hidden';
    login_container.style.visibility = 'visible';
})

pw_to_menu_btn.addEventListener('click', () => {
    menu_container.style.visibility = 'visible';
    change_pw_container.style.visibility = 'hidden';
})

time_to_menu_btn.addEventListener('click', () => {
    menu_container.style.visibility = 'visible';
    control_container.style.visibility = 'hidden';
})
