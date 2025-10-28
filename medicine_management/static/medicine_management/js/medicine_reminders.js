function toggleNotificationFields() {
    const notificationMethod = document.getElementById("id_notification_method").value;
    const emailField = document.getElementById("email_field");
    const phoneField = document.getElementById("phone_field");

    emailField.style.display = "none";
    phoneField.style.display = "none";

    if (notificationMethod === "email") {
      emailField.style.display = "block";
    } else if (notificationMethod === "sms") {
      phoneField.style.display = "block";
    }
  }

  window.onload = function() {
    toggleNotificationFields();
  };

  window.addEventListener('DOMContentLoaded', () => {
    const messages = document.querySelectorAll('.message');
    messages.forEach(msg => {
      setTimeout(() => {
        msg.style.display = 'none';
      }, 5000);
    });
  });
