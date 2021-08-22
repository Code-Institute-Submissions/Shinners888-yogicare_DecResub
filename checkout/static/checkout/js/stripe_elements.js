/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
/* Styles from stripe docs */
var style = {
    base: {
        color: '#333333',
        fontFamily: '"Montserrat", sans-serif',
        
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#333333'
        }
    },
    invalid: {
        color: 'red',
        iconColor: 'red'
    }
};
var card = elements.create('card', {style: style});
card.mount('#payment-element');

