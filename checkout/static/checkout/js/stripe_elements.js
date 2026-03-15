document.addEventListener("DOMContentLoaded", function () {
    const stripe = Stripe(stripePublicKey);

    const elements = stripe.elements({
        clientSecret: clientSecret,
    });

    const paymentElement = elements.create("payment");
    paymentElement.mount("#payment-element");

    const form = document.getElementById("payment-form");
    const submitButton = document.getElementById("submit-button");
    const errorDiv = document.getElementById("payment-errors");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        // stop double clicking
        if (submitButton.disabled) {
            return;
        }

        submitButton.disabled = true;
        submitButton.textContent = "Processing...";
        errorDiv.textContent = "";

        const { error } = await stripe.confirmPayment({
            elements,
            confirmParams: {
                return_url: window.location.origin + "/checkout/success/"
            }
        });

        if (error) {
            errorDiv.textContent = error.message;
            submitButton.disabled = false;
            submitButton.textContent = "Pay Now";
        }
    });
});