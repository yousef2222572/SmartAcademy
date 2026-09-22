
const attach_btn = document.getElementById("attach_btn");
const imageInput = document.getElementById("image");
const send_btn = document.getElementById("send_btn");
const q_countainer = document.getElementById("q_countainer");
const lesson_id = document.getElementById("lesson_id").dataset.lesson_id;
const image_preview = document.getElementById("image-preview");
const messageInput = document.getElementById("message");

// متغيرات الرد والملفات
let selectedFiles = [];
let replyTargetId = null; // يحفظ معرف الرسالة عند الرد

/* =========================
    Open file picker
========================= */
attach_btn.addEventListener("click", () => {
    imageInput.click();
});

/* =========================
    Show & Accumulate selected images
========================= */
imageInput.addEventListener("change", () => {
    const files = Array.from(imageInput.files);
    if (files.length === 0) return;

    const newFiles = files.map(file => ({
        file: file,
        previewUrl: URL.createObjectURL(file)
    }));

    selectedFiles = selectedFiles.concat(newFiles);
    renderPreviews();

    imageInput.value = "";
});

function renderPreviews() {
    image_preview.innerHTML = "";

    if (selectedFiles.length === 0) {
        image_preview.classList.remove("active");
        return;
    }

    image_preview.classList.add("active");

    selectedFiles.forEach((item, index) => {
        const preview_item = document.createElement("div");
        preview_item.className = "preview-item";

        const img = document.createElement("img");
        img.src = item.previewUrl;
        img.alt = item.file.name;

        const removeBtn = document.createElement("button");
        removeBtn.type = "button";
        removeBtn.className = "remove-img-btn";
        removeBtn.innerHTML = "&times;";
        removeBtn.onclick = (e) => {
            e.stopPropagation();
            removeFile(index);
        };

        preview_item.appendChild(img);
        preview_item.appendChild(removeBtn);
        image_preview.appendChild(preview_item);
    });
}

function removeFile(index) {
    URL.revokeObjectURL(selectedFiles[index].previewUrl);
    selectedFiles.splice(index, 1);
    renderPreviews();
}

/* =========================
    Reply Logic (Event Delegation)
========================= */
q_countainer.addEventListener("click", (e) => {
    const replyBtn = e.target.closest(".message-reply-btn");
    if (!replyBtn) return;

    const qId = replyBtn.dataset.q_id;
    const messageBubble = replyBtn.closest(".message-bubble");
    
    // استخراج نص الرسالة
    const msgTextEl = messageBubble.querySelector(".message-text");
    const replyText = msgTextEl ? msgTextEl.innerText.trim() : "مرفق صورة/ملف";


    messageInput.dataset.id = qId;
    replyTargetId = qId;

    // 2. إظهار شريط المعاينة فوق الحقل بخط رمادي
    showReplyBanner(replyText);

    // التركيز على حقل الكتابة
    messageInput.focus();
});

function showReplyBanner(text) {
    let banner = document.getElementById("reply-banner");
    if (!banner) {
        banner = document.createElement("div");
        banner.id = "reply-banner";
        banner.className = "reply-banner";
        
        // إدراج شريط المعاينة قبل صندوق الـ input مباشرة
        const inputWrapper = messageInput.closest(".input-wrapper");
        inputWrapper.parentNode.insertBefore(banner, inputWrapper);
    }

    banner.innerHTML = `
        <div class="reply-info">
            <span class="reply-title">الرد على:</span>
            <span class="reply-text-preview">${text}</span>
        </div>
        <button type="button" class="cancel-reply-btn" onclick="clearReplyState()">&times;</button>
    `;
    banner.style.display = "flex";
}

function clearReplyState() {
    replyTargetId = null;
    delete messageInput.dataset.id;

    const banner = document.getElementById("reply-banner");
    if (banner) {
        banner.style.display = "none";
        banner.innerHTML = "";
    }
}

