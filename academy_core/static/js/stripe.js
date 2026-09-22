

const stripe = Stripe("pk_test_51U8WBv92FfFLxs5khEuFsW8TdCTGr2EUSk8CX8sWnE22hhB1bxl3y8XVfimTjS9fZ61lZiLZ5l1wxkJdQZIezOTo008169F0I8");

let elements = null;
let paymentElement = null;
const checkoutBtn = document.getElementById("checkout-btn");
const course_id = checkoutBtn.dataset.courseId;

const stripeSubmit = document.getElementById("stripe-submit");

async function createStripeSession() {

    const form = document.getElementById("form-user-info");
    const formData = new FormData(form);

    formData.append("course_id", course_id);


    stripeSubmit.disabled = true;

    try {

        const response = await axios.post(
            "/checkout/stripe",
            formData
        );

        const clientSecret = response.data.client_secret;

        console.log("Client secret:", clientSecret);

        if (!clientSecret) {
            throw new Error("Stripe client_secret was not returned.");
        }

        /*
          * إذا كان Payment Element موجودًا مسبقًا
          * لا تنشئ واحدًا جديدًا.
          */
        if (paymentElement) {
            paymentElement.destroy();
            paymentElement = null;
        }

        const appearance = {
            theme: "flat"
        };

        elements = stripe.elements({
            clientSecret: clientSecret,
            appearance: appearance
        });

        paymentElement = elements.create("payment");

        paymentElement.mount("#payment-element");

        document.getElementById("stripe-card").style.display = "block";

        stripeSubmit.disabled = false;

    } catch (error) {

        console.error("Stripe error:", error);

        console.error(
            "Server response:",
            error.response?.data
        );

        notyf.error(
            error.response?.data?.message ||
            error.message ||
            "Something went wrong."
        );

        stripeSubmit.disabled = false;
    }
}


async function _stripeFormSubmit(e) {

    e.preventDefault();

    if (!stripe || !elements) {
        notyf.error("Stripe is not ready.");
        return;
    }

    stripeSubmit.disabled = true;

    const host =
        window.location.protocol +
        "//" +
        window.location.host;

    const { error } = await stripe.confirmPayment({

        elements: elements,

        confirmParams: {
            return_url:
                `${host}/checkoutcomplete`,
        },

    });

    if (error) {

        console.error("Payment error:", error);

        if (
            error.type === "card_error" ||
            error.type === "validation_error"
        ) {
            notyf.error(error.message);
        } else {
            notyf.error(
                "حدث خطأ أثناء عملية الدفع."
            );
        }

        stripeSubmit.disabled = false;
    }
}


document
    .getElementById("payment-form")
    .addEventListener(
        "submit",
        _stripeFormSubmit
    );


