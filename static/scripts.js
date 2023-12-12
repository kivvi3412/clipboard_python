let timeoutId = null;

function saveText(text) {
    const token = localStorage.getItem('token');
    if (token) {
        fetch('/api/text/', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({text: text})
        })
            .then(response => response.json())
            .then(data => {
                console.log('Text saved');
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
}

function onTextInput() {
    const text = document.getElementById('text').value;
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
        saveText(text);
    }, 1); // 延迟1ms保存
}

function loadText() {
    const token = localStorage.getItem('token');
    if (token) {
        fetch('/api/text/', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('text').value = data.text;
            });
    }
}

function uploadFile() {
    const formData = new FormData();
    const fileInput = document.getElementById('fileInput');
    if (fileInput.files.length > 0) {
        formData.append('file', fileInput.files[0]);

        fetch('/api/upload/', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
            },
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                // alert(data.message);
                loadFiles(); // Reload files list if needed
            });
    }
}

function downloadFile(fileName) {
    // Modify to handle file download
    const token = localStorage.getItem('token');
    if (token) {
        fetch('/api/download/', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({file_name: fileName})
        })
            .then(response => response.blob())
            .then(blob => {
                // Create a link to download the blob
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = fileName.split('/').pop(); // Extract actual file name
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            })
            .catch(error => console.error('Error:', error));
    }
}

function deleteFile(fileName) {
    const token = localStorage.getItem('token');
    if (token) {
        fetch('/api/delete/', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({file_name: fileName})
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                loadFiles(); // Reload files list
            });
    }
}

function loadFiles() {
    fetch('/api/files/', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token'),
        }
    })
    .then(response => response.json())
    .then(data => {
        const fileList = document.getElementById('fileList');
        fileList.innerHTML = '';
        data.files.forEach(fullPath => {
            const splitPath = fullPath.split('/');
            const fileName = splitPath[splitPath.length - 1]; // 获取文件名
            const li = document.createElement('li');

            // 使用文件名而不是完整路径
            li.textContent = fileName;

            const downloadButton = document.createElement('button');
            downloadButton.textContent = '下载';
            // 使用闭包来捕获当前的完整路径
            downloadButton.onclick = (function(fullPath) {
                return function() { downloadFile(fullPath); };
            })(fullPath);
            li.appendChild(downloadButton);

            const deleteButton = document.createElement('button');
            deleteButton.textContent = '删除';
            // 同样使用闭包来捕获当前的完整路径
            deleteButton.onclick = (function(fullPath) {
                return function() { deleteFile(fullPath); };
            })(fullPath);
            li.appendChild(deleteButton);

            fileList.appendChild(li);
        });
    });
}



function checkLogin() {
    if (!localStorage.getItem('token')) {
        window.location.href = '/login/'; // Redirect to login page
    }
}


window.onload = () => {
    checkLogin();
    loadText();
    loadFiles();
};