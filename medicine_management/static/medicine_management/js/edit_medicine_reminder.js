document.addEventListener('DOMContentLoaded', function () {
  const methodSelect = document.getElementById('id_notification_method');
  const emailField = document.getElementById('email-field');
  const phoneField = document.getElementById('phone-field');

  function toggleFields() {
    const selected = methodSelect.value;
    if (selected === 'email') {
      emailField.style.display = 'block';
      phoneField.style.display = 'none';
    } else if (selected === 'sms') {
      emailField.style.display = 'none';
      phoneField.style.display = 'block';
    } else {
      emailField.style.display = 'none';
      phoneField.style.display = 'none';
    }
  }

  methodSelect.addEventListener('change', toggleFields);
  toggleFields(); 
});