/* =========================
    Send message
========================= */
send_btn.addEventListener("click", () => {
    const message = messageInput.value.trim();
    const csrfElement = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrfToken = csrfElement ? csrfElement.value : '';

    if (!message && selectedFiles.length === 0) {
        return;
    }


    let typeBool = '0'

    const formData = new FormData();
    formData.append("message", message);
    formData.append("lesson_id", lesson_id);


    if (replyTargetId) {
        formData.append("question_id", replyTargetId);
        typeBool=1
    }
    formData.append("type_bool", typeBool);

    selectedFiles.forEach((item) => {
        formData.append("files", item.file);
    });

    send_btn.disabled = true;

    fetch("/sendmessage/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Request failed");
        }
        return response.json();
    })
    .then(data => {
        // تجهيز عناصر HTML المشتركة لتفادي تكرار الكود
        const message_html = data.message ? `
            <div class="message-text">
                ${data.message}
            </div>
        ` : "";

        const imagesSources = (data.images_urls && data.images_urls.length > 0) 
            ? data.images_urls 
            : selectedFiles.map(item => item.previewUrl);

        const images_html = imagesSources.length > 0 ? `
            <div class="message-images">
                ${imagesSources.map(src => `
                    <div class="preview-item">
                        <img src="${src}" alt="attachment" />
                    </div>
                `).join('')}
            </div>
        ` : "";

        if (data.id) {
        q_countainer.insertAdjacentHTML('beforeend', `
        
                            <div data-q_id="${data.id}" style="background-color: #f4f5f7; border-radius: 12px; margin-bottom: 15px; padding: 10px;">
                                <div class="message-row message-user">
                                    <div class="message-bubble" style="width: 100%; padding: 15px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px;">
                                        
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; padding-bottom: 8px; border-bottom: 1px solid #f0f0f0;">
                                            <span style="font-weight: bold; color: #0d6efd; font-size: 15px;">
                                                ${data.user_name}
                                            </span>
                                            <span style="color: black; font-size: 13px;">
                                                ${data.time}
                                            </span>
                                        </div>
                                        

                                        <div style="direction: ltr; text-align: left; margin-bottom: 10px; color: #333; font-size: 15px;">
                                            <span style="color: black; padding: 0px;">${message_html}</span>
                                        </div>
                                        ${images_html}
                                        
                                        <div class="message-actions" style="margin-top: 15px; text-align: left;">
                                            <button
                                                type="button"
                                                class="message-reply-btn"
                                                data-q_id="${data.id}"
                                                title="Reply"
                                                style="cursor: pointer; padding: 6px 12px; border: none; background-color: black; color: white; border-radius: 6px;"
                                            >
                                                <span class="reply-icon">↩</span>
                                                <span>Reply</span>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        
        
        
        `);

        } else {
            // حالة: رد على سؤال موجود
            const targetDiv = q_countainer.querySelector(`[data-q_id='${data.message_reply_id}']`);

            if (targetDiv) {


                targetDiv.innerHTML += `
                    <div
                        data-q_id="${data.id}"
                        class="message-row"
                        style="
                            width: 100%;
                            margin: 12px 0 0 0;
                            padding-left: 28px;
                            box-sizing: border-box;
                        "
                    >

                        <div
                            class="message-bubble"
                            style="
                                width: 100%;
                                padding: 14px 16px;
                                background: #f8f9fa;
                                color: #333;
                                border: 1px solid #e1e5e9;
                                border-left: 3px solid #6c757d;
                                border-radius: 10px;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
                                box-sizing: border-box;
                            "
                        >

                            <!-- Header -->
                            <div
                                style="
                                    display: flex;
                                    justify-content: space-between;
                                    align-items: center;
                                    gap: 10px;
                                    margin-bottom: 10px;
                                    padding-bottom: 8px;
                                    border-bottom: 1px solid #e9ecef;
                                "
                            >

                                <span
                                    style="
                                        font-weight: 600;
                                        color: #0d6efd;
                                        font-size: 14px;
                                    "
                                >
                                    ${data.user_name}
                                </span>

                                <span
                                    style="
                                        color: #868e96;
                                        font-size: 12px;
                                        white-space: nowrap;
                                    "
                                >
                                    ${data.time}
                                </span>

                            </div>


                            <!-- Reply content -->
                            <div
                                style="
                                    direction: rtl;
                                    text-align: right;
                                    color: #343a40;
                                    font-size: 14px;
                                    line-height: 1.7;
                                "
                            >
                                ${message_html}
                            </div>


                            <!-- Images -->
                            ${images_html}

                        </div>

                    </div>
                `;


            } else {
                console.warn("لم يتم العثور على السؤال الأصلي المُراد الرد عليه برقم:", data.message_reply_id);
            }
        }

        // إعادة التصفير كاملة بعد النجاح
        messageInput.value = "";
        selectedFiles = [];
        renderPreviews();
        clearReplyState();
    })
    .catch(error => {
        console.error("Error sending message:", error);
    })
    .finally(() => {
        send_btn.disabled = false;
    });
});

