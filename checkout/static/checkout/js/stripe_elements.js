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

        if (submitButton.disabled) {
            return;
        }

        submitButton.disabled = true;
        submitButton.textContent = "Processing...";
        errorDiv.textContent = "";

        const result = await stripe.confirmPayment({
            elements,
            redirect: "if_required",
        });

        if (result.error) {
            errorDiv.textContent = result.error.message;
            submitButton.disabled = false;
            submitButton.textContent = "Pay £" + totalAmount;
            return;
        }

        form.submit();
    });
});