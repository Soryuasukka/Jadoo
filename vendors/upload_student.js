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




// 为startForm表单的submit事件添加事件处理函数，这样只会在表单提交时触发相关逻辑，避免重复提交
startForm.addEventListener('submit', function (event) {
    event.preventDefault();
    // 判断是否已经上传了音频文件，即fileList中是否有内容
    if (fileList.children.length === 0) {
        console.log("音频文件未上传，触发返回操作");
        alert('请先上传音频文件')
        return;
    }
    if (transcriptTextarea.textContent === "") {
        console.log("转录文本为空，触发返回操作");
        alert('请先等待几秒完成音频转录操作');
        return;
    }

    // 打印表单提交事件被触发的提示信息，用于确认事件是否正常绑定并执行
    console.log("表单提交事件已触发");
    const text_to_pass = transcriptTextarea.value;
    console.log("获取到的text_to_pass内容:", text_to_pass); // 检查是否成功获取到文本域内容以及内容具体是什么
    // 创建FormData对象来组织要发送的数据
    const formData = new FormData(startForm);
    formData.append('text_to_pass', text_to_pass);
    for (const [key, value] of formData) {
        console.log("键：", key, "值：", value);
    }


    fetch('/student_next', {
            method: 'POST',
            body: formData
        })
       .then(response => {
            console.log("fetch请求已发送，收到响应，状态码:", response.status); // 检查请求是否成功发送以及响应状态码情况
            if (response.status === 200) {
                return response.text();
            }
            throw new Error('请求出现错误，状态码非200');
        })
       .then(html => {
            console.log("获取到的后端返回内容:", html);

            // 这里可以根据后端返回的内容进行一些额外处理，比如判断是否需要手动触发页面跳转等情况
            // 如果后端返回的内容里有特定的跳转指示（如在HTML中包含了重定向的meta标签等情况），可以在这里做相应处理
            // 但通常如果后端配置正确，表单提交后会自动根据响应头进行页面重定向，这里可以不做额外操作，具体根据实际情况调整
        })
       .catch(error => {
            console.error('请求出现错误:', error);
            console.error('错误详细内容:', error.message);

        });
    startForm.submit();
    });