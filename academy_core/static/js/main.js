async function cartUpdate(e) {
    const { data } = await axios(e.dataset.url)
    const { message, items_count } = data

    notyf.success({
        message,
        dismissible: true,
        icon: false
    })

    document.getElementById('cart-items-count').innerHTML = items_count
}

















const cash_button = document.getElementById('cash-order-btn');

if (cash_button) {
    cash_button.addEventListener('click', async (event) => {
        event.preventDefault();

        try {
            const form = document.getElementById('form-user-info');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const response = await fetch('/checkout/cash', {
                method: 'POST',
                body: new FormData(form),
                headers: {'X-CSRFToken': csrfToken}
            });
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'حدث خطأ أثناء إنشاء الطلب');
            }

            window.location.href = data.redirect_url;
        } catch (error) {
            console.error(error);
            notyf.error(error.message);
        }
    });
}




















async function cartRemove(e) {
    await axios(e.dataset.url)
    location.reload()
}
function showCashPayment() {
    const cashCard = document.getElementById('cash-card');

    cashCard.style.display = 'block';
}



async function createCashOrder() {
    try {
        const form = document.getElementById('form-user-info');
        const formData = new FormData(form);

        const { data } = await axios.post('/checkout/cash', formData);

        window.location.href = data.redirect_url;

    } catch (e) {
        notyf.error(e.response?.data?.message || 'حدث خطأ أثناء إنشاء الطلب');
    }
}

