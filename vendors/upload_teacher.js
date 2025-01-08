const form = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const transcriptTextarea = document.getElementById('transcriptTextarea');
const fileInfo = document.getElementById('fileInfo');
const startButton = document.getElementById('start');
const startForm = document.getElementById('startForm');
/*选择音频按钮*/
document.addEventListener('DOMContentLoaded', function () {

    fileInput.addEventListener('change', function () {
        const files = fileInput.files;
        fileInfo.innerHTML = ''; // 先清空之前显示的内容
        for (let i = 0; i < files.length; i++) {
            const listItem = document.createElement('p');
            listItem.textContent = `已选择音频文件: ${files[i].name}`;
            fileInfo.appendChild(listItem);
        }
    });

    const audioPlayer = document.querySelector('audio');
    uploadForm.addEventListener('submit', function (event) {
        event.preventDefault();
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            const fileURL = URL.createObjectURL(file);
            audioPlayer.src = fileURL;
            // 不立即播放音频，只是设置好音频源，等待用户操作播放按钮来播放
        }
    });
});
/*确定上传按钮*/
form.addEventListener('submit', (event) => {
    if (fileInfo.textContent === "请选择文件") {
                alert('请先点击黄色的“选择音频”按钮');
                return;
            }
    event.preventDefault();
    // 先清空之前的文件列表项，确保只有一条记录
    fileList.innerHTML = '';
    if (fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        const listItem = document.createElement('li');
        listItem.textContent = fileName;
        // 添加内联样式来去除圆点
        listItem.style.listStyleType = 'none';
        fileList.appendChild(listItem);
    }
    // 获取文本域元素
    const transcriptTextarea = document.getElementById('transcriptTextarea');
    // 清空文本域中的内容
    transcriptTextarea.textContent = '';
    // 修改 placeholder 属性值
    transcriptTextarea.placeholder = '请等待几秒';

    // 此处可以添加代码将表单数据发送给后端，例如使用 fetch 或 XMLHttpRequest 等（下面有示例介绍）
    const formData = new FormData(form);
    fetch('/transcribe_audio', {
        method: 'POST',
        body: formData
    }).then(response => response.text()).then(transcript => {
        transcriptTextarea.textContent = transcript;
        console.log(transcriptTextarea.textContent)
    }).catch(error => console.error('请求出现错误:', error));
});




document.addEventListener('DOMContentLoaded', function () {
    const startJourneyButton = document.getElementById('startJourney');
    const transcriptTextarea = document.getElementById('transcriptTextarea');
    const fileList = document.getElementById('fileList');

    // 点击事件
    startJourneyButton.addEventListener('click', function () {
        // 检查是否已经上传音频文件
        if (fileList.children.length === 0) {
            alert('请先上传音频文件');
            return;
        }

        // 检查转录文本是否为空
        if (transcriptTextarea.value.trim() === "") {
            alert('请先等待几秒完成音频转录操作');
            return;
        }

        // 获取转录文本
        const text_to_pass = transcriptTextarea.value.trim();
        console.log("获取到的 text_to_pass:", text_to_pass);

        // 发送 POST 请求
        fetch('/teacher_next', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                text_to_pass: text_to_pass,
            }),
        })
            .then(response => {
                console.log("fetch 请求状态码:", response.status);
                if (response.redirected) {
                    // 如果后端返回重定向，跳转到目标页面
                    window.location.href = response.url;
                } else if (response.status === 200) {
                    return response.text();
                } else {
                    throw new Error('请求失败');
                }
            })
            .then(html => {
                console.log("后端返回内容:", html);
            })
            .catch(error => {
                console.error('请求错误:', error);
            });
    });
});
