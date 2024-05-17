function resetForm(button) {
  const resetUrl = button.getAttribute("data-reset-url");
  window.location.href = resetUrl;
}
